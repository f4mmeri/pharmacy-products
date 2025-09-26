from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
# Para usar MySQL (comenta la línea de SQLite)
# DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password123@localhost:3306/farmacia_db")

# Para usar SQLite (descomenta esta línea para pruebas rápidas)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://farmacia_user:farmacia_pass@mysql:3306/farmacia_db"
)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modelo de la base de datos
class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, index=True)
    tipo = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    requiere_receta = Column(Integer, nullable=False, default=0)  # 0 = False, 1 = True (SQLite compatible)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Crear las tablas
Base.metadata.create_all(bind=engine)


# Modelos Pydantic para la API
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255, description="Nombre del producto")
    tipo: str = Field(..., min_length=1, max_length=100,
                      description="Tipo de producto (medicamento, higiene, vitaminas, etc.)")
    precio: float = Field(..., gt=0, description="Precio del producto en soles")
    stock: int = Field(..., ge=0, description="Cantidad disponible en stock")
    requiere_receta: bool = Field(default=False, description="Indica si el producto requiere receta médica")


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    tipo: Optional[str] = Field(None, min_length=1, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    requiere_receta: Optional[bool] = Field(None, description="Indica si el producto requiere receta médica")


class ProductoResponse(ProductoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    @classmethod
    def from_orm(cls, obj):
        # Convertir el entero de requiere_receta de vuelta a booleano
        data = {
            'id': obj.id,
            'nombre': obj.nombre,
            'tipo': obj.tipo,
            'precio': obj.precio,
            'stock': obj.stock,
            'requiere_receta': bool(obj.requiere_receta),
            'fecha_creacion': obj.fecha_creacion,
            'fecha_actualizacion': obj.fecha_actualizacion
        }
        return cls(**data)

    class Config:
        from_attributes = True


# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crear la aplicación FastAPI
app = FastAPI(
    title="API REST Farmacia - Productos",
    description="Microservicio para gestionar productos de farmacia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Endpoints de la API

@app.get("/", tags=["Root"])
async def root():
    return {"mensaje": "API REST Farmacia - Microservicio de Productos", "version": "1.0.0"}


@app.get("/echo", tags=["Test"])
async def echo_get(message: str = "pong"):
    """
    Endpoint de echo para GET - devuelve el mensaje que recibe
    """
    return {
        "echo": message,
        "timestamp": datetime.utcnow(),
        "method": "GET"
    }


@app.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, tags=["Productos"])
async def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo producto en la farmacia
    """
    # Verificar si ya existe un producto con el mismo nombre
    db_producto = db.query(ProductoDB).filter(ProductoDB.nombre == producto.nombre).first()
    if db_producto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con este nombre"
        )

    # Convertir el producto a diccionario y ajustar el campo booleano
    producto_data = producto.dict()
    producto_data['requiere_receta'] = 1 if producto_data['requiere_receta'] else 0

    db_producto = ProductoDB(**producto_data)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


@app.get("/productos", response_model=List[ProductoResponse], tags=["Productos"])
async def obtener_productos(
        skip: int = 0,
        limit: int = 100,
        tipo: Optional[str] = None,
        stock_minimo: Optional[int] = None,
        db: Session = Depends(get_db)
):
    """
    Obtener lista de productos con filtros opcionales
    """
    query = db.query(ProductoDB)

    if tipo:
        query = query.filter(ProductoDB.tipo.ilike(f"%{tipo}%"))

    if stock_minimo is not None:
        query = query.filter(ProductoDB.stock >= stock_minimo)

    productos = query.offset(skip).limit(limit).all()
    return productos


@app.get("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
async def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtener un producto específico por su ID
    """
    producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto


@app.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
async def actualizar_producto(
        producto_id: int,
        producto_update: ProductoUpdate,
        db: Session = Depends(get_db)
):
    """
    Actualizar un producto existente
    """
    producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    # Actualizar solo los campos proporcionados
    update_data = producto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(producto, field, value)

    producto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(producto)
    return producto


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"])
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un producto
    """
    producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    db.delete(producto)
    db.commit()
    return


@app.patch("/productos/{producto_id}/stock", response_model=ProductoResponse, tags=["Productos"])
async def actualizar_stock(
        producto_id: int,
        request: dict,
        db: Session = Depends(get_db)
):
    """
    Actualizar únicamente el stock de un producto
    Body: {"nuevo_stock": 50}
    """
    nuevo_stock = request.get("nuevo_stock")
    if nuevo_stock is None or nuevo_stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="nuevo_stock debe ser un número mayor o igual a 0"
        )

    producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    producto.stock = nuevo_stock
    producto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(producto)
    return producto


@app.get("/productos/tipo/{tipo}", response_model=List[ProductoResponse], tags=["Productos"])
async def obtener_productos_por_tipo(tipo: str, db: Session = Depends(get_db)):
    """
    Obtener productos filtrados por tipo
    """
    productos = db.query(ProductoDB).filter(ProductoDB.tipo.ilike(f"%{tipo}%")).all()
    return productos


@app.get("/productos/stock-bajo/{minimo}", response_model=List[ProductoResponse], tags=["Productos"])
async def obtener_productos_stock_bajo(minimo: int = 10, db: Session = Depends(get_db)):
    """
    Obtener productos con stock por debajo del mínimo especificado
    """
    productos = db.query(ProductoDB).filter(ProductoDB.stock < minimo).all()
    return productos


@app.get("/productos/con-receta", response_model=List[ProductoResponse], tags=["Productos"])
async def obtener_productos_con_receta(db: Session = Depends(get_db)):
    """
    Obtener productos que requieren receta médica
    """
    productos = db.query(ProductoDB).filter(ProductoDB.requiere_receta == 1).all()
    return productos


@app.get("/productos/sin-receta", response_model=List[ProductoResponse], tags=["Productos"])
async def obtener_productos_sin_receta(db: Session = Depends(get_db)):
    """
    Obtener productos que NO requieren receta médica
    """
    productos = db.query(ProductoDB).filter(ProductoDB.requiere_receta == 0).all()
    return productos


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

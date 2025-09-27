from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine, wait_for_db
from app.productos.controller import router as productos_router
from app.core.seed import seed_db
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Esperar a que la base de datos esté disponible
logger.info("Esperando conexión con la base de datos...")
if not wait_for_db():
    logger.critical("No se pudo conectar a la base de datos después de múltiples intentos")
    exit(1)

# Crear las tablas
logger.info("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API REST Farmacia - Productos",
    description="Microservicio para gestionar productos de farmacia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
origins = [
    "http://localhost:5173",    # Vite
    "http://127.0.0.1:5173",    # Vite con 127.0.0.1
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(productos_router, prefix="/api")  # Agregué el prefijo /api

# Poblar la base de datos con datos iniciales
logger.info("Ejecutando seed de la base de datos...")
seed_db()

@app.get("/echo", tags=["Test"])
def echo_get(message: str = "pong"):
    from datetime import datetime
    return {
        "echo": message,
        "timestamp": datetime.utcnow(),
        "method": "GET"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": __import__('datetime').datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
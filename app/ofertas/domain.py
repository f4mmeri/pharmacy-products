from sqlalchemy import Column, Integer, DateTime, Float, ARRAY, func
from app.core.database import Base

class OfertaDB(Base):
    __tablename__ = "ofertas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    producto_ids = Column(ARRAY(Integer), nullable=False)  # lista de IDs de productos afectados
    descuentos = Column(ARRAY(Float), nullable=False)      # lista de descuentos por producto
    fecha_vencimiento = Column(DateTime, nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
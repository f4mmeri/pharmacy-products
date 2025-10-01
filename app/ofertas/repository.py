from app.ofertas.domain import OfertaDB
from sqlalchemy.orm import Session
from datetime import datetime

def get_by_id(db: Session, oferta_id: int):
    return db.query(OfertaDB).filter(OfertaDB.id == oferta_id).first()

def get_all(db: Session):
    return db.query(OfertaDB).all()

def create(db: Session, oferta: dict):
    db_oferta = OfertaDB(**oferta)
    db.add(db_oferta)
    db.commit()
    db.refresh(db_oferta)
    return db_oferta

def update(db: Session, oferta, update_data: dict):
    for field, value in update_data.items():
        setattr(oferta, field, value)
    oferta.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(oferta)
    return oferta

def delete(db: Session, oferta):
    db.delete(oferta)
    db.commit()
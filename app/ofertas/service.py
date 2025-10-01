from app.ofertas.repository import (
    get_by_id, get_all, create, update, delete
)
from app.ofertas.dto import OfertaCreate, OfertaUpdate
from fastapi import HTTPException, status

def crear_oferta(db, oferta: OfertaCreate):
    # Validaciones básicas
    if len(oferta.producto_ids) != len(oferta.descuentos):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las listas producto_ids y descuentos deben tener el mismo tamaño")
    data = oferta.dict()
    return create(db, data)

def obtener_oferta(db, oferta_id: int):
    oferta = get_by_id(db, oferta_id)
    if not oferta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta no encontrada")
    return oferta

def obtener_ofertas(db):
    return get_all(db)

def actualizar_oferta(db, oferta_id: int, oferta_update: OfertaUpdate):
    oferta = get_by_id(db, oferta_id)
    if not oferta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta no encontrada")
    update_data = oferta_update.dict(exclude_unset=True)
    return update(db, oferta, update_data)

def eliminar_oferta(db, oferta_id: int):
    oferta = get_by_id(db, oferta_id)
    if not oferta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Oferta no encontrada")
    delete(db, oferta)
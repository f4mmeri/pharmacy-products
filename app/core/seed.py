import csv
import os
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.productos.domain import ProductoDB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "productos.csv")

def is_db_seeded(db: Session) -> bool:
    return db.query(ProductoDB).first() is not None

def seed_db():
    db = SessionLocal()

    if is_db_seeded(db):
        print("La base de datos ya está poblada. No se realizará el seed.")
        db.close()
        return

    print("Poblando la base de datos con productos de productos.csv...")
    with open(CSV_PATH, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        productos = [
            ProductoDB(
                nombre=row["nombre"],
                tipo=row["tipo"],
                precio=float(row["precio"]),
                stock=int(row["stock"]),
                requiere_receta=(row["requiere_receta"] == 'SI')
            )
            for row in reader
        ]
        db.bulk_save_objects(productos)
        db.commit()
    db.close()
    print(f"Seed completado: {len(productos)} productos insertados.")

if __name__ == "__main__":
    seed_db()
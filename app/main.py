from fastapi import FastAPI
from app.core.database import Base, engine
from app.productos.controller import router as productos_router
from app.core.seed import seed_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API REST Farmacia - Productos",
    description="Microservicio para gestionar productos de farmacia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(productos_router)
seed_db()

@app.get("/echo", tags=["Test"])
def echo_get(message: str = "pong"):
    from datetime import datetime
    return {
        "echo": message,
        "timestamp": datetime.utcnow(),
        "method": "GET"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
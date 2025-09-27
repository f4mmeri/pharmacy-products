import os
from typing import Optional


class Settings:
    # Configuración de base de datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://farmacia_user:farmacia_password@localhost:3306/farmacia"
    )

    # Configuraciones específicas de MySQL (opcional, para uso directo)
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "farmacia")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "farmacia_user")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "farmacia_password")

    # Configuración del servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
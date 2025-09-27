import os

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "mysql+mysqlconnector://user:password@localhost:3306/farmacia_db"
    )

settings = Settings()
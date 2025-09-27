import os

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://farmacia_user:farmacia_pass@localhost:3306/farmacia_db"
    )

settings = Settings()
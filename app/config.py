import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://:memory:")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

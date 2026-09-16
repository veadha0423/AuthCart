from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./authcart.db"

# Create the SQLite engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining database models
Base = declarative_base()

# Helper dependency to get the database session in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
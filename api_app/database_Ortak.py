from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(
   "postgresql+pg8000://user:password@postgresserver/db",
    isolation_level="READ UNCOMMITTED"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database_Lisans import Base as BaseLisans
from .database_Ortak import Base as BaseOrtak



"""class Lisans(BaseLisans):
    __tablename__ = "lisanslar"
    __table_args__={'schema':'denemeLisans'}
    id = Column(Integer, primary_key=True, index=True)
    musterikodu = Column(String, unique=True, index=True)
    dbname = Column(String)
    dbusername = Column(String)
    dbpassword = Column(String)"""

class Lisanslar(BaseOrtak):
    __tablename__ = "lisanslar"
    __table_args__={'schema':'public'}
    id = Column(Integer, primary_key=True, index=True)
    musterikodu = Column(String, unique=True, index=True)
    dbname = Column(String)
    dbusername = Column(String)
    dbpassword = Column(String)
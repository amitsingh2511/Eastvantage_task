from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Address(Base):
    """
    
    Sqlalchemy module for address database table.
    
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)

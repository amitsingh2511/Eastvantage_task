from pydantic import BaseModel, Field
from typing import Optional

class AddressBase(BaseModel):
    """
        Base Pydantic Class for Address
    """
    name: str
    latitude: float = Field(..., gt=-90, lt=90)
    longitude: float = Field(..., gt=-180, lt=180)

class AddressCreate(AddressBase):
    """
        Base Pydantic Class for creating Address
    """
    pass

class Address(AddressBase):
    """
        Base Pydantic Class for fetching Address by id.
    """
    id: int

    class Config:
        orm_mode = True

import geopy.distance
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import List
from . import models, schemas

def get_address(db: Session, address_id: int) -> JSONResponse:
    """_summary_

    Args:
        db (Session): Database connection
        address_id (int): set the address id

    Returns:
        _type_: Json
    """
    return db.query(models.Address).filter(models.Address.id == address_id).first()



def get_addresses(db: Session, skip: int = 0, limit: int = 10) -> List[JSONResponse]:
    """_summary_

    Args:
        db (Session): Database connection
        skip (int, optional): skip: page. Defaults to 0.
        limit (int, optional): limit: set the limit of address. Defaults to 10.

    Returns:
        _type_: list of Json
    """
    return db.query(models.Address).offset(skip).limit(limit).all()


def create_address(db: Session, address: schemas.AddressCreate) -> JSONResponse: 
    """_summary_

    Args:
        db (Session): Database connections
        address (schemas.AddressCreate): A Pydantic Model
                                        - name : name of the address
                                        - latitude: latitude of address
                                        - longitude: longitude of the address.

    Returns:
        _type_: Json 
    """
    db_address = models.Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def update_address(db: Session, address_id: int, address: schemas.AddressCreate) -> JSONResponse:
    """_summary_

    Args:
        db (Session): Database connection
        address_id (int): set the address id
        address (schemas.AddressCreate): A Pydantic Model
                                        - name : name of the address
                                        - latitude: latitude of address
                                        - longitude: longitude of the address.

    Returns:
        _type_: Json
    """
    db_address = get_address(db, address_id)
    if db_address:
        db_address.name = address.name
        db_address.latitude = address.latitude
        db_address.longitude = address.longitude
        db.commit()
        db.refresh(db_address)
        return db_address
    return None


def delete_address(db: Session, address_id: int) -> JSONResponse:
    """_summary_

    Args:
        db (Session): Database connection
        address_id (int): set the address id

    Returns:
        _type_: Json
    """
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
        return db_address
    return None


def get_addresses_within_distance(db: Session, latitude: float, longitude: float, distance: float) -> List[JSONResponse]:
    """_summary_

    Args:
        db (Session): Database connection
        latitude (float): set the value of latitude
        longitude (float): set the value of longitude
        distance (float): set the value of distance

    Returns:
        _type_: List of Json
    """
    all_addresses = db.query(models.Address).all()
    nearby_addresses = []
    for address in all_addresses:
        if geopy.distance.distance((latitude, longitude), (address.latitude, address.longitude)).km <= distance:
            nearby_addresses.append(address)
    return nearby_addresses

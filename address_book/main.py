from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import JSONResponse
import address_book.crud as crud
import address_book.models as models
import address_book.schemas as schemas
from address_book.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address")

@app.post("/addresses/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)) -> JSONResponse:
    """_summary_

    Args:
        address (schemas.AddressCreate): A Pydantic Model
                                        - name : name of the address
                                        - latitude: latitude of address
                                        - longitude: longitude of the address.
                                        
        db (Session, optional): database connection. Defaults to Depends(get_db).

    Returns: 
        _type_: Json
    """
    return crud.create_address(db=db, address=address)

@app.get("/addresses/", response_model=List[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[JSONResponse]:
    """_summary_

    Args:
        skip (int, optional): Skip - page. Defaults to 0.
        limit (int, optional): Limit - set limit of the data. Defaults to 10.
        db (Session, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        _type_: List of Json
    """
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses

@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """_summary_

    Args:
        address_id (int): set the address id
        db (Session, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: handling raise exceptions

    Returns:
        _type_: Json
    """
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)) -> JSONResponse:
    """_summary_

    Args:
        address_id (int): set the value of address id
        address (schemas.AddressCreate): A Pydantic Model
                                        - name : name of the address
                                        - latitude: latitude of address
                                        - longitude: longitude of the address.
        db (Session, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: handled raise exceptions

    Returns:
        _type_: Json
    """
    db_address = crud.update_address(db, address_id=address_id, address=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.delete("/addresses/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """_summary_

    Args:
        address_id (int): set the address id
        db (Session, optional): Database connection. Defaults to Depends(get_db).

    Raises:
        HTTPException: handled raise exceptions

    Returns:
        _type_: Json
    """
    db_address = crud.delete_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.get("/addresses/nearby/", response_model=List[schemas.Address])
def read_addresses_within_distance(latitude: float, longitude: float, distance: float, db: Session = Depends(get_db)) -> List[JSONResponse]:
    """_summary_

    Args:
        latitude (float): set the latitude value.
        longitude (float): set the longitude value.
        distance (float): set the distance value.
        db (Session, optional): Database connection. Defaults to Depends(get_db).

    Returns:
        _type_: List of Json
    """
    addresses = crud.get_addresses_within_distance(db, latitude=latitude, longitude=longitude, distance=distance)
    return addresses

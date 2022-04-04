#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, APIRouter, Depends

from db import SessionLocal, engine
import schemas
import models
import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Find a bookkeeper API")
router = APIRouter(prefix="/values", tags=['values'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Bookkeepers
@app.get("/")
async def read_root():
    return {
        "title": "Find a Bookkeeper API",
        "message": "Welcome to find a bookkeeper API. Check the docs for info."
    }

@app.get("/bookkeepers", response_model = list[schemas.Bookkeeper])
async def read_bookkeepers(skip: int = 0, limit: int = 20, search: str = None, db = Depends(get_db)):
    if search is not None:
        bookkeepers = crud.bookkeeper.get_by_name(db, search, skip, limit)
        return bookkeepers
    return crud.bookkeeper.get_all(db, skip, limit)

@app.get("/bookkeepers/{bookkeeper_id}", response_model = schemas.Bookkeeper)
async def read_bookkeeper(bookkeeper_id: int, db = Depends(get_db)):
    result = crud.bookkeeper.get(db, bookkeeper_id)
    if result:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {bookkeeper_id}"
    )

@app.post("/bookkeepers/", response_model = schemas.Bookkeeper)
async def create_bookkeeper(bookkeeper_in: schemas.BookkeeperCreate, db = Depends(get_db)):
    return crud.bookkeeper.create(db, bookkeeper_in)

@app.delete("/bookkeepers/{bookkeeper_id}")
async def delete_bookkeeper(bookkeeper_id: int, db = Depends(get_db)):
    result = crud.bookkeeper.delete(db, bookkeeper_id)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {bookkeeper_id}"
    )

@app.put("/bookkeepers/{bookkeeper_id}")
async def update_bookkeeper(bookkeeper_id: int, bookkeeper_in: schemas.BookkeeperUpdate, db = Depends(get_db)):
    result = crud.bookkeeper.update(db, bookkeeper_id, bookkeeper_in)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"there's no item with id: {bookkeeper_id}"
    )

@app.get("/bookkeepers/{bookkeeper_id}/services", response_model = list[str])
async def read_bookkeeper(bookkeeper_id: int, db = Depends(get_db)):
    result = crud.bookkeeper.get_services(db, bookkeeper_id)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {bookkeeper_id}"
    )

@app.post("/bookkeepers/{bookkeeper_id}/services/{service_id}", response_model = schemas.Bookkeeper)
async def add_service(bookkeeper_id: int, service_id: int, db = Depends(get_db)):
    # check if service id is there in db
    result = crud.service.get(db, service_id)
    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = f"There's no service with id: {bookkeeper_id}"
        )
    result = crud.bookkeeper.get(db, bookkeeper_id)
    if result is None:
        raise HTTPException(
            status_code = 404,
            detail = f"There's no bookkeeper with id: {service_id}"
        )
    result = crud.bookkeeper.add_service(db, bookkeeper_id, service_id)
    return crud.bookkeeper.get(db, bookkeeper_id)

# Resources
@router.get("/")
def read_resources():
    return {
        "message": "Query for resources: possible values for services and locations"
    }

@router.get("/services", response_model=list[schemas.Service])
async def read_services(skip: int = 0, limit: int = 20, db = Depends(get_db)):
    result = crud.service.get_all(db, skip, limit)
    return result

@router.post("/services", response_model = schemas.Service)
async def create_service(service_in: schemas.ServiceCreate, db = Depends(get_db)):
    return crud.service.create(db, service_in)

@router.get("/services/{service_id}", response_model = schemas.Service)
async def read_service(service_id: int, db = Depends(get_db)):
    result = crud.service.get(db, service_id)
    if result:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {service_id}"
    )

@router.put("/services/{service_id}", response_model = schemas.Service)
async def update_service(service_id: int, service_in: schemas.ServiceUpdate, db = Depends(get_db)):
    result = crud.service.update(db, service_id, service_in)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"there's no item with id: {service_id}"
    )

@router.delete("/services/{service_id}")
async def delete_service(service_id: int, db = Depends(get_db)):
    result = crud.service.delete(db, service_id)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {service_id}"
    )

# Location
@router.get("/locations", response_model=list[schemas.Location])
async def read_locations(skip: int = 0, limit: int = 20, db = Depends(get_db)):
    result = crud.location.get_all(db, skip, limit)
    return result

@router.post("/locations", response_model = schemas.Location)
async def create_location(location_in: schemas.LocationCreate, db = Depends(get_db)):
    return crud.location.create(db, location_in)

@router.get("/locations/{location_id}", response_model = schemas.Location)
async def read_location(location_id: int, db = Depends(get_db)):
    result = crud.location.get(db, location_id)
    if result:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {location_id}"
    )

@router.put("/locations/{location_id}", response_model = schemas.Location)
async def update_location(location_id: int, location_in: schemas.LocationUpdate, db = Depends(get_db)):
    result = crud.location.update(db, location_id, location_in)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"there's no item with id: {location_id}"
    )

@router.delete("/locations/{location_id}")
async def delete_location(location_id: int, db = Depends(get_db)):
    result = crud.location.delete(db, location_id)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {location_id}"
    )

app.include_router(router)

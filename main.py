#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, APIRouter

from db import SessionLocal
import schemas
import crud

app = FastAPI(title="Find a bookkeeper API")
db = SessionLocal()
router = APIRouter(prefix="/services", tags=['services'])

# Bookkeepers
@app.get("/")
async def read_root():
    return {
        "title": "Find a Bookkeeper API",
        "message": "Welcome to find a bookkeeper API. Check the docs for info."
    }

@app.get("/bookkeepers", response_model = list[schemas.Bookkeeper])
async def read_bookkeepers(skip: int = 0, limit: int = 20, search: str = None):
    if search is not None:
        bookkeepers = crud.bookkeeper.get_by_name(db, search, skip, limit)
        return bookkeepers
    return crud.bookkeeper.get_all(db, skip, limit)

@app.get("/bookkeepers/{bookkeeper_id}", response_model = schemas.Bookkeeper)
async def read_bookkeeper(bookkeeper_id: int):
    result = crud.bookkeeper.get(db, bookkeeper_id)
    if result:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {bookkeeper_id}"
    )

@app.post("/bookkeepers/")
async def create_bookkeeper(bookkeeper_in: schemas.BookkeeperCreate):
    return crud.bookkeeper.create(db, bookkeeper_in)

@app.delete("/bookkeepers/{bookkeeper_id}")
async def delete_bookkeeper(bookkeeper_id: int):
    result = crud.bookkeeper.delete(db, bookkeeper_id)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {bookkeeper_id}"
    )

@app.put("/bookkeepers/{bookkeeper_id}")
async def update_bookkeeper(bookkeeper_id: int, bookkeeper_in: schemas.BookkeeperUpdate):
    result = crud.bookkeeper.update(db, bookkeeper_id, bookkeeper_in)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"there's no item with id: {bookkeeper_id}"
    )

@router.get("/", response_model=list[schemas.Service])
async def read_services(skip: int = 0, limit: int = 20):
    result = crud.service.get_all(db, skip, limit)
    return result

@router.post("/", response_model = schemas.Service)
async def create_service(service_in: schemas.ServiceCreate):
    return crud.service.create(db, service_in)

@router.get("/{service_id}", response_model = schemas.Service)
async def read_service(service_id: int):
    result = crud.service.get(db, service_id)
    if result:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {service_id}"
    )

@router.put("/{service_id}", response_model = schemas.Service)
async def update_service(service_id: int, service_in: schemas.ServiceUpdate):
    result = crud.service.update(db, service_id, service_in)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"there's no item with id: {service_id}"
    )

@router.delete("/{service_id}")
async def delete_service(service_id: int):
    result = crud.service.delete(db, service_id)
    if result is not None:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {service_id}"
    )

app.include_router(router)

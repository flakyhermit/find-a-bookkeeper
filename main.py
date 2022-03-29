#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException

from db import SessionLocal
import schema
import crud

app = FastAPI(title="Find a bookkeeper API")
db = SessionLocal()

# Bookkeepers
@app.get("/")
async def read_root():
    return { "title": "Find a Bookkeeper API", "message": "Welcome to find a bookkeeper API. Check the docs for info." }

@app.get("/bookkeepers", response_model = list[schema.Bookkeeper])
async def read_bookkeepers(skip: int = 0, limit: int = 20, search: str = None):
    if search is not None:
        bookkeepers = crud.search_bookkeepers_by_name(db, search, skip, limit)
    else:
        bookkeepers = crud.get_bookkeepers(db, skip, limit)
    return bookkeepers

@app.get("/bookkeepers/{bookkeeper_id}", response_model = schema.Bookkeeper)
async def read_bookkeeper(bookkeeper_id: int):
    result = crud.get_bookkeeper_by_id(db, bookkeeper_id)
    if result:
        return result
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {bookkeeper_id}"
    )

# @app.get("/bookkeepers/search", response_model = BookkeeperSearchResult)
# async def search_bookkeepers(keyword: str | None = None, limit: int = 20) -> list[dict]:
#     print(keyword)
#     if keyword is not None:
#         result = db.search_bookkeeper_by_name(keyword)
#         print(result)
#         return { "results": result[:limit] }
#     d = db.read_bookkeepers()
#     return { "results" : d[:limit] }

# @app.get("/bookkeepers/{bookkeeper_id}", response_model = Bookkeeper)
# async def read_bookkeeper(bookkeeper_id: int) -> dict[Bookkeeper]:
#     result = db.read_bookkeeper(bookkeeper_id)
#     if result:
#         return result
#     raise HTTPException(
#         status_code = 404,
#         detail = f"There's no item with id: {bookkeeper_id}"
#     )

# @app.post("/bookkeepers/")
# async def create_bookkeeper(bookkeeper_in: BookkeeperCreate):
#     db.create_bookkeeper(bookkeeper_in.name, bookkeeper_in.bio)
#     return { "message": "Bookkeeeper added", "result": bookkeeper }

# # Services
# @app.get("/services", response_model = ServicesSearchResult)
# async def read_services(skip: int = 0, limit: int = 20) -> list[dict]:
#     d = db.read_services()
#     return { "results" : d[skip: skip + limit] }

# @app.get("/services/{service_id}", response_model = Service)
# async def read_service(service_id: int) -> dict[Service]:
#     result = db.read_service(service_id)
#     if result:
#         return result
#     raise HTTPException(
#         status_code = 404,
#         detail = f"There's no item with id: {service_id}"
#     )

# @app.post("/services/")
# async def create_service(service_in: ServiceCreate):
#     service_result = db.check_exits_service(service_in.name.lower())
#     if service_result:
#         return { "message": "Service already exits", "result": service_result }
#     service_result = db.create_service(service_in.name.lower())
#     return { "message": "Service added", "result": service_result }

# @app.delete("/services/")
# async def delete_service(service: str):
#     db.delete_service(service)
#     return { "message": "DONE" }

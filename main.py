#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException

from schema import Bookkeeper, BookkeeperSearchResult, BookkeeperCreate
import db

app = FastAPI(title="Find a bookkeeper API")

@app.get("/")
async def read_root():
    return { "title": "Find a Bookkeeper API", "message": "Welcome to find a bookkeeper API. Check the docs for info." }

DATA = []
with open('./bookkeepers.json', 'r', encoding = 'utf-8') as f:
    from json import load
    data = load(f)

@app.get("/bookkeepers", response_model = BookkeeperSearchResult)
async def read_bookkeepers(skip: int = 0, limit: int = 20) -> list[dict]:
    d = db.read_bookkeepers()
    return { "results" : d[skip: skip + limit] }

@app.get("/bookkeepers/search", response_model = BookkeeperSearchResult)
async def search_bookkeepers(keyword: str | None = None, limit: int = 20) -> list[dict]:
    print(keyword)
    if keyword is not None:
        result = db.search_bookkeeper_by_name(keyword)
        print(result)
        return { "results": result[:limit] }
    d = db.read_bookkeepers()
    return { "results" : d[:limit] }

@app.get("/bookkeepers/{bookkeeper_id}", response_model = Bookkeeper)
async def read_bookkeeper(bookkeeper_id: int) -> dict:
    result = [bookkeeper for bookkeeper in DATA if bookkeeper["id"] == bookkeeper_id]
    if result:
        return result[0]
    raise HTTPException(
        status_code = 404,
        detail = f"There's no item with id: {bookkeeper_id}"
    )

@app.post("/bookkeepers/")
async def create_bookkeeper(recipe_in: BookkeeperCreate):
    max_bookkeeper_id = db.get_max_id()
    bookkeeper = Bookkeeper(
        id = max_bookkeeper_id + 1,
        name = recipe_in.name,
        bio = recipe_in.bio
    )
    db.cr_bookkeeper(bookkeeper.name, bookkeeper.bio)
    return { "message": "Bookkeeeper added", "result": bookkeeper }

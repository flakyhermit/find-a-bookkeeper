#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Find a bookkeeper API")

@app.get("/")
async def read_root():
    return { "title": "Find a Bookkeeper API", "message": "Welcome to find a bookkeeper API. Check the docs for info." }

class Bookkeeper(BaseModel):
    """ The model for a bookkeeper """
    id: int
    name: str
    bio: str

class BookkeeperSearchResult(BaseModel):
    results: list[Bookkeeper]

class BookkeeperCreate(BaseModel):
    name: str
    bio: str


DATA = [
    {
        "id": 1,
        "name": "Martin Thomas",
        "bio": "The founder of Weekend Bookkeeper, himself a weekend bookkeeper."
    },
    {
        "id": 2,
        "name": "Jewel James",
        "bio": "The lead developer of Weekend Bookkeeper, and its chief economic adviser."
    },
    {
        "id": 3,
        "name": "Breezy",
        "bio": "The Weekend Bookkeeper pet robot."
    }
]

@app.get("/bookkeepers", response_model = BookkeeperSearchResult)
async def read_bookkeepers(skip: int = 0, limit: int = 20) -> list[dict]:
    return { "results" : DATA[skip: skip + limit] }

@app.get("/bookkeepers/search", response_model = BookkeeperSearchResult)
async def search_bookkeepers(keyword: str | None = None, limit: int = 20) -> list[dict]:
    if keyword is not None:
        result = [entry for entry in DATA if keyword.lower() in entry["name"].lower()]
        return { "results": result[:limit] }
    return { "results" : DATA[:limit] }

@app.get("/bookkeepers/{bookkeeper_id}", response_model = Bookkeeper)
async def read_bookkeeper(bookkeeper_id: int) -> dict:
    result = [bookkeeper for bookkeeper in DATA if bookkeeper["id"] == bookkeeper_id]
    if result:
        return result[0]
    else:
        return { "message": "id not found in db" }

@app.post("/bookkeepers/")
async def create_bookkeeper(recipe_in: BookkeeperCreate):
    bookkeeper = Bookkeeper(
        id = len(DATA) + 1,
        name = recipe_in.name,
        bio = recipe_in.bio
    )
    DATA.append(bookkeeper)
    return { "message": "Bookkeeeper added", "result": bookkeeper }

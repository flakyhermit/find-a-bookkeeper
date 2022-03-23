#!/usr/bin/env python3

from fastapi import FastAPI

app = FastAPI(title="Find a bookkeeper API")

@app.get("/")
async def read_root():
    return { "title": "Find a Bookkeeper", "message": "Welcome to find a bookkeeper API. Check the docs for info." }

@app.get("/bookkeepers/")
async def read_bookkeepers(skip: int = 0, limit: int = 20):
    # Return only limit number of parameters
    return { "name": "Jewel James" }

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

@app.get("/bookkeepers/{bookkeeper_id}")
async def read_bookkeeper(bookkeeper_id: int):
    result = [bookkeeper for bookkeeper in DATA if bookkeeper["id"] == bookkeeper_id]
    if result:
        return result[0]
    else:
        return { "message": "id not found in db" }

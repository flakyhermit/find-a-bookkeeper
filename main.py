#!/usr/bin/env python3

from fastapi import FastAPI

app = FastAPI(title="Find a bookkeeper API")

class Bookkeeper():
    id: int
    name: str
    bio: str
    def __init__(self, id, name, bio):
        self.id = id
        self.name = name
        self.bio = bio

@app.get("/")
async def read_root():
    return { "title": "Find a Bookkeeper", "message": "Welcome to find a bookkeeper API. Check the docs for info." }

@app.get("/bookkeepers/")
async def read_bookkeepers(skip: int = 0, limit: int = 20):
    # Return only limit number of parameters
    return { "name": "Jewel James" }

data = {
    "id": 1,
    "name": "Martin Thomas",
    "bio": "The founder of Weekend Bookkeeper, himself a weekend bookkeeper."
}

bookkeeper = Bookkeeper(**data)
@app.get("/bookkeepers/{bookkeeper_id}")
async def read_bookkeeper(bookkeeper_id: int):
    return bookkeeper

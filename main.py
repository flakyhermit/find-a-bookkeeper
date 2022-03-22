#!/usr/bin/env python3

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "title": "Find a Bookkeeper", "message": "Welcome to find a bookkeeper API. Check the docs for info." }

@app.get("/bookkeepers/")
def read_bookkeepers():
    return { "name": "Jewel James" }

@app.get("/bookkeepers/{bookkeeper_id}")
def read_bookkeeper(bookkeeper_id: int):
    return { "id": bookkeeper_id, "name": "Dummy Name" }

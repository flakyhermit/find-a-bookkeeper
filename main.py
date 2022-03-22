#!/usr/bin/env python3

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "title": "Find a Bookkeeper",
        "description": "A contact list for bookkeepers."
    }

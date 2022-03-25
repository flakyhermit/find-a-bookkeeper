#!/usr/bin/env python3

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

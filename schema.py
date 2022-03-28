#!/usr/bin/env python3

from pydantic import BaseModel

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

class Service(BaseModel):
    """ The model for a service """
    id: int
    name: str

class ServicesSearchResult(BaseModel):
    results: list[Service]

class ServiceCreate(BaseModel):
    name: str

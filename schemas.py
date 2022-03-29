#!/usr/bin/env python3

from pydantic import BaseModel

class BookkeeperBase(BaseModel):
    name: str
    bio: str

class Bookkeeper(BookkeeperBase):
    id: int
    class Config:
        orm_mode = True

class BookkeeperCreate(BookkeeperBase):
    pass

class BookkeeperUpdate(BookkeeperBase):
    name: str | None = None
    bio: str | None = None

class ServiceBase(BaseModel):
    name: str

class Service(ServiceBase):
    id: int
    class Config:
        orm_mode = True

class ServiceCreate(ServiceBase):
    pass

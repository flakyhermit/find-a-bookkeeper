#!/usr/bin/env python3

from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str

class Service(ServiceBase):
    id: int
    class Config:
        orm_mode = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class LocationBase(BaseModel):
    name: str

class Location(LocationBase):
    id: int
    class Config:
        orm_mode = True

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    pass

class BookkeeperBase(BaseModel):
    name: str
    bio: str

class Bookkeeper(BookkeeperBase):
    id: int
    location: Location
    class Config:
        orm_mode = True

class BookkeeperCreate(BookkeeperBase):
    location_id: int
    pass

class BookkeeperUpdate(BookkeeperBase):
    name: str | None = None
    bio: str | None = None
    location_id: int | None = None

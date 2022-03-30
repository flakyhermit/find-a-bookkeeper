#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String

from db import Base

class Bookkeeper(Base):
    __tablename__ = "bookkeepers"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    bio = Column(String(50))


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))

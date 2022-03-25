#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

connection = create_engine("sqlite://some.db", future = True)

# declarative base class
Base = declarative_base()

class Bookkeeper(Base):
    __tablename__ = 'bookkeeper'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bio = Column(String)

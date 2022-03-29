#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DB_URL = "sqlite:///db.db"

engine = create_engine(
    DB_URL,
    future = True,
    connect_args={ "check_same_thread": False }
)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

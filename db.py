#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import MetaData, Table

from sqlalchemy import select, func

engine = create_engine("sqlite:///db.db", future = True)
metadata = MetaData()

bookkeeper_table = Table(
    'bookkeepers',
    metadata,
    Column("id", Integer, primary_key = True),
    Column("name", String(50)),
    Column("bio", String(200))
)

with engine.begin() as conn:
    metadata.create_all(conn)

def read_bookkeepers():
    with engine.begin() as conn:
        stmt = select(bookkeeper_table)
        results = conn.execute(stmt).all()
        return results

def cr_bookkeeper(name, bio):
    with engine.begin() as conn:
        stmt = bookkeeper_table.insert().values(name = name, bio = bio)
        conn.execute(stmt)

def get_max_id():
    with engine.begin() as conn:
        stmt = select([func.max(bookkeeper_table.c.id)])
        result = conn.execute(stmt)
        result = result.one()
        return result[0]

def initialize():
    with open('./bookkeepers.json', 'r', encoding = 'utf-8') as f:
        from json import load
        data = load(f)

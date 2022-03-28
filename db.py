#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import MetaData, Table

from sqlalchemy.exc import NoResultFound
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

service_table = Table(
    'services',
    metadata,
    Column("id", Integer, primary_key = True),
    Column("name", String(50))
)

with engine.begin() as conn:
    metadata.create_all(conn)

# Bookkeepers
def _read_all(table: Table):
    with engine.begin() as conn:
        stmt = select(table)
        results = conn.execute(stmt).all()
        return results

def _read_by_columnname(table: Table, columnname: str, value: int | str):
    with engine.begin() as conn:
        stmt = select(table).where(table.c[columnname] == value)
        try:
            result = conn.execute(stmt).one()
            return result
        except NoResultFound:
            return False

def read_bookkeepers():
    return _read_all(bookkeeper_table)

def read_bookkeeper(id: int):
    return _read_by_columnname(bookkeeper_table, "id", id)

def search_bookkeeper_by_name(keyword: str):
    with engine.begin() as conn:
        stmt = select(bookkeeper_table).where(bookkeeper_table.c.name.like(f'%{keyword}%'))
        results = conn.execute(stmt).all()
        return results

def create_bookkeeper(name, bio):
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


# Services
def read_services():
    return _read_table_all(service_table)

def check_exits_service(name: str):
    with engine.begin() as conn:
        stmt = select(service_table).where(service_table.c.name == name)
        try:
            result = conn.execute(stmt).one()
            return result
        except NoResultFound:
            return False

def create_service(name):
    with engine.begin() as conn:
        stmt = service_table.insert().values(name = name)
        conn.execute(stmt)
        stmt = select(service_table).where(service_table.c.name == name)
        result = conn.execute(stmt).one()
        return result

def delete_service(name):
    with engine.begin() as conn:
        stmt = service_table.delete().where(service_table.c.name == name)
        conn.execute(stmt)

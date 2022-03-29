#!/usr/bin/env python3

from sqlalchemy.orm import Session
from pydantic import BaseModel

from db import Base

import models
import schemas

class CRUDBase():
    def __init__(self, model: Base, schema: BaseModel):
        self.model = model
        self.schema = schema

    def get_all(self, db: Session, skip: int, limit: int):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get(self, db: Session, id: int):
        result = db.query(self.model).filter(self.model.id == id).first()
        return result

    def create(self, db: Session, item: BaseModel):
        res = self.model(name = item.name, bio = item.bio)
        db.add(res)
        db.commit()
        db.refresh(res)
        return res

    def delete(self, db: Session, id: int):
        res = db.query(self.model).get(id)
        if res is not None:
            db.delete(res)
            db.commit()
        return res

    def update(self, db: Session, id: int, item: BaseModel):
        res = db.query(self.model).get(id)
        if res is not None:
            res.name = item.name
            res.bio = item.bio
            db.commit()
            db.refresh(res)
        return res

def get_bookkeepers(db: Session, skip: int, limit: int):
    return db.query(models.Bookkeeper).offset(skip).limit(limit).all()

def get_bookkeeper_by_id(db: Session, id: int):
    result = db.query(models.Bookkeeper).filter(models.Bookkeeper.id == id).first()
    return result

def search_bookkeepers_by_name(db: Session, search: str, skip: int, limit: int):
    result = db.query(models.Bookkeeper).filter(
        models.Bookkeeper.name.like(f'%{search}%')
    ).offset(skip).limit(limit).all()
    return result

def create_bookkeeper(db: Session, item: schemas.BookkeeperCreate):
    bookkeeper = models.Bookkeeper(name = item.name, bio = item.bio)
    db.add(bookkeeper)
    db.commit()
    db.refresh(bookkeeper)
    return bookkeeper

def delete_bookkeeper(db: Session, id: int):
    bookkeeper = db.query(models.Bookkeeper).get(id)
    if bookkeeper is not None:
        db.delete(bookkeeper)
        db.commit()
    return bookkeeper

def update_bookkeeper(db: Session, id: int, item: schemas.BookkeeperCreate):
    bookkeeper = db.query(models.Bookkeeper).get(id)
    if bookkeeper is not None:
        bookkeeper.name = item.name
        bookkeeper.bio = item.bio
        db.commit()
        db.refresh(bookkeeper)
    return bookkeeper

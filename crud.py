#!/usr/bin/env python3

from sqlalchemy.orm import Session

import models
import schema

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

def create_bookkeeper(db: Session, item: schema.BookkeeperCreate):
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
    return False

def update_bookkeeper(db: Session, id: int, item: schema.BookkeeperCreate):
    bookkeeper = db.query(models.Bookkeeper).get(id)
    if bookkeeper is not None:
        bookkeeper.name = item.name
        bookkeeper.bio = item.bio
        db.commit()
        db.refresh(bookkeeper)
        return bookkeeper
    return False

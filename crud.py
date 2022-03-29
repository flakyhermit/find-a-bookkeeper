#!/usr/bin/env python3

from sqlalchemy.orm import Session

import models

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

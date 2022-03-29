#!/usr/bin/env python3

from sqlalchemy.orm import Session

import models

def read_bookkeepers(db: Session, skip: int, limit: int):
    return db.query(models.Bookkeeper).offset(skip).limit(limit).all()

def read_bookkeeper(db: Session, id: int):
    result = db.query(models.Bookkeeper).filter(models.Bookkeeper.id == id).first()
    return result

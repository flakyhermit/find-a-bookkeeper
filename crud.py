#!/usr/bin/env python3

from sqlalchemy import Session

import models

def read_bookkeepers(db: Session, skip: int, limit: int):
    return db.query(models.Bookkeeper).offset(skip).limit(limit).all()

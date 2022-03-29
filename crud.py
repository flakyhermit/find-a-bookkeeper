#!/usr/bin/env python3

from sqlalchemy.orm import Session
from pydantic import BaseModel

from typing import Generic, TypeVar

from db import Base

import models
import schemas

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: ModelType, schema: SchemaType):
        self.model = model
        self.schema = schema

    def get_all(self, db: Session, skip: int, limit: int):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get(self, db: Session, id: int):
        result = db.query(self.model).filter(self.model.id == id).first()
        return result

    def create(self, db: Session, item: SchemaType):
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

    def update(self, db: Session, id: int, item: SchemaType):
        res = db.query(self.model).get(id)
        if res is not None:
            res.name = item.name
            res.bio = item.bio
            db.commit()
            db.refresh(res)
        return res

class CRUDBookkeepers(CRUDBase[models.Bookkeeper, schemas.BookkeeperCreate]):
    def get_by_name(self, db: Session, search: str, skip: int, limit: int):
        result = db.query(self.model).filter(
            self.model.name.like(f'%{search}%')
        ).offset(skip).limit(limit).all()
        return result

bookkeeper = CRUDBookkeepers(models.Bookkeeper, schemas.BookkeeperCreate)

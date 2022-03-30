#!/usr/bin/env python3

from sqlalchemy.orm import Session
from pydantic import BaseModel

from typing import Generic, TypeVar

from db import Base

import models
import schemas

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    def get_all(self, db: Session, skip: int, limit: int):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get(self, db: Session, id: int):
        result = db.query(self.model).filter(self.model.id == id).first()
        return result

    def create(self, db: Session, item: CreateSchemaType):
        res = self.model(**item.dict())
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

    def update(self, db: Session, id: int, item: UpdateSchemaType):
        res = db.query(self.model).get(id)
        if res is not None:
            for key, value in item.dict(exclude_unset = True).items():
                setattr(res, key, value)
            db.commit()
            db.refresh(res)
        return res

class CRUDBookkeeper(CRUDBase[models.Bookkeeper, schemas.BookkeeperCreate, schemas.BookkeeperUpdate]):
    def get_by_name(self, db: Session, search: str, skip: int, limit: int):
        result = db.query(self.model).filter(
            self.model.name.like(f'%{search}%')
        ).offset(skip).limit(limit).all()
        return result

    def get_services(self, db: Session, id: int):
        bookkeeper_obj = db.query(self.model).get(id)
        if bookkeeper_obj is not None:
            services = [i.name for i in bookkeeper_obj.services]
            return services
        return None

    def add_service(self, db: Session, id: int, service_id: int):
        bookkeeper_obj = db.query(self.model).get(id)
        service_obj = db.query(models.Service).get(service_id)
        bookkeeper_obj.services.append(service_obj)
        db.commit()
        db.refresh(bookkeeper_obj)
        return bookkeeper_obj

class CRUDService(CRUDBase[models.Service, schemas.ServiceCreate, schemas.ServiceUpdate]):
    pass

bookkeeper = CRUDBookkeeper(models.Bookkeeper)
service = CRUDService(models.Service)

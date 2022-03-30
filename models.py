#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from db import Base

service_bookkeeper_association_table = Table(
    'service_bookkeeper_association',
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id"), primary_key = True),
    Column("bookkeeper_id", Integer, ForeignKey("bookkeepers.id"), primary_key = True)
)

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))

class Bookkeeper(Base):
    __tablename__ = "bookkeepers"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    bio = Column(String(50))

    services = relationship("Service", secondary = service_bookkeeper_association_table,
                            order_by=Service.id)

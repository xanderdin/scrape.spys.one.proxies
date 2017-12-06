# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Proxy(Base):
    __tablename__ = 'proxies'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String(15))
    port = Column(Integer)


engine = create_engine('sqlite:///proxies.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# -*- coding:utf-8 -*-

from sqlalchemy import Column, Integer, String
from core.base import Model


class User(Model):
    __tablename__ = 'users'

    name = Column(String)
    age = Column(Integer)


    def __repr__(self):
        return '<User %r>' % self.name

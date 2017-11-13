#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from itsdangerous import(TimedJSONWebSignatureSerializer as
                         Serializer, BadSignature, SignatureExpired)
from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    picture = Column(String)
    email = Column(String, index=True)

    @property
    def is_active(self):
        """True, as all users are active."""
        return True

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id':   self.id,
            'name': self.name
            }


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String, ForeignKey('category.name'), nullable=False)
    image = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id':          self.id,
            'name':        self.name,
            'description': self.description,
            'category':    self.category,
            'image':       self.image
            }

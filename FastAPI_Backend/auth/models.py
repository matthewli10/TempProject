from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

"""
This class represents all users in our app. Connects to PostgresSQL
"""
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

"""
This class represents all posts in our app. 
"""
# class Post(Base):
#     __tablename__ = ""








from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, Float, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
import firebase_admin 
from firebase import credentials, firestone



Base = declarative_base()

"""
This class represents all users in our app. Connects to PostgresSQL
"""
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable = False)
    hashed_password = Column(String, nullable = False)
    is_verified = Column(Boolean, default = False)



"""
This class represents all posts in our app. 
"""
# class Post(Base):
#     __tablename__ = ""

# class Account(Base):
#     __tablename__ = ""






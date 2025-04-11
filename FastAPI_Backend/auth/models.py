from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID 
import uuid
from datetime import datetime

"""
This class represents all users in our app. Connects to PostgresSQL
"""
class User(Base):
    __tablename__ = ""


"""
This class represents all posts in our app. 
"""
class Post(Base):
    __tablename__ = ""

class 





from .database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
  __tablename__ = 'users'

  userid = Column(Integer, primary_key=True)
  password = Column(String)
  username = Column(String, unique=True)


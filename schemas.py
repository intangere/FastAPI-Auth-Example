from pydantic import BaseModel
from typing import Union

class UserBase(BaseModel):
  username: str

class UserCreate(UserBase):
  password: str

class User(UserBase):

  class Config:
    orm_mode = True

class UserIn(UserCreate):
  ...

class UserOut(User):
  token: str

class Response(BaseModel):
  status: str
  reason: str
  data: Union[list,dict,UserOut] = {}

class Payload(BaseModel):
  username: str

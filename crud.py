from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hash_password

def get_user(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = hash_password(user.password.encode())
  db_user = models.User(username = user.username,
                        password = hashed_password)

  db.add(db_user)
  db.commit()
  db.refresh(db_user)

  return db_user


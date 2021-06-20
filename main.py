from typing import Callable
from sqlalchemy.orm import Session
from fastapi import FastAPI, Body, Request, Response, Depends
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from .database import SessionLocal, engine
from .responses import MsgpackResponse
from . import models, crud, schemas
from .constants import *
from .utils import *
from .config import USE_MSGPACK
import msgpack

models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MsgpackRequest(Request):
  async def body(self) -> bytes:
    if not hasattr(self, '_body'):
      raw_body = await super().body()
      body = b''

      if 'application/x-msgpack' in self.headers.getlist('Content-Type'):
        try:
          body = msgpack.unpackb(raw_body, raw=False)
        except Exception as e:
          pass

      self._body = body

    return self._body

class MsgpackRoute(APIRoute):
  def get_route_handler(self) -> Callable:
    original_route_handler = super().get_route_handler()

    async def custom_route_handler(request: Request) -> Response:
      request = MsgpackRequest(request.scope, request.receive)
      return await original_route_handler(request)

    return custom_route_handler

if USE_MSGPACK:
  app = FastAPI(default_response_class=MsgpackResponse)
  app.router.route_class = MsgpackRoute
else:
  app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)):

  payload = decode_token(token)

  if not payload:
    return

  db_user = crud.get_user(db, username = payload.username)

  return schemas.User.from_orm(db_user)

@app.get('/')
async def index():
  return {'Welcome': 'Boards API'}

@app.post('/login')
async def login(user: schemas.UserIn,
                db: Session = Depends(get_db)):

  db_user = crud.get_user(db, username = user.username)

  if db_user is None:
    return schemas.Response(status = FAILED, reason = USER_NOT_FOUND)

  if not verify_password(user.password.encode(), db_user.password):
    return schemas.Response(status = FAILED, reason = BAD_PASSWORD)

  user_data = schemas.User.from_orm(db_user).dict()
  user_data.update({'token': create_token(db_user.username)})

  user = schemas.UserOut(**user_data)

  return schemas.Response(status = SUCCESS, reason=LOGGED_IN, data=user)

@app.post('/create_user')
async def create_user(user: schemas.UserCreate,
                      db: Session = Depends(get_db)):

  db_user = crud.get_user(db, username = user.username)

  if db_user:
    return schemas.Response(status = FAILED, reason = USERNAME_TAKEN)

  if not check_password(user.password):
    return schemas.Response(status = FAILED, reason = PASSWORD_REQ)

  if crud.create_user(db, user):
    return schemas.Response(status = SUCCESS, reason = USER_CREATED)

  return schemas.Response(status = FAILED, reason = '')

@app.get('/test')
async def auth_test(user: schemas.User = Depends(get_current_user)):
  return schemas.Response(status = SUCCESS, reason = 'You are authenticated as %s' % user.username)

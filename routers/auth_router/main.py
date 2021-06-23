from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt

from datetime import timedelta

from main import get_db,oauth2_scheme
import utils

router = APIRouter()

access_token_expires = timedelta(minutes=30)

@router.post("/authenticate")
async def authenticate(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    user = await crud.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException( status_code=404, detail="user not found")
    if await crud.verify_password(db, payload.password, user.password):
        access_token = utils.create_access_token(data = payload.dict(), expires_delta=access_token_expires)
        return {'access_token': access_token, "token_type": "Bearer"}
    raise HTTPException( status_code=404, detail="Something went wrong make sure you have entered the right credentials")

#token verification
@router.get("/current_user")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), payload : dict = Depends(utils.verify_token) ):
    try:
        if payload:
            del payload['exp']
            return payload
        raise  HTTPException( status_code=400, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.exceptions.DecodeError as e:
        raise HTTPException( status_code=500, detail="decode error not enough segments", headers={"WWW-Authenticate": "Bearer"})

@router.get("/")
async def read_users(skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.get_users(db,skip,limit,search,value)

@router.get("/{id}")
async def read_user(id: int, db: Session = Depends(get_db)):
    return await crud.get_user(db, id)
     
@router.post("/create")
async def create_users(user:schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(user,db)

@router.delete("/delete/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    return await crud.delete_user(db, id)

@router.put("/update/{id}")
async def update_user(id: int, payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return await crud.update_user(db,id,payload)

@router.get("/protected/{id}")
async def test(id: Optional[int] = 1, is_authenticated : bool = Depends(utils.verify_token) ):
    from datetime import datetime,timedelta
    print(datetime.utcnow()+timedelta(days=100))
    # a = datetime.utcnow() + timedelta(minutes=15)
    if not is_authenticated:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})
    return id


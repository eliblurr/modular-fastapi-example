from sqlalchemy.orm import Session
from fastapi import Depends

from . import models, schemas

async def create_user( user: schemas.UserCreate , db: Session):
    new_user = models.User(email=user.email, password=models.User.generate_hash(user.password))
    db.add(new_user)
    db.commit()
    return 'success',200

async def get_users(db: Session, skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    base = db.query(models.User)
    if search and value:
        try:
            base = base.filter(models.User.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

async def verify_password(db: Session, password: str, hashed_password):
    return models.User.verify_hash(password, hashed_password)

async def delete_user(db: Session,id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return 'user not found'
    db.delete(user)
    db.commit()
    return 'success'

async def update_user(db: Session, id: int, payload: schemas.UserCreate):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return 'user not found'
    res = db.query(models.User).filter(models.User.id == id).update(payload)
    db.commit()
    return res



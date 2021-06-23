from sqlalchemy.orm import Session
from fastapi import Depends

from . import models, schemas

async def create_item( db: Session, item: schemas.Item ):
    item = models.Item(title=item.title, description=item.description)
    db.add(item)
    db.commit()
    return item
    
async def get_items(db: Session, skip: int = 0, limit: int = 100, search:str=None, value:str=None):
    base = db.query(models.Item)
    if search and value:
        # print(search)
        try:
            base = base.filter(models.Item.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


async def delete_item(db: Session, id: int):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        return 'item not found'
    db.delete(item)
    db.commit()
    return 'success',200

async def update_item(db: Session, id: int, payload: schemas.ItemUpdate):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        return 'item not found'
    res = db.query(models.Item).filter(models.Item.id == id).update(payload)
    db.commit()
    return res



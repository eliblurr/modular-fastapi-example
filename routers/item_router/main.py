from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List, Optional
from pydantic import UUID4, EmailStr
from typing import List, Optional

from main import get_db

router = APIRouter()

@router.get("/")
async def read_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:Optional[str] = None, value:Optional[str] = None):
    print(search)
    print(value)
    return await crud.get_items(db,skip,limit,search,value)

@router.get("/{id}")
async def read_item(id: int, db: Session = Depends(get_db)):
    return await crud.get_item(db, id)
     
@router.post("/create")
async def create_item(item:schemas.ItemCreate, db: Session = Depends(get_db)):
    item =  await crud.create_item(db, item)
    if item:
        return 'success',200
    raise HTTPException(status_code=400, detail="failed to add item")
    

@router.delete("/delete/{id}")
async def delete_item(id: int, db: Session = Depends(get_db)):
    return await crud.delete_item(db, id)

@router.put("/update/{id}")
async def update_item(id: int, payload: schemas.ItemUpdate, db: Session = Depends(get_db)):
    print(payload)
    return await crud.update_item(db,id,payload)


from typing import List, Optional

from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str

class ItemUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

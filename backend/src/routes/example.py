from fastapi import APIRouter, HTTPException
from config.database import Database
from models.base import DBModelBase
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Item(DBModelBase):
    name: str
    description: str

@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    db = Database.client[DATABASE_NAME]
    result = await db.items.insert_one(item.dict(by_alias=True))
    created_item = await db.items.find_one({"_id": result.inserted_id})
    return Item(**created_item)

@router.get("/items/", response_model=List[Item])
async def get_items():
    db = Database.client[DATABASE_NAME]
    items = await db.items.find().to_list(1000)
    return [Item(**item) for item in items] 
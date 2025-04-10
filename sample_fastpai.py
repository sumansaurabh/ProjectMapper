from fastapi import FastAPI, HTTPException, Depends, Query, Path, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import List, Optional
from projectmapper import map_project

app = FastAPI(
    title="Sample FastAPI Server",
    description="A demonstration of FastAPI features",
    version="0.1.0"
)

# Initialize the project mapper
mapper = map_project(app, base_path="/api")

# Pydantic models for request and response
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_offer: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Example Item",
                "description": "This is an example item",
                "price": 35.4,
                "is_offer": True
            }
        }

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_offer: bool = False

# Simulate a database with a simple list
items_db = [
    Item(id=1, name="Item 1", description="Description 1", price=10.5, is_offer=False),
    Item(id=2, name="Item 2", description="Description 2", price=20.0, is_offer=True),
]

# Basic auth for demonstration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # This is just a simple demo - in a real app, you'd validate the token
    return {"username": "demo_user"}

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Welcome to the sample FastAPI server"}

# Get all items
@app.get("/items/", response_model=List[Item], tags=["items"])
def read_items(skip: int = Query(0, description="Number of items to skip"),
               limit: int = Query(10, description="Maximum number of items to return")):
    return items_db[skip:skip+limit]

# Get a specific item by ID
@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def read_item(item_id: int = Path(..., title="The ID of the item to get")):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Create a new item
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(item: ItemCreate):
    new_id = max(item.id for item in items_db) + 1 if items_db else 1
    new_item = Item(id=new_id, **item.dict())
    items_db.append(new_item)
    return new_item

# Update an item
@app.put("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, item: ItemCreate):
    for idx, stored_item in enumerate(items_db):
        if stored_item.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            items_db[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int):
    for idx, stored_item in enumerate(items_db):
        if stored_item.id == item_id:
            items_db.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Item not found")

# Protected endpoint example
@app.get("/protected/", tags=["protected"])
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user["username"]}

# Run with: uvicorn sample_fastpai:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sample_fastpai:app", host="0.0.0.0", port=9000, reload=True)
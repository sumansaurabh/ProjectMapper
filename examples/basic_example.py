from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from projectmapper import map_project

# Create FastAPI application
app = FastAPI(title="Example API")

# Initialize ProjectMapper
mapper = map_project(app)

# Define some models
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

class User(BaseModel):
    id: int
    username: str
    email: str
    
# Define some dependencies
def get_current_user():
    return {"id": 1, "username": "testuser"}

def verify_token(token: str = None):
    if token != "valid_token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

# Define routes
@app.get("/", tags=["root"])
def read_root():
    """Return welcome message."""
    return {"message": "Welcome to Example API"}

@app.get("/items/", response_model=List[Item], tags=["items"])
def list_items(current_user = Depends(get_current_user)):
    """List all items."""
    return [
        Item(id=1, name="Item 1", description="This is item 1", price=10.5),
        Item(id=2, name="Item 2", price=20.0)
    ]

@app.post("/items/", response_model=Item, tags=["items"])
def create_item(item: Item, token: str = Depends(verify_token)):
    """Create a new item."""
    return item

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int, current_user = Depends(get_current_user)):
    """Get item by ID."""
    return Item(id=item_id, name=f"Item {item_id}", price=10.0)

@app.get("/users/", response_model=List[User], tags=["users"])
def list_users():
    """List all users."""
    return [
        User(id=1, username="user1", email="user1@example.com"),
        User(id=2, username="user2", email="user2@example.com")
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

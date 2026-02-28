from pydantic import BaseModel, Field
from datetime import date

class ExpenseBase(BaseModel):
    description: str
    amount: int = Field(..., ge=0)
    
class ExpenseCreate(ExpenseBase):
    category: str | None = None
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    date: date
    category: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    name: str | None = None
    password: str
    
class UserResponse(UserBase):
    name: str
    id: int

    class Config:
        from_attributes = True
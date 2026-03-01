from pydantic import BaseModel, Field
from datetime import date
from models import CategoryEnum

class ExpenseBase(BaseModel):
    description: str
    amount: int = Field(..., ge=0)
    category: CategoryEnum
    
class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    date: date

    class Config:
        from_attributes = True

class ExpensePatch(BaseModel):
    description: str | None = None
    amount: int | None = Field(None, ge=0)
    category: CategoryEnum | None = None

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
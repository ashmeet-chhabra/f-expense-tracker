from pydantic import BaseModel, Field, ConfigDict
from datetime import date

from app.models import CategoryEnum

class ExpenseBase(BaseModel):
    description: str
    amount: int = Field(..., ge=0)
    category: CategoryEnum
    
class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    date: date
    
    model_config = ConfigDict(from_attributes = True) 
    
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

    model_config = ConfigDict(from_attributes = True) 

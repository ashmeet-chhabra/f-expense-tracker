from pydantic import BaseModel, Field
from datetime import date

class ExpenseBase(BaseModel):
    description: str
    amount: int = Field(..., ge=0)

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    date: date

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str | None = None
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
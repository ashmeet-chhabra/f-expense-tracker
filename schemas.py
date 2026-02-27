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
        orm_mode = True
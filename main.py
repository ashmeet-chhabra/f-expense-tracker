from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field
from datetime import datetime
from datetime import date
from typing import List
import json
import os

FILE_NAME = 'data.json'

class ExpenseCreate(BaseModel):
    description: str
    amount: int = Field(..., ge=0)

class Expense(BaseModel):
    id: int
    description: str
    amount: int
    date: str

app = FastAPI()

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, 'r') as f:
        try:
            expenses = json.load(f)
            return expenses
        except json.JSONDecodeError:
            return []

def save_expenses(expenses):
    with open(FILE_NAME, 'w') as f:
        json.dump(expenses, f, indent=4)

def get_next_id(expenses):
    if not expenses:
        return 1
    next_id = max(expense['id'] for expense in expenses) + 1
    return next_id

@app.get('/')
def root():
    return {'message': 'Expense Tracker API is running'}

@app.get('/expenses', response_model=List[Expense])
def list_expenses():
    return load_expenses()

@app.get('/summary')
def summarize_expenses(month: int | None=None):
    expenses = load_expenses()
    if month is not None:
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail='Month must be between 1 and 12')
        filtered_total = sum(
            expense['amount']
            for expense in expenses
            if date.fromisoformat(expense['date']).month == month
        )
        return {'month': month, 'total': filtered_total}
    else:
        total_expense = sum(expense['amount'] for expense in expenses)
        return {'total': total_expense}

@app.post('/expenses', response_model=Expense, status_code=201)
def add_expense(expense: ExpenseCreate):    
    expenses = load_expenses()
    expense_id = get_next_id(expenses)

    new_expense = {
        "id": expense_id,
        "description": expense.description,
        "amount": expense.amount,
        "date": str(datetime.now().date())
    }

    expenses.append(new_expense)
    save_expenses(expenses)

    return new_expense

@app.delete('/expenses/{expense_id}', status_code=204)
def delete_expense(expense_id: int):
    expenses = load_expenses()
    for expense in expenses:
        if expense['id'] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            return
    raise HTTPException(status_code=404, detail='Expense not found')

@app.patch('/expenses/{expense_id}', response_model=Expense)
def update_expense(expense_id: int, expense: ExpenseCreate):
    expenses = load_expenses()
    for e in expenses:
        if e['id'] == expense_id:
            e['description'] = expense.description
            e['amount'] = expense.amount
            save_expenses(expenses)
            return e
    raise HTTPException(status_code=404, detail='Expense not found')
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field
from datetime import datetime
from datetime import date
from typing import List
import json
import os
from database import init_db, get_connection

class ExpenseCreate(BaseModel):
    description: str
    amount: int = Field(..., ge=0)

class Expense(BaseModel):
    id: int
    description: str
    amount: int
    date: str

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

def fetch_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.get('/')
def root():
    return {'message': 'Expense Tracker API is running'}

@app.get('/expenses', response_model=List[Expense])
def list_expenses():
    return fetch_all_expenses()

@app.get('/summary')
def summarize_expenses(month: int | None=None):
    expenses = fetch_all_expenses()
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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (description, amount, date) VALUES (?, ?, DATE('now))",
        (expense.description, expense.amount)
    )

    conn.commit()

    expense_id = cursor.lastrowid

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id))
    row = cursor.fetchone()

    conn.close()
    
    return dict(row)

@app.delete('/expenses/{expense_id}', status_code=204)
def delete_expense(expense_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE ? = expense_id", expense_id)
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, details="Expense not found")

    conn.close()

@app.patch('/expenses/{expense_id}', response_model=Expense)
#replace patch
def update_expense(expense_id: int, expense: ExpenseCreate):
    conn = get_connection()
    cur = conn.cur()

    cur.execute("UPDATE expenses SET description = ?, amount = ? WHERE id = ?",
                (expense.description, expense.amount, expense_id)
    )
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Expense not found')
    
    cur.execute("SELECT * FROM expenses WHERE ? = expense_id", expense_id)
    row = cur.fetchone()
    
    conn.close()

    return dict(row)
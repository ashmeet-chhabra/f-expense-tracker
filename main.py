from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pydantic import Field
from typing import List
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
def summarize_expenses(month: int | None = Query(None, ge=1, le=12)):

    conn = get_connection()
    cur = conn.cursor()

    if month is not None:
        cur.execute(
            """
            SELECT SUM(amount) AS total
            FROM expenses
            WHERE strftime('%m', date) = ?
            """,
            (f'{month:02d}',)
        )
    else:
        cur.execute("SELECT SUM(amount) AS total FROM expenses")

    row = cur.fetchone()
    conn.close()

    total = row["total"] if row["total"] is not None else 0

    return {"month": month, "total": total} if month is not None else {"total": total}

@app.post('/expenses', response_model=Expense, status_code=201)
def add_expense(expense: ExpenseCreate):    

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (description, amount, date) VALUES (?, ?, DATE('now'))",
        (expense.description, expense.amount)
    )

    conn.commit()

    expense_id = cursor.lastrowid

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cursor.fetchone()

    conn.close()
    
    return dict(row)

@app.delete('/expenses/{expense_id}', status_code=204)
def delete_expense(expense_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")

    conn.close()

@app.patch('/expenses/{expense_id}', response_model=Expense)
#replace patch
def update_expense(expense_id: int, expense: ExpenseCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE expenses SET description = ?, amount = ? WHERE id = ?",
                (expense.description, expense.amount, expense_id)
    )
    conn.commit()

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail='Expense not found')
    
    cur.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    row = cur.fetchone()
    
    conn.close()

    return dict(row)
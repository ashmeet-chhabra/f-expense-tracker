from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import ExpenseModel, UserModel
from schemas import ExpenseCreate, ExpenseResponse
from deps import get_current_user 

router = APIRouter(
    prefix = "/expenses",
    tags = ["Expenses"]
)

@router.get('/', response_model=List[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return db.query(ExpenseModel).filter(
        ExpenseModel.user_id == current_user.id
    ).all()

# protect routes
@router.get('/summary')
def summarize_expenses(month: int | None = Query(None, ge=1, le=12), db: Session = Depends(get_db)):

    if month is not None:
        total = (
            db.query(func.sum(ExpenseModel.amount))
                .filter(extract('month', ExpenseModel.date) == month)
                .scalar()
        )
    else:
        total = db.query(func.sum(ExpenseModel.amount)).scalar()

    total = total or 0

    return {"month": month, "total": total} if month is not None else {"total": total}

@router.post('/', response_model=ExpenseResponse, status_code=201)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):    

    db_expense = ExpenseModel(
         description = expense.description,
         amount = expense.amount
         user_id = current_user.id
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)    

    return db_expense

@router.delete('/{expense_id}', status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):

    expense = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

@router.patch('/{expense_id}', response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db)):
    
    db_expense = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id
    ).first()

    if not db_expense:
        raise HTTPException(status_code=404, detail='Expense not found')
    
    db_expense.description = expense.description
    db_expense.amount = expense.amount

    db.commit()
    db.refresh(db_expense)

    return db_expense
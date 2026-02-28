from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta, timezone

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
    date_filter: str | None = None,
    start: date | None = None,
    end: date | None = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    
    query = db.query(ExpenseModel).filter(
            ExpenseModel.user_id == current_user.id
        )
    
    if date_filter:
        end = date.today()
        match date_filter:
            case 'week': 
                start = end - timedelta(days=7)
            case 'month':
                start = end - timedelta(days=30)
            case '3months':
                start = end - timedelta(days=90)
            case _: raise HTTPException(status_code=400, detail="Invalid date filter value")

    if start and end:
        query = query.filter(
            ExpenseModel.date <= end,
            ExpenseModel.date >= start
        )

    return query.all()

@router.get('/summary')
def summarize_expenses(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if month is not None:
        total = (
            db.query(func.sum(ExpenseModel.amount))
            .filter(
                ExpenseModel.user_id == current_user.id,
                extract('month', ExpenseModel.date) == month
            )
            .scalar()
        )
    else:
        total = (
            db.query(func.sum(ExpenseModel.amount))
            .filter(ExpenseModel.user_id == current_user.id)
            .scalar()
        )

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
         amount = expense.amount,
         user_id = current_user.id
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)    

    return db_expense

@router.delete('/{expense_id}', status_code=204)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):

    expense = db.query(ExpenseModel).filter(
        ExpenseModel.user_id == current_user.id,
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
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    
    db_expense = db.query(ExpenseModel).filter(
        ExpenseModel.user_id  == current_user.id,
        ExpenseModel.id == expense_id
    ).first()

    if not db_expense:
        raise HTTPException(status_code=404, detail='Expense not found')
    
    db_expense.description = expense.description
    db_expense.amount = expense.amount

    db.commit()
    db.refresh(db_expense)

    return db_expense
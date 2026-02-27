from sqlalchemy import Column, Integer, String, Date
from datetime import date

from database import Base

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(Date, default=date.today)


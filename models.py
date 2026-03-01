from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import date
from enum import Enum

from database import Base

class CategoryEnum(str, Enum):
    groceries = "Groceries"
    leisure = "Leisure"
    electronics = "Electronics"
    utilities = "Utilities"
    clothing = "Clothing"
    health = "Health"
    others = "Others"

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(Date, default=date.today)
    category = Column(SqlEnum(CategoryEnum), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="expenses")

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Guest")
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    expenses = relationship("ExpenseModel", back_populates="user")
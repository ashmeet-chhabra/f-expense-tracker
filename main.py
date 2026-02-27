from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import engine, Base
from routers import expenses

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(expenses.router)

@app.get('/')
def root():
    return {'message': 'Expense Tracker API is running'}
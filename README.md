# Expense Tracker API

A secure, multi-user Expense Tracker API built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**.

This project is based on the Backend roadmap project from roadmap.sh:

🔗 https://roadmap.sh/projects/expense-tracker-api

It implements a fully authenticated REST API that allows users to manage their personal expenses with filtering and categorization support.

---

## Features

### Authentication
- User registration
- Secure password hashing (bcrypt)
- JWT-based login
- Protected routes using Bearer tokens
- Per-user data isolation

### Expense Management
- Create a new expense
- View all your expenses
- Update an existing expense
- Delete an expense
- View expense summary

### Date Filtering
Filter expenses by:
- Past week
- Past month
- Last 3 months
- Custom date range (`start` and `end`)
- Open-ended ranges (only `start` or only `end`)

### Categories

Each expense must belong to one of the following categories:

- Groceries
- Leisure
- Electronics
- Utilities
- Clothing
- Health
- Others

Categories are strictly validated via Enum.

---

## Tech Stack

- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Passlib (bcrypt)**
- **python-jose (JWT)**
- **OAuth2PasswordBearer**

---

## Project Structure

```
.
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── deps.py
├── routers/
│   ├── expenses.py
│   └── users.py
├── requirements.txt
└── README.md
```

---

## Setup & Run Instructions

###  Clone the repository

```bash
git clone https://github.com/ashmeet-chhabra/f-expense-tracker
cd f-expense-tracker
```

###  Create and activate virtual environment

```bash
python -m venv venv
```

#### Windows
```bash
venv\Scripts\activate
```

#### macOS/Linux
```bash
source venv/bin/activate
```

###  Install dependencies

```bash
pip install -r requirements.txt
```

###  (Optional but Recommended) Set Environment Variable

By default, the app uses a development secret key.

#### Windows (PowerShell)
```bash
setx SECRET_KEY "your-super-secret-key"
```

#### macOS/Linux
```bash
export SECRET_KEY="your-super-secret-key"
```

###  Run the server

```bash
uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Authentication Flow

### Register

**POST** `/users/register`

```json
{
  "name": "John",
  "email": "john@example.com",
  "password": "secret123"
}
```

---

### Login

**POST** `/users/login`

Uses `application/x-www-form-urlencoded`:

- `username` = email  
- `password` = password  

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Use the token in headers:

```
Authorization: Bearer <token>
```

---

## Expense Endpoints

### Create Expense

**POST** `/expenses`

```json
{
  "description": "Groceries from store",
  "amount": 500,
  "category": "Groceries"
}
```

---

### List Expenses

**GET** `/expenses`

---

### Date Filters

Predefined:

```
GET /expenses?date_filter=week
GET /expenses?date_filter=month
GET /expenses?date_filter=3months
```

Custom range:

```
GET /expenses?start=2025-01-01&end=2025-01-30
```

Open-ended:

```
GET /expenses?start=2025-01-01
GET /expenses?end=2025-01-30
```

---

### Filter by Category

```
GET /expenses?category=Groceries
```

---

### Update Expense

**PATCH** `/expenses/{expense_id}`

---

### Delete Expense

**DELETE** `/expenses/{expense_id}`

---

## Security Design

- Passwords are hashed using bcrypt.
- JWT tokens include expiration.
- All expense routes require authentication.
- Users can only access their own expenses.
- Ownership is enforced at the database query level.

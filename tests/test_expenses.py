def test_protected_route_requires_auth(client):
    response = client.get('/expenses')
    assert response.status_code == 401
    
def test_list_expenses_authenticated(auth_client):
    response = auth_client.get('/expenses')
    assert response.status_code == 200
    assert response.json() == []

def test_add_expense(auth_client):
    expense = {
        "description": "Test description",
        "amount": 100,
        "category": "Health"
    }
    response = auth_client.post('/expenses', json=expense)
    data = response.json()

    assert response.status_code == 201
    assert data["description"] == "Test description"
    assert data["amount"] == 100
    assert data["category"] == "Health"
    assert "id" in data
    assert "date" in data

def test_expense_is_in_list(auth_client):
    expense = {
        "description": "Test description",
        "amount": 100,
        "category": "Health"
    }
    auth_client.post('/expenses', json=expense)
    response = auth_client.get('/expenses')
    data = response.json()
    expense_response = data[0]
    assert response.status_code == 200
    assert len(data) == 1
    assert expense_response["description"] == "Test description"
    assert expense_response["amount"] == 100
    assert expense_response["category"] =="Health"

def test_users_cannot_see_each_others_expenses(client):
    user1 = {"name":"Test1","email":"Test123@gmail.com","password":"Test111"}
    client.post("/users/register", json=user1)

    user1 = {"username":"Test123@gmail.com","password":"Test111"}
    response = client.post("/users/login", data=user1)

    access_token1 = response.json()['access_token']

    client.headers.update({
        "Authorization": f"Bearer {access_token1}"
    })

    expense = {
        "description": "User1 expense",
        "amount": 100,
        "category": "Groceries"
    }

    client.post('/expenses', json=expense)
    client.headers.clear()

    user2 = {"name":"Test2","email":"Test321@gmail.com","password":"Test222"}
    client.post("/users/register", json=user2)

    user2 = {"username":"Test321@gmail.com","password":"Test222"}
    response = client.post("/users/login", data=user2)

    access_token2 = response.json()['access_token']

    client.headers.update({
        "Authorization": f"Bearer {access_token2}"
    })

    response = client.get('/expenses')
    assert response.json() == []

def test_delete_expense(auth_client):
    expense = {
        "description": "Test description",
        "amount": 100,
        "category": "Health"
    }
    id = auth_client.post('/expenses', json=expense).json()["id"]

    response = auth_client.delete(f'/expenses/{id}')
    assert response.status_code == 204
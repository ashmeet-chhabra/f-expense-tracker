def test_protected_route_requires_auth(client):
    response = client.get('/expenses')
    assert response.status_code == 401
    
def test_list_expenses_authenticated(auth_client):
    response = auth_client.get('/expenses')
    assert response.status_code == 200
    assert response.json() == []

def test_add_expense(auth_client):
    pass
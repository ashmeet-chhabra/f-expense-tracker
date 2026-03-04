def test_register_user(client):
    user = {"name":"Test","email":"Test123@gmail.com","password":"Test111"}
    response = client.post("/users/register", json=user)
    data = response.json()

    assert response.status_code == 201
    assert data["email"] == user["email"]
    assert data["name"] == user["name"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data

def test_duplicate_registration(client):
    user = {"name":"Test","email":"Test123@gmail.com","password":"Test111"}
    client.post("/users/register", json=user)
    response = client.post("/users/register", json=user)

    assert response.status_code == 400
    assert response.json()['detail'] == "Email already registered"
    
def test_login_success(client):
    user = {"name":"Test","email":"Test123@gmail.com","password":"Test111"}
    client.post("/users/register", json=user)

    user = {"username":"Test123@gmail.com","password":"Test111"}
    response = client.post("/users/login", data=user)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
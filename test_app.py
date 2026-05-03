import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_get_students(client):
    response = client.get('/api/students')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_get_student_not_found(client):
    response = client.get('/api/students/9999')
    assert response.status_code == 404

def test_add_student(client):
    new_student = {'name': 'Memoona', 'grade': 'A'}
    response = client.post('/api/students', json=new_student)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Memoona'

def test_add_student_missing_field(client):
    response = client.post('/api/students', json={'name': 'Sara'})
    assert response.status_code == 400
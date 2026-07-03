import pytest
import json
import os
from app.app import app, TASKS_FILE

@pytest.fixture
def client():
    app.config["TESTING"] = True
    
    # Ensure starting with a clean state
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
        
    with app.test_client() as client:
        yield client
        
    # Cleanup after tests
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"DevOps Todo" in response.data

def test_add_task(client):
    response = client.post("/tasks", 
                          json={"title": "Test DevOps Pipeline"},
                          content_type="application/json")
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Test DevOps Pipeline"
    assert data["completed"] is False
    assert "id" in data

def test_add_empty_task(client):
    response = client.post("/tasks", 
                          json={"title": "   "},
                          content_type="application/json")
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_delete_task(client):
    # First add a task
    post_res = client.post("/tasks", json={"title": "To be deleted"})
    task_id = json.loads(post_res.data)["id"]
    
    # Then delete it
    del_res = client.delete(f"/tasks/{task_id}")
    assert del_res.status_code == 200
    
    # Verify it's gone
    get_res = client.get("/tasks")
    tasks = json.loads(get_res.data)
    assert len(tasks) == 0

def test_complete_task(client):
    # First add a task
    post_res = client.post("/tasks", json={"title": "To be completed"})
    task_id = json.loads(post_res.data)["id"]
    
    # Toggle it
    patch_res = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert patch_res.status_code == 200
    data = json.loads(patch_res.data)
    assert data["completed"] is True

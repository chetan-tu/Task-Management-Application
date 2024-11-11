from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from apps.main import app

client = TestClient(app)

# Sample data for creating a task
sample_task = {
    "title": "Sample Task",
    "description": "A test description",
    "status": "Open"
}
# Sample data for updating a task
updated_task_data = {
    "title": "Updated Task",
    "description": "An updated description",
    "status": "In Progress"
}

@pytest.fixture
def create_task():
    """Fixture to create a task for testing."""
    response = client.post("/tasks/", json=sample_task)
    assert response.status_code == 201
    return response.json()

# End-to-End Workflow Test
def test_end_to_end_task_lifecycle():
    # Creating a task
    response = client.post("/tasks/", json=sample_task)
    assert response.status_code == 201
    task = response.json()
    task_id = task["id"]

    # Updating the Task
    response = client.put(f"/tasks/{task_id}", json=updated_task_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == updated_task_data["title"]

    #Retrieving the Updated Task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["status"] == "In Progress"  # Confirm retrieved status

    #Deleting the Task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Confirming task deletion by 404 Not found
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

# Additional tests
#Testing fetching a task from empty database
def test_get_task_empty_database():
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    
#testing deleting a task from empty database
def test_delete_task_empty_database():
    response = client.delete("/tasks/9999")
    assert response.status_code == 404

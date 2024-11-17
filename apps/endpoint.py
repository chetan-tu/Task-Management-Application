from typing import List
from .model import Task,TaskResponse
from .database import get_connection
from fastapi import HTTPException, Path, status,APIRouter
from datetime import datetime

conn = get_connection()
cursor = conn.cursor()

router = APIRouter(prefix= "/tasks",tags=['Tasks'])

#Endpoint to read all tasks
@router.get("/", description="Endpoint to read all tasks",status_code=status.HTTP_200_OK, response_model=List[TaskResponse])
def read_all_tasks():
    cursor.execute("SELECT * FROM task")
    tasks = cursor.fetchall()
    
    tasks_list = [
        {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "status": task["status"],
            "created_at": task["created_at"],
            "updated_at": task["updated_at"]
        }
        for task in tasks
    ]
    
    return tasks_list

# Endpoint to create a new task
@router.post("/",description="Endpoint to create a task",status_code=status.HTTP_201_CREATED,response_model=TaskResponse,responses={
        201: {
            "description": "Task created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Sample Task",
                        "description": "Detailed description of the task",
                        "status": "Open",
                        "createdAt": "2024-11-09T15:04:45.504965",
                        "updatedAt": "2024-11-09T15:04:45.504965"
                    }
                }
            }
        },
        422: {
            "description": "Validation Error - Check input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "title"],
                                "msg": "Field required",
                                "type": "value_error.missing"
                            },
                            {
                                "loc": ["body", "status"],
                                "msg": "Invalid status provided",
                                "type": "type_error.enum"
                            }
                        ]
                    }
                }
            }
        }
    })
def create_task(task: Task):
    cursor.execute(
        """
        INSERT INTO task (title, description, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
        """,
        (task.title, task.description, task.status, datetime.now(), datetime.now())
    )
    new_task = cursor.fetchone()
    conn.commit()
    return new_task

# Endpoint to retrieve a single task by ID
@router.get("/{id}",description="Endpoint to retrieve a single task by ID",response_model=TaskResponse,status_code=status.HTTP_200_OK,responses={
        200: {
            "description": "Task retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Sample Task",
                        "description": "Detailed description of the task",
                        "status": "Open",
                        "createdAt": "2024-11-09T15:04:45.504965",
                        "updatedAt": "2024-11-09T15:04:45.504965"
                    }
                }
            }
        },
        404: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Task with ID 1 not found"}
                }
            }
        },
        422: {
            "description": "Validation Error - Check input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }
    })
def read_task(id: int = Path(..., description="The ID of the task to be deleted", example=1)):
    cursor.execute("SELECT * FROM task WHERE id = %s", (id,))
    task = cursor.fetchone()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    return task

# Endpoint to update a task by ID
@router.put("/{id}",description="Endpoint to update a single task by ID",response_model=TaskResponse,status_code=status.HTTP_200_OK,responses={
        200: {
            "description": "Task updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Updated Task Title",
                        "description": "Updated task description",
                        "status": "In Progress",
                        "createdAt": "2024-11-09T15:04:45.504965",
                        "updatedAt": "2024-11-10T16:10:23.504965"
                    }
                }
            }
        },
        404: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Task with ID 1 not found"}
                }
            }
        },
        422: {
            "description": "Validation Error - Check input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            },
                            {
                                "loc": ["body", "status"],
                                "msg": "Invalid status provided",
                                "type": "type_error.enum"
                            }
                        ]
                    }
                }
            }
        }
    })
def update_task(task: Task, id: int = Path(..., description="The ID of the task to be deleted", example=1)):
    cursor.execute(
        """
        UPDATE task
        SET title = %s, description = %s, status = %s, updated_at = %s
        WHERE id = %s RETURNING *;
        """,
        (task.title, task.description, task.status, datetime.now(), id)
    )
    updated_task = cursor.fetchone()
    conn.commit()
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    return updated_task

# Endpoint to delete a task by ID
@router.delete("/{id}",description="Endpoint to delete a single task by ID",status_code=status.HTTP_204_NO_CONTENT,responses={
        204: {
            "description": "Task deleted successfully"
        },
        404: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Task with ID 1 not found"}
                }
            }
        }
    ,
        422: {
            "description": "Validation Error - Check input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["path", "id"],
                                "msg": "value is not a valid integer",
                                "type": "type_error.integer"
                            }
                        ]
                    }
                }
            }
        }}
    )
def delete_task(id: int = Path(..., description="The ID of the task to be deleted", example=1)):
    cursor.execute("DELETE FROM task WHERE id = %s RETURNING *", (id,))
    deleted_task = cursor.fetchone()
    conn.commit()
    if not deleted_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    return {"message": f"Task with ID {id} deleted successfully"}

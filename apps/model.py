from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"

class Task(BaseModel):
    id: Optional[int] = Field(None, example=1) 
    title: str = Field(..., min_length=1, example="My Task Title")
    description: Optional[str] = Field("No Description provided", example="Detailed description of the task")
    status: Optional[TaskStatus] = Field("In Progress", example="Open")
    created_at: Optional[datetime] = Field(None, example="2024-11-09 15:04:45.504965")
    updated_at: Optional[datetime] = Field(None, example="2024-11-09 15:04:45.504965")

    class Config:
        extra = "forbid"  # Forbid extra fields to be passed in API call.

class TaskResponse(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="My Task Title")
    description: Optional[str] = Field("No Description provided", example="Detailed description of the task")
    status: TaskStatus = Field(..., example="Open")
    created_at: datetime = Field(..., example="2024-11-09T15:04:45.504965")
    updated_at: datetime = Field(..., example="2024-11-09T15:04:45.504965")


from apps.model import Task
import pytest
from pydantic import ValidationError

def test_task_model_validation():
    with pytest.raises(ValidationError):
        Task()  # Attempt to create a Task without required fields

"""
In-memory storage implementation for the todo application.
"""
from typing import Dict, List, Optional
from src.todo_app.domain.models import Todo


class InMemoryStorage:
    """
    In-memory storage using Python data structures.
    """
    def __init__(self):
        self._storage: Dict[str, Todo] = {}

    def save(self, todo: Todo) -> Todo:
        """Save a todo item to storage."""
        self._storage[todo.id] = todo
        return todo

    def get_by_id(self, todo_id: str) -> Optional[Todo]:
        """Retrieve a todo item by its ID."""
        return self._storage.get(todo_id)

    def get_all(self) -> List[Todo]:
        """Retrieve all todo items from storage."""
        return list(self._storage.values())

    def delete(self, todo_id: str) -> bool:
        """Delete a todo item by ID."""
        if todo_id in self._storage:
            del self._storage[todo_id]
            return True
        return False

    def clear(self):
        """Clear all todos from storage (useful for testing)."""
        self._storage.clear()
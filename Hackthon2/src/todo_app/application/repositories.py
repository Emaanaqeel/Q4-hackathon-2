"""
Repository interfaces and implementations for the todo application.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.todo_app.domain.models import Todo
from src.todo_app.infrastructure.storage import InMemoryStorage
from src.todo_app.domain.exceptions import TodoNotFoundException


class TodoRepository(ABC):
    """
    Interface for managing todo items in storage.
    """

    @abstractmethod
    def add(self, todo: Todo) -> Todo:
        """Adds a new todo item to storage, returns the created item."""
        pass

    @abstractmethod
    def get_by_id(self, todo_id: str) -> Todo | None:
        """Retrieves a todo item by its ID, returns None if not found."""
        pass

    @abstractmethod
    def get_all(self) -> List[Todo]:
        """Retrieves all todo items from storage."""
        pass

    @abstractmethod
    def update(self, todo_id: str, title: str = None, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None, recurring: str = None) -> Todo | None:
        """Updates an existing todo item, returns updated item or None if not found."""
        pass

    @abstractmethod
    def delete(self, todo_id: str) -> bool:
        """Deletes a todo item by ID, returns True if successful, False if not found."""
        pass

    @abstractmethod
    def mark_complete(self, todo_id: str) -> Todo | None:
        """Marks a todo item as complete, returns updated item or None if not found."""
        pass

    @abstractmethod
    def mark_incomplete(self, todo_id: str) -> Todo | None:
        """Marks a todo item as incomplete, returns updated item or None if not found."""
        pass


class InMemoryTodoRepository(TodoRepository):
    """
    In-memory implementation of TodoRepository.
    """

    def __init__(self, storage: InMemoryStorage):
        self._storage = storage

    def add(self, todo: Todo) -> Todo:
        """Adds a new todo item to storage."""
        return self._storage.save(todo)

    def get_by_id(self, todo_id: str) -> Todo | None:
        """Retrieves a todo item by its ID."""
        return self._storage.get_by_id(todo_id)

    def get_all(self) -> List[Todo]:
        """Retrieves all todo items from storage."""
        return self._storage.get_all()

    def update(self, todo_id: str, title: str = None, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None, recurring: str = None) -> Todo | None:
        """Updates an existing todo item."""
        todo = self._storage.get_by_id(todo_id)
        if todo is None:
            return None

        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if priority is not None:
            todo.priority = priority
        if tags is not None:
            todo.tags = tags
        if due_date is not None:
            todo.due_date = due_date
        if recurring is not None:
            todo.recurring = recurring

        return self._storage.save(todo)

    def delete(self, todo_id: str) -> bool:
        """Deletes a todo item by ID."""
        return self._storage.delete(todo_id)

    def mark_complete(self, todo_id: str) -> Todo | None:
        """Marks a todo item as complete."""
        todo = self._storage.get_by_id(todo_id)
        if todo is None:
            return None

        todo.mark_complete()
        return self._storage.save(todo)

    def mark_incomplete(self, todo_id: str) -> Todo | None:
        """Marks a todo item as incomplete."""
        todo = self._storage.get_by_id(todo_id)
        if todo is None:
            return None

        todo.mark_incomplete()
        return self._storage.save(todo)
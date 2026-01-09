"""
Application services for the todo application.
"""
from typing import List, Optional
from src.todo_app.domain.models import Todo
from src.todo_app.application.repositories import TodoRepository
from src.todo_app.domain.exceptions import (
    TodoTitleTooLongException,
    TodoTitleEmptyException,
    TodoDescriptionTooLongException,
    TodoNotFoundException,
    InvalidTodoException,
    InvalidPriorityException,
    InvalidRecurringException,
    InvalidDateException,
    InvalidTagException
)
from datetime import datetime
import uuid


class TodoService:
    """
    Application service that implements business logic for todo operations.
    """

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    def _validate_title(self, title: str):
        """Validate the title according to business rules."""
        if not title or not title.strip():
            raise TodoTitleEmptyException("Title cannot be empty or contain only whitespace")

        if len(title) > 100:
            raise TodoTitleTooLongException(f"Title exceeds maximum length of 100 characters: {len(title)} provided")

    def _validate_description(self, description: str):
        """Validate the description according to business rules."""
        if description and len(description) > 500:
            raise TodoDescriptionTooLongException(f"Description exceeds maximum length of 500 characters: {len(description)} provided")

    def _validate_priority(self, priority: str):
        """Validate the priority level."""
        if priority and priority not in ['low', 'medium', 'high']:
            raise InvalidPriorityException(f"Priority must be one of 'low', 'medium', or 'high': {priority} provided")

    def _validate_recurring(self, recurring: str):
        """Validate the recurring pattern."""
        if recurring and recurring not in ['daily', 'weekly', 'monthly', None]:
            raise InvalidRecurringException(f"Recurring pattern must be one of 'daily', 'weekly', 'monthly', or None: {recurring} provided")

    def _validate_date(self, date_str: str):
        """Validate the date format (YYYY-MM-DD)."""
        if date_str:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                raise InvalidDateException(f"Date must be in YYYY-MM-DD format: {date_str} provided")

    def _validate_tags(self, tags: List[str]):
        """Validate the tags list."""
        if tags:
            for tag in tags:
                if not isinstance(tag, str) or not tag.strip():
                    raise InvalidTagException(f"Tags must be non-empty strings: {tag} provided")

    def create_todo(self, title: str, description: str = None, priority: str = "medium", tags: List[str] = None, due_date: str = None, recurring: str = None) -> Todo:
        """Creates a new todo item with validation."""
        self._validate_title(title)
        if description:
            self._validate_description(description)
        if priority:
            self._validate_priority(priority)
        if tags:
            self._validate_tags(tags)
        if due_date:
            self._validate_date(due_date)
        if recurring:
            self._validate_recurring(recurring)

        # Generate a unique ID
        todo_id = str(uuid.uuid4())

        # Convert due_date string to datetime object if provided
        due_date_obj = None
        if due_date:
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')

        # Create and save the new todo
        todo = Todo(
            id=todo_id,
            title=title.strip(),
            description=description,
            completed=False,
            priority=priority,
            tags=tags or [],
            due_date=due_date_obj,
            recurring=recurring
        )

        return self._repository.add(todo)

    def get_todo(self, todo_id: str) -> Todo | None:
        """Retrieves a todo item by ID."""
        return self._repository.get_by_id(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """Retrieves all todo items."""
        return self._repository.get_all()

    def update_todo(self, todo_id: str, title: str = None, description: str = None, priority: str = None, tags: List[str] = None, due_date: str = None, recurring: str = None) -> Todo | None:
        """Updates an existing todo item with validation."""
        # Get the existing todo
        existing_todo = self._repository.get_by_id(todo_id)
        if existing_todo is None:
            return None

        # Validate new values if provided
        if title is not None:
            self._validate_title(title)
            title = title.strip()
        if description is not None:
            self._validate_description(description)
        if priority is not None:
            self._validate_priority(priority)
        if tags is not None:
            self._validate_tags(tags)
        if due_date is not None:
            self._validate_date(due_date)
        if recurring is not None:
            self._validate_recurring(recurring)

        # Convert due_date string to datetime object if provided
        due_date_obj = None
        if due_date:
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')

        # Update the todo
        return self._repository.update(todo_id, title, description, priority, tags, due_date_obj, recurring)

    def delete_todo(self, todo_id: str) -> bool:
        """Deletes a todo item by ID."""
        return self._repository.delete(todo_id)

    def complete_todo(self, todo_id: str) -> Todo | None:
        """Marks a todo item as complete."""
        return self._repository.mark_complete(todo_id)

    def incomplete_todo(self, todo_id: str) -> Todo | None:
        """Marks a todo item as incomplete."""
        return self._repository.mark_incomplete(todo_id)

    def search_todos(self, keyword: str) -> List[Todo]:
        """Search todos by keyword in title or description."""
        all_todos = self._repository.get_all()
        keyword_lower = keyword.lower()
        return [
            todo for todo in all_todos
            if keyword_lower in todo.title.lower() or
            (todo.description and keyword_lower in todo.description.lower())
        ]

    def filter_todos(self, status: str = None, priority: str = None, tags: List[str] = None) -> List[Todo]:
        """Filter todos by status, priority, or tags."""
        all_todos = self._repository.get_all()
        filtered_todos = all_todos

        if status is not None:
            if status == "complete":
                filtered_todos = [todo for todo in filtered_todos if todo.completed]
            elif status == "incomplete":
                filtered_todos = [todo for todo in filtered_todos if not todo.completed]

        if priority is not None:
            filtered_todos = [todo for todo in filtered_todos if todo.priority == priority]

        if tags is not None and len(tags) > 0:
            # Filter todos that contain all specified tags
            for tag in tags:
                filtered_todos = [todo for todo in filtered_todos if tag in todo.tags]

        return filtered_todos

    def sort_todos(self, by: str = "title") -> List[Todo]:
        """Sort todos by priority, due date, or title."""
        all_todos = self._repository.get_all()

        if by == "priority":
            # Sort by priority: high, medium, low
            priority_order = {"high": 0, "medium": 1, "low": 2}
            return sorted(all_todos, key=lambda todo: (priority_order.get(todo.priority, 3), todo.title))
        elif by == "due_date":
            # Sort by due date (None dates go to the end)
            return sorted(all_todos, key=lambda todo: (todo.due_date is None, todo.due_date))
        else:  # Default to sorting by title
            return sorted(all_todos, key=lambda todo: todo.title.lower())

    def get_todos_due_soon(self, days: int = 7) -> List[Todo]:
        """Get todos that are due within the specified number of days."""
        from datetime import datetime, timedelta
        all_todos = self._repository.get_all()

        today = datetime.now().date()
        future_date = today + timedelta(days=days)

        due_soon_todos = []
        for todo in all_todos:
            if todo.due_date:
                due_date_only = todo.due_date.date()
                if today <= due_date_only <= future_date:
                    due_soon_todos.append(todo)

        return due_soon_todos

    def process_recurring_tasks(self):
        """Process recurring tasks and create new instances when needed."""
        from datetime import datetime, timedelta
        all_todos = self._repository.get_all()

        for todo in all_todos:
            if todo.recurring and todo.completed:
                # Check if it's time to create a new recurring instance
                if todo.due_date:
                    due_date_only = todo.due_date.date()
                    today = datetime.now().date()

                    # Determine the next occurrence based on the recurring pattern
                    next_occurrence = None
                    if todo.recurring == "daily":
                        next_occurrence = due_date_only + timedelta(days=1)
                    elif todo.recurring == "weekly":
                        next_occurrence = due_date_only + timedelta(weeks=1)
                    elif todo.recurring == "monthly":
                        # Simple monthly calculation (add 30 days)
                        next_occurrence = due_date_only + timedelta(days=30)

                    # If the next occurrence date has arrived or passed, create a new instance
                    if next_occurrence and next_occurrence <= today:
                        # Create a new todo with the same properties but not completed
                        new_todo = Todo(
                            id=str(uuid.uuid4()),
                            title=todo.title,
                            description=todo.description,
                            completed=False,
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                            priority=todo.priority,
                            tags=todo.tags,
                            due_date=datetime.combine(next_occurrence, datetime.min.time()),
                            recurring=todo.recurring,
                            reminder_set=todo.reminder_set
                        )
                        self._repository.add(new_todo)
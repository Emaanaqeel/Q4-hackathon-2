from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Todo:
    """
    Represents a single todo item with all required attributes.

    Attributes:
        id (str): Unique identifier for the todo item (automatically generated)
        title (str): Title of the todo item (required, max 100 characters)
        description (str): Optional description of the todo item (optional, max 500 characters)
        completed (bool): Completion status of the todo item (default: False)
        created_at (datetime): Timestamp when the todo was created
        updated_at (datetime): Timestamp when the todo was last updated
        priority (str): Priority level ('low', 'medium', 'high') (default: 'medium')
        tags (List[str]): List of tags/categories for the task (default: [])
        due_date (datetime): Optional due date for the task (default: None)
        recurring (str): Recurrence pattern ('daily', 'weekly', 'monthly', None) (default: None)
        reminder_set (bool): Whether a reminder is set (default: False)
    """
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = None
    updated_at: datetime = None
    priority: str = "medium"
    tags: List[str] = None
    due_date: datetime = None
    recurring: str = None
    reminder_set: bool = False

    def __post_init__(self):
        """Initialize timestamps after object creation."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.tags is None:
            self.tags = []

    def mark_complete(self):
        """Mark the todo as complete."""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self):
        """Mark the todo as incomplete."""
        self.completed = False
        self.updated_at = datetime.now()

    def update(self, title: str = None, description: str = None, priority: str = None, tags: List[str] = None, due_date: datetime = None, recurring: str = None, reminder_set: bool = None):
        """Update the todo with new information."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = priority
        if tags is not None:
            self.tags = tags
        if due_date is not None:
            self.due_date = due_date
        if recurring is not None:
            self.recurring = recurring
        if reminder_set is not None:
            self.reminder_set = reminder_set
        self.updated_at = datetime.now()

    def add_tag(self, tag: str):
        """Add a tag to the todo if it doesn't already exist."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str):
        """Remove a tag from the todo if it exists."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
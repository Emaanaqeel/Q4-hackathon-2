"""
Domain-specific exceptions for the todo application.
"""


class TodoException(Exception):
    """Base exception for todo-related errors."""
    pass


class InvalidTodoException(TodoException):
    """Raised when a todo item is invalid."""
    pass


class TodoTitleTooLongException(InvalidTodoException):
    """Raised when a todo title exceeds the maximum length."""
    pass


class TodoTitleEmptyException(InvalidTodoException):
    """Raised when a todo title is empty or contains only whitespace."""
    pass


class TodoDescriptionTooLongException(InvalidTodoException):
    """Raised when a todo description exceeds the maximum length."""
    pass


class TodoNotFoundException(TodoException):
    """Raised when a todo item with a given ID is not found."""
    pass


class InvalidTodoIdException(TodoException):
    """Raised when a todo ID is invalid."""
    pass


class InvalidPriorityException(InvalidTodoException):
    """Raised when a priority level is invalid."""
    pass


class InvalidRecurringException(InvalidTodoException):
    """Raised when a recurring pattern is invalid."""
    pass


class InvalidDateException(InvalidTodoException):
    """Raised when a date format is invalid."""
    pass


class InvalidTagException(InvalidTodoException):
    """Raised when a tag is invalid."""
    pass
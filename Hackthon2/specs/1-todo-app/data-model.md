# Data Model: Phase I – In-Memory Python Console-Based Todo Application

## Todo Entity

**Name**: Todo
**Description**: Represents a single todo item with all required attributes

**Fields**:
- `id` (str): Unique identifier for the todo item (automatically generated)
- `title` (str): Title of the todo item (required, max 100 characters)
- `description` (str): Optional description of the todo item (optional, max 500 characters)
- `completed` (bool): Completion status of the todo item (default: False)

**Validation Rules**:
- `id`: Must be unique within the system, automatically generated using UUID or incrementing counter
- `title`: Required field, must be 1-100 characters long, cannot be empty or whitespace-only
- `description`: Optional field, if provided must be 1-500 characters long
- `completed`: Boolean value, defaults to False when creating new items

**State Transitions**:
- `incomplete` → `complete`: When user marks todo as complete
- `complete` → `incomplete`: When user marks todo as incomplete

## Todo Repository Interface

**Name**: TodoRepository
**Description**: Interface for managing todo items in storage

**Methods**:
- `add(todo: Todo) -> Todo`: Adds a new todo item to storage, returns the created item
- `get_by_id(todo_id: str) -> Todo | None`: Retrieves a todo item by its ID, returns None if not found
- `get_all() -> List[Todo]`: Retrieves all todo items from storage
- `update(todo_id: str, title: str = None, description: str = None) -> Todo | None`: Updates an existing todo item, returns updated item or None if not found
- `delete(todo_id: str) -> bool`: Deletes a todo item by ID, returns True if successful, False if not found
- `mark_complete(todo_id: str) -> Todo | None`: Marks a todo item as complete, returns updated item or None if not found
- `mark_incomplete(todo_id: str) -> Todo | None`: Marks a todo item as incomplete, returns updated item or None if not found

## Todo Service Interface

**Name**: TodoService
**Description**: Application service that implements business logic for todo operations

**Methods**:
- `create_todo(title: str, description: str = None) -> Todo`: Creates a new todo item with validation
- `get_todo(todo_id: str) -> Todo | None`: Retrieves a todo item by ID
- `get_all_todos() -> List[Todo]`: Retrieves all todo items
- `update_todo(todo_id: str, title: str = None, description: str = None) -> Todo | None`: Updates an existing todo item with validation
- `delete_todo(todo_id: str) -> bool`: Deletes a todo item by ID
- `complete_todo(todo_id: str) -> Todo | None`: Marks a todo item as complete
- `incomplete_todo(todo_id: str) -> Todo | None`: Marks a todo item as incomplete

## Validation Rules Summary

**Title Validation**:
- Required field
- Length: 1-100 characters
- Cannot be empty or contain only whitespace

**Description Validation**:
- Optional field
- Length: 0-500 characters (if provided, must be 1-500 characters)

**ID Validation**:
- Automatically generated
- Must be unique within the system
- Format: UUID string or incrementing integer as string

**Status Validation**:
- Boolean value only
- Default value: False (incomplete)
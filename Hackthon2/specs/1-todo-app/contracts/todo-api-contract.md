# Todo Application API Contract

## Overview
This contract defines the interface for the in-memory console-based todo application. The application provides a command-line interface for managing todo items.

## Commands

### Add Todo
- **Command**: `add`
- **Arguments**:
  - `title` (required): Title of the todo item (string, 1-100 characters)
  - `description` (optional): Description of the todo item (string, 0-500 characters)
- **Response**: Success message with created todo ID and details
- **Error Cases**:
  - Title too long (over 100 characters)
  - Title is empty or whitespace only

### List Todos
- **Command**: `list`
- **Arguments**: None
- **Response**: List of all todos with ID, title, description, and completion status
- **Error Cases**: None

### Update Todo
- **Command**: `update`
- **Arguments**:
  - `id` (required): ID of the todo to update (string)
  - `new_title` (optional): New title for the todo (string, 1-100 characters)
  - `new_description` (optional): New description for the todo (string, 0-500 characters)
- **Response**: Success message with updated todo details
- **Error Cases**:
  - Todo with given ID does not exist
  - New title too long (over 100 characters)
  - New title is empty or whitespace only

### Delete Todo
- **Command**: `delete`
- **Arguments**:
  - `id` (required): ID of the todo to delete (string)
- **Response**: Success message confirming deletion
- **Error Cases**:
  - Todo with given ID does not exist

### Mark Complete
- **Command**: `complete`
- **Arguments**:
  - `id` (required): ID of the todo to mark as complete (string)
- **Response**: Success message with updated todo status
- **Error Cases**:
  - Todo with given ID does not exist

### Mark Incomplete
- **Command**: `incomplete`
- **Arguments**:
  - `id` (required): ID of the todo to mark as incomplete (string)
- **Response**: Success message with updated todo status
- **Error Cases**:
  - Todo with given ID does not exist

## Data Model

### Todo
- `id` (string): Unique identifier
- `title` (string): Title (1-100 characters)
- `description` (string): Description (0-500 characters)
- `completed` (boolean): Completion status

## Error Handling
All commands should return appropriate error messages when:
- Invalid command is provided
- Required arguments are missing
- Todo ID does not exist
- Validation constraints are violated
- Malformed input is provided
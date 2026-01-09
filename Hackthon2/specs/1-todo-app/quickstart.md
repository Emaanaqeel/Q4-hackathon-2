# Quickstart Guide: Phase I – In-Memory Python Console-Based Todo Application

## Prerequisites

- Python 3.13 or higher
- UV package manager (for dependency management)

## Setup

1. **Clone or initialize the repository**
   ```bash
   # If starting fresh, initialize the project
   uv init
   ```

2. **Create the project structure**
   ```bash
   mkdir -p src/todo_app/{domain,application,infrastructure}
   touch src/todo_app/__init__.py
   touch src/todo_app/domain/__init__.py
   touch src/todo_app/application/__init__.py
   touch src/todo_app/infrastructure/__init__.py
   ```

3. **Install dependencies (if any)**
   ```bash
   # This Phase I application uses only standard library, so no dependencies needed
   # But if you add dependencies later, use:
   # uv add <package-name>
   ```

## Running the Application

1. **Execute the main application**
   ```bash
   python -m src.todo_app.main
   ```

2. **Or run directly if main.py is configured as a module**
   ```bash
   python src/todo_app/main.py
   ```

## Available Commands

Once the application is running, you can use the following commands:

### Add a new todo
```bash
python -m src.todo_app.main add "My new task" "Optional description here"
```

### List all todos
```bash
python -m src.todo_app.main list
```

### Update a todo
```bash
python -m src.todo_app.main update <todo_id> "New title" "Optional new description"
```

### Delete a todo
```bash
python -m src.todo_app.main delete <todo_id>
```

### Mark a todo as complete
```bash
python -m src.todo_app.main complete <todo_id>
```

### Mark a todo as incomplete
```bash
python -m src.todo_app.main incomplete <todo_id>
```

## Example Usage

```bash
# Add a new todo
python -m src.todo_app.main add "Buy groceries" "Need to buy milk, bread, and eggs"

# List all todos
python -m src.todo_app.main list

# Mark the first todo as complete (assuming its ID is 1)
python -m src.todo_app.main complete 1

# Update a todo
python -m src.todo_app.main update 1 "Buy groceries - urgent" "Need to buy milk, bread, eggs, and fruits"

# Delete a todo
python -m src.todo_app.main delete 1
```

## Development

### Running Tests
```bash
# Install pytest if needed
uv add pytest

# Run all tests
python -m pytest tests/
```

### Project Structure
```
src/
├── todo_app/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py          # Todo entity and related models
│   │   └── exceptions.py      # Domain-specific exceptions
│   ├── application/
│   │   ├── __init__.py
│   │   ├── services.py        # Todo service with business logic
│   │   └── repositories.py    # In-memory repository implementation
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── console.py         # Console interface and command parsing
│   │   └── storage.py         # In-memory storage implementation
│   └── main.py                # Application entry point
│
tests/
├── unit/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── integration/
│   └── test_end_to_end.py
└── conftest.py
```

## Environment Configuration

The application uses only in-memory storage and requires no external configuration. All data is stored in memory during the application's runtime and is lost when the application terminates.
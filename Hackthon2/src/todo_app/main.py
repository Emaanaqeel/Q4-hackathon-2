import sys
from src.todo_app.infrastructure.storage import InMemoryStorage
from src.todo_app.application.repositories import InMemoryTodoRepository
from src.todo_app.application.services import TodoService
from src.todo_app.infrastructure.console import ConsoleInterface


def main():
    # Initialize the application components
    storage = InMemoryStorage()
    repository = InMemoryTodoRepository(storage)
    service = TodoService(repository)
    console = ConsoleInterface(service)

    # If command line arguments are provided, run them as a single command
    if len(sys.argv) > 1:
        # Skip the script name and pass the rest as arguments
        args = sys.argv[1:]
        result = console.parse_command(args)
        print(result)
    else:
        # Run the interactive console
        console.run_interactive()


if __name__ == "__main__":
    main()
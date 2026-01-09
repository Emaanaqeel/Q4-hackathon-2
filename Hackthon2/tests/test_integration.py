import unittest
from src.todo_app.infrastructure.storage import InMemoryStorage
from src.todo_app.application.repositories import InMemoryTodoRepository
from src.todo_app.application.services import TodoService
from src.todo_app.infrastructure.console import ConsoleInterface


class TestTodoAppIntegration(unittest.TestCase):
    def setUp(self):
        storage = InMemoryStorage()
        repository = InMemoryTodoRepository(storage)
        service = TodoService(repository)
        self.console = ConsoleInterface(service)

    def test_complete_workflow(self):
        """Test the complete workflow: add, list, update, complete, delete"""
        # Add a todo
        result = self.console.handle_add(["Test todo", "Test description"])
        self.assertIn("Added todo:", result)

        # Extract the ID from the result
        todo_id = result.split(" - ")[0].split(": ")[1]

        # List todos
        result = self.console.handle_list()
        self.assertIn("Test todo", result)
        self.assertIn("Test description", result)
        self.assertIn("I", result)  # Should show incomplete status

        # Update the todo
        result = self.console.handle_update([todo_id, "Updated todo", "Updated description"])
        self.assertIn("Updated todo:", result)

        # Complete the todo
        result = self.console.handle_complete([todo_id])
        self.assertIn("Marked todo as complete:", result)

        # List again to see the complete status
        result = self.console.handle_list()
        self.assertIn("C", result)  # Should show complete status

        # Delete the todo
        result = self.console.handle_delete([todo_id])
        self.assertIn("Deleted todo", result)

        # List to confirm deletion
        result = self.console.handle_list()
        self.assertIn("No todos found", result)


if __name__ == '__main__':
    unittest.main()
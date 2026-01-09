import unittest
from src.todo_app.infrastructure.storage import InMemoryStorage
from src.todo_app.application.repositories import InMemoryTodoRepository
from src.todo_app.application.services import TodoService
from src.todo_app.domain.exceptions import TodoTitleTooLongException, TodoTitleEmptyException, TodoDescriptionTooLongException


class TestTodoApp(unittest.TestCase):
    def setUp(self):
        storage = InMemoryStorage()
        repository = InMemoryTodoRepository(storage)
        self.service = TodoService(repository)

    def test_create_todo_with_title_and_description(self):
        """Test creating a todo with title and description"""
        title = "Test title"
        description = "Test description"

        todo = self.service.create_todo(title, description)

        self.assertEqual(todo.title, title)
        self.assertEqual(todo.description, description)
        self.assertFalse(todo.completed)  # Should default to incomplete
        self.assertIsNotNone(todo.id)     # Should have a unique ID

    def test_create_todo_with_title_only(self):
        """Test creating a todo with only a title"""
        title = "Test title"

        todo = self.service.create_todo(title)

        self.assertEqual(todo.title, title)
        self.assertIsNone(todo.description)
        self.assertFalse(todo.completed)
        self.assertIsNotNone(todo.id)

    def test_create_todo_title_validation(self):
        """Test that titles are validated properly"""
        # Test empty title
        with self.assertRaises(TodoTitleEmptyException):
            self.service.create_todo("")

        # Test whitespace-only title
        with self.assertRaises(TodoTitleEmptyException):
            self.service.create_todo("   ")

        # Test title too long
        with self.assertRaises(TodoTitleTooLongException):
            self.service.create_todo("A" * 101)  # 101 characters

    def test_create_todo_description_validation(self):
        """Test that descriptions are validated properly"""
        # Test description too long
        with self.assertRaises(TodoDescriptionTooLongException):
            self.service.create_todo("Valid title", "A" * 501)  # 501 characters

    def test_update_todo(self):
        """Test updating a todo"""
        # Create a todo first
        original_title = "Original title"
        original_description = "Original description"
        todo = self.service.create_todo(original_title, original_description)

        # Update the todo
        new_title = "Updated title"
        new_description = "Updated description"
        updated_todo = self.service.update_todo(todo.id, new_title, new_description)

        self.assertEqual(updated_todo.title, new_title)
        self.assertEqual(updated_todo.description, new_description)

    def test_complete_and_incomplete_todo(self):
        """Test marking a todo as complete and incomplete"""
        # Create a todo
        todo = self.service.create_todo("Test title")
        self.assertFalse(todo.completed)

        # Mark as complete
        completed_todo = self.service.complete_todo(todo.id)
        self.assertTrue(completed_todo.completed)

        # Mark as incomplete
        incomplete_todo = self.service.incomplete_todo(todo.id)
        self.assertFalse(incomplete_todo.completed)

    def test_delete_todo(self):
        """Test deleting a todo"""
        # Create a todo
        todo = self.service.create_todo("Test title")

        # Verify it exists
        retrieved_todo = self.service.get_todo(todo.id)
        self.assertIsNotNone(retrieved_todo)

        # Delete the todo
        result = self.service.delete_todo(todo.id)
        self.assertTrue(result)

        # Verify it no longer exists
        retrieved_todo = self.service.get_todo(todo.id)
        self.assertIsNone(retrieved_todo)


if __name__ == '__main__':
    unittest.main()
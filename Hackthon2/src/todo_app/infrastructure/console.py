"""
Console interface for the menu-driven todo application.
"""
import sys
import os
from datetime import datetime, timedelta
from typing import List, Optional
from src.todo_app.application.services import TodoService
from src.todo_app.domain.models import Todo


class ConsoleInterface:
    """
    Console interface for the menu-driven todo application.
    """

    def __init__(self, todo_service: TodoService):
        self.todo_service = todo_service

    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display the application header."""
        self.clear_screen()
        print("TODO LIST APPLICATION")
        print("=" * 30)

    def display_menu(self):
        """Display the main menu options."""
        print("\nPlease select an option:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete / Incomplete")
        print("6. Manage Task Features")
        print("7. Exit")
        print()

    def display_features_menu(self):
        """Display the features submenu."""
        print("\nTask Features Menu:")
        print("1. Set Priority")
        print("2. Add/Remove Tags")
        print("3. Set Due Date")
        print("4. Set Recurring Task")
        print("5. Search Tasks")
        print("6. Filter Tasks")
        print("7. Sort Tasks")
        print("8. View Reminders")
        print("9. Back to Main Menu")
        print()

    def get_user_choice(self) -> str:
        """Get and validate user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                sys.exit(0)

    def get_features_choice(self) -> str:
        """Get and validate user's features menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-9): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 9.")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                sys.exit(0)

    def handle_add_task(self):
        """Handle adding a new task with guided input."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()

        description_input = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        # Get priority
        priority = "medium"  # Default
        priority_input = input("Enter priority (high/medium/low, press Enter for 'medium'): ").strip().lower()
        if priority_input in ['high', 'medium', 'low']:
            priority = priority_input
        elif priority_input:  # If user entered something but it's not valid
            print("Invalid priority. Using 'medium' as default.")
            priority = "medium"

        # Get tags
        tags_input = input("Enter tags separated by commas (optional, press Enter to skip): ").strip()
        tags = []
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        # Get due date
        due_date = None
        due_date_input = input("Enter due date (YYYY-MM-DD format, optional, press Enter to skip): ").strip()
        if due_date_input:
            due_date = due_date_input

        # Get recurring pattern
        recurring = None
        recurring_input = input("Enter recurrence (daily/weekly/monthly, optional, press Enter to skip): ").strip().lower()
        if recurring_input in ['daily', 'weekly', 'monthly']:
            recurring = recurring_input
        elif recurring_input:  # If user entered something but it's not valid
            print("Invalid recurring pattern. No recurrence will be set.")

        try:
            todo = self.todo_service.create_todo(title, description, priority, tags, due_date, recurring)
            print(f"\n✓ Added task: {todo.id[:8]} - {todo.title}")
        except Exception as e:
            print(f"\n✗ Error adding task: {str(e)}")

    def display_tasks(self):
        """Display all tasks in a formatted table with sequential numbers."""
        todos = self.todo_service.get_all_todos()

        if not todos:
            print("\nNo tasks found.")
            return

        print("\n#  | Status | Priority | Tags              | Due Date   | Title                    | Description")
        print("-" * 120)

        for index, todo in enumerate(todos, start=1):
            status = "[✓]" if todo.completed else "[ ]"
            priority = f"[{todo.priority[:3].upper()}]"  # Show first 3 letters of priority
            tags_str = ",".join(todo.tags[:2])  # Show first 2 tags, join with comma
            if len(todo.tags) > 2:
                tags_str += "..."
            due_date_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
            title = todo.title[:20]  # Limit title length for display
            description = (todo.description[:20] if todo.description else "")[:20]  # Limit description length
            print(f"{index:<2} | {status}    | {priority:<7}  | {tags_str:<17} | {due_date_str:<10} | {title:<22} | {description}")

        # Return the mapping of sequential numbers to UUIDs for reference
        return {index: todo.id for index, todo in enumerate(todos, start=1)}

    def handle_view_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- All Tasks ---")
        self.display_tasks()

    def handle_update_task(self):
        """Handle updating an existing task with guided input."""
        print("\n--- Update Task ---")
        id_mapping = self.display_tasks()

        if not self.todo_service.get_all_todos():
            print("No tasks available to update.")
            return

        task_num_input = input("\nEnter the task number to update: ").strip()

        # Validate and convert the task number to UUID
        try:
            task_num = int(task_num_input)
            if task_num not in id_mapping:
                print(f"✗ Error: Task number {task_num} not found.")
                return
            todo_id = id_mapping[task_num]
        except ValueError:
            print("✗ Error: Please enter a valid number.")
            return

        # Check if the task exists
        existing_todo = self.todo_service.get_todo(todo_id)
        if not existing_todo:
            print(f"✗ Error: Task with ID {todo_id} not found.")
            return

        print(f"Current title: {existing_todo.title}")
        new_title = input("Enter new title (or press Enter to keep current): ").strip()
        new_title = new_title if new_title else None  # Use None if empty to keep current

        print(f"Current description: {existing_todo.description or 'None'}")
        new_description = input("Enter new description (or press Enter to keep current): ").strip()
        new_description = new_description if new_description else None  # Use None if empty to keep current

        print(f"Current priority: {existing_todo.priority}")
        new_priority = input("Enter new priority (high/medium/low, or press Enter to keep current): ").strip().lower()
        new_priority = new_priority if new_priority in ['high', 'medium', 'low'] else None  # Use None if empty or invalid to keep current

        print(f"Current tags: {', '.join(existing_todo.tags) if existing_todo.tags else 'None'}")
        new_tags_input = input("Enter new tags separated by commas (or press Enter to keep current): ").strip()
        new_tags = None
        if new_tags_input:
            new_tags = [tag.strip() for tag in new_tags_input.split(',') if tag.strip()]
        # If empty input, we keep current tags by not updating

        print(f"Current due date: {existing_todo.due_date.strftime('%Y-%m-%d') if existing_todo.due_date else 'None'}")
        new_due_date = input("Enter new due date (YYYY-MM-DD format, or press Enter to keep current): ").strip()
        new_due_date = new_due_date if new_due_date else None  # Use None if empty to keep current

        print(f"Current recurrence: {existing_todo.recurring or 'None'}")
        new_recurring = input("Enter new recurrence (daily/weekly/monthly, or press Enter to keep current): ").strip().lower()
        new_recurring = new_recurring if new_recurring in ['daily', 'weekly', 'monthly'] else None  # Use None if empty or invalid to keep current

        try:
            updated_todo = self.todo_service.update_todo(todo_id, new_title, new_description, new_priority, new_tags, new_due_date, new_recurring)
            if updated_todo:
                print(f"\n✓ Updated task: {task_num} - {updated_todo.title}")
            else:
                print(f"\n✗ Error: Task with ID {todo_id} not found.")
        except Exception as e:
            print(f"\n✗ Error updating task: {str(e)}")

    def handle_delete_task(self):
        """Handle deleting a task with guided input."""
        print("\n--- Delete Task ---")
        id_mapping = self.display_tasks()

        if not self.todo_service.get_all_todos():
            print("No tasks available to delete.")
            return

        task_num_input = input("\nEnter the task number to delete: ").strip()

        # Validate and convert the task number to UUID
        try:
            task_num = int(task_num_input)
            if task_num not in id_mapping:
                print(f"✗ Error: Task number {task_num} not found.")
                return
            todo_id = id_mapping[task_num]
        except ValueError:
            print("✗ Error: Please enter a valid number.")
            return

        try:
            success = self.todo_service.delete_todo(todo_id)
            if success:
                print(f"\n✓ Deleted task #{task_num}")
            else:
                print(f"\n✗ Error: Task with ID {todo_id} not found.")
        except Exception as e:
            print(f"\n✗ Error deleting task: {str(e)}")

    def handle_toggle_complete(self):
        """Handle marking a task as complete/incomplete with guided input."""
        print("\n--- Mark Task Complete / Incomplete ---")
        id_mapping = self.display_tasks()

        if not self.todo_service.get_all_todos():
            print("No tasks available to update.")
            return

        task_num_input = input("\nEnter the task number to toggle: ").strip()

        # Validate and convert the task number to UUID
        try:
            task_num = int(task_num_input)
            if task_num not in id_mapping:
                print(f"✗ Error: Task number {task_num} not found.")
                return
            todo_id = id_mapping[task_num]
        except ValueError:
            print("✗ Error: Please enter a valid number.")
            return

        # Check if the task exists
        existing_todo = self.todo_service.get_todo(todo_id)
        if not existing_todo:
            print(f"✗ Error: Task with ID {todo_id} not found.")
            return

        try:
            if existing_todo.completed:
                # Mark as incomplete
                updated_todo = self.todo_service.incomplete_todo(todo_id)
                if updated_todo:
                    print(f"\n✓ Marked task #{task_num} as incomplete: {updated_todo.title}")
                else:
                    print(f"\n✗ Error: Task with ID {todo_id} not found.")
            else:
                # Mark as complete
                updated_todo = self.todo_service.complete_todo(todo_id)
                if updated_todo:
                    print(f"\n✓ Marked task #{task_num} as complete: {updated_todo.title}")
                else:
                    print(f"\n✗ Error: Task with ID {todo_id} not found.")
        except Exception as e:
            print(f"\n✗ Error updating task status: {str(e)}")

    def pause_for_user_input(self):
        """Pause and wait for user to press Enter."""
        input("\nPress Enter to continue...")

    def handle_set_priority(self):
        """Handle setting priority for a task."""
        print("\n--- Set Task Priority ---")
        id_mapping = self.display_tasks()

        if not self.todo_service.get_all_todos():
            print("No tasks available.")
            return

        task_num_input = input("\nEnter the task number to set priority: ").strip()

        # Validate and convert the task number to UUID
        try:
            task_num = int(task_num_input)
            if task_num not in id_mapping:
                print(f"✗ Error: Task number {task_num} not found.")
                return
            todo_id = id_mapping[task_num]
        except ValueError:
            print("✗ Error: Please enter a valid number.")
            return

        # Check if the task exists
        existing_todo = self.todo_service.get_todo(todo_id)
        if not existing_todo:
            print(f"✗ Error: Task with ID {todo_id} not found.")
            return

        print(f"Current priority: {existing_todo.priority}")
        new_priority = input("Enter new priority (high/medium/low): ").strip().lower()

        if new_priority not in ['high', 'medium', 'low']:
            print("✗ Error: Invalid priority. Must be 'high', 'medium', or 'low'.")
            return

        try:
            updated_todo = self.todo_service.update_todo(todo_id, priority=new_priority)
            if updated_todo:
                print(f"\n✓ Updated priority for task: {task_num} - {updated_todo.title} [{updated_todo.priority}]")
            else:
                print(f"\n✗ Error: Task with ID {todo_id} not found.")
        except Exception as e:
            print(f"\n✗ Error updating priority: {str(e)}")

    def handle_manage_tags(self):
        """Handle adding/removing tags for a task."""
        print("\n--- Manage Task Tags ---")
        id_mapping = self.display_tasks()

        if not self.todo_service.get_all_todos():
            print("No tasks available.")
            return

        task_num_input = input("\nEnter the task number to manage tags: ").strip()

        # Validate and convert the task number to UUID
        try:
            task_num = int(task_num_input)
            if task_num not in id_mapping:
                print(f"✗ Error: Task number {task_num} not found.")
                return
            todo_id = id_mapping[task_num]
        except ValueError:
            print("✗ Error: Please enter a valid number.")
            return

        # Check if the task exists
        existing_todo = self.todo_service.get_todo(todo_id)
        if not existing_todo:
            print(f"✗ Error: Task with ID {todo_id} not found.")
            return

        print(f"Current tags: {', '.join(existing_todo.tags) if existing_todo.tags else 'None'}")
        print("Options:")
        print("1. Add tags")
        print("2. Remove tags")

        option = input("Choose option (1 or 2): ").strip()

        if option == "1":
            new_tags_input = input("Enter tags to add separated by commas: ").strip()
            if new_tags_input:
                new_tags = [tag.strip() for tag in new_tags_input.split(',') if tag.strip()]

                # Combine existing tags with new ones, avoiding duplicates
                all_tags = list(set(existing_todo.tags + new_tags))

                try:
                    updated_todo = self.todo_service.update_todo(todo_id, tags=all_tags)
                    if updated_todo:
                        print(f"\n✓ Updated tags for task: {task_num} - {updated_todo.title}")
                        print(f"New tags: {', '.join(updated_todo.tags)}")
                    else:
                        print(f"\n✗ Error: Task with ID {todo_id} not found.")
                except Exception as e:
                    print(f"\n✗ Error updating tags: {str(e)}")
            else:
                print("No tags were added.")
        elif option == "2":
            if not existing_todo.tags:
                print("Task has no tags to remove.")
                return

            tags_to_remove_input = input("Enter tags to remove separated by commas: ").strip()
            if tags_to_remove_input:
                tags_to_remove = [tag.strip() for tag in tags_to_remove_input.split(',') if tag.strip()]

                # Remove specified tags from existing tags
                new_tags = [tag for tag in existing_todo.tags if tag not in tags_to_remove]

                try:
                    updated_todo = self.todo_service.update_todo(todo_id, tags=new_tags)
                    if updated_todo:
                        print(f"\n✓ Updated tags for task: {task_num} - {updated_todo.title}")
                        print(f"Remaining tags: {', '.join(updated_todo.tags) if updated_todo.tags else 'None'}")
                    else:
                        print(f"\n✗ Error: Task with ID {todo_id} not found.")
                except Exception as e:
                    print(f"\n✗ Error updating tags: {str(e)}")
            else:
                print("No tags were removed.")
        else:
            print("Invalid option. Please choose 1 or 2.")

    def handle_set_due_date(self):
        """Handle setting due date for a task."""
        print("\n--- Set Task Due Date ---")
        id_mapping = self.display_tasks()

        if not self.todo_service.get_all_todos():
            print("No tasks available.")
            return

        task_num_input = input("\nEnter the task number to set due date: ").strip()

        # Validate and convert the task number to UUID
        try:
            task_num = int(task_num_input)
            if task_num not in id_mapping:
                print(f"✗ Error: Task number {task_num} not found.")
                return
            todo_id = id_mapping[task_num]
        except ValueError:
            print("✗ Error: Please enter a valid number.")
            return

        # Check if the task exists
        existing_todo = self.todo_service.get_todo(todo_id)
        if not existing_todo:
            print(f"✗ Error: Task with ID {todo_id} not found.")
            return

        print(f"Current due date: {existing_todo.due_date.strftime('%Y-%m-%d') if existing_todo.due_date else 'None'}")
        new_due_date = input("Enter new due date (YYYY-MM-DD format): ").strip()

        if new_due_date:
            try:
                # Validate the date format
                datetime.strptime(new_due_date, '%Y-%m-%d')

                try:
                    updated_todo = self.todo_service.update_todo(todo_id, due_date=new_due_date)
                    if updated_todo:
                        due_date_str = updated_todo.due_date.strftime('%Y-%m-%d') if updated_todo.due_date else 'None'
                        print(f"\n✓ Updated due date for task: {task_num} - {updated_todo.title} [{due_date_str}]")
                    else:
                        print(f"\n✗ Error: Task with ID {todo_id} not found.")
                except Exception as e:
                    print(f"\n✗ Error updating due date: {str(e)}")
            except ValueError:
                print("✗ Error: Invalid date format. Please use YYYY-MM-DD format.")
        else:
            print("No due date was set.")

    def handle_set_recurring(self):
        """Handle setting recurring pattern for a task."""
        print("\n--- Set Task Recurrence ---")
        id_mapping = self.display_tasks()

        if not self.todo_service.get_all_todos():
            print("No tasks available.")
            return

        task_num_input = input("\nEnter the task number to set recurrence: ").strip()

        # Validate and convert the task number to UUID
        try:
            task_num = int(task_num_input)
            if task_num not in id_mapping:
                print(f"✗ Error: Task number {task_num} not found.")
                return
            todo_id = id_mapping[task_num]
        except ValueError:
            print("✗ Error: Please enter a valid number.")
            return

        # Check if the task exists
        existing_todo = self.todo_service.get_todo(todo_id)
        if not existing_todo:
            print(f"✗ Error: Task with ID {todo_id} not found.")
            return

        print(f"Current recurrence: {existing_todo.recurring or 'None'}")
        new_recurring = input("Enter recurrence pattern (daily/weekly/monthly, or 'none' to remove): ").strip().lower()

        if new_recurring == 'none':
            new_recurring = None
        elif new_recurring not in ['daily', 'weekly', 'monthly']:
            print("✗ Error: Invalid recurrence pattern. Must be 'daily', 'weekly', 'monthly', or 'none'.")
            return

        try:
            updated_todo = self.todo_service.update_todo(todo_id, recurring=new_recurring)
            if updated_todo:
                recurring_str = updated_todo.recurring or 'None'
                print(f"\n✓ Updated recurrence for task: {task_num} - {updated_todo.title} [{recurring_str}]")
            else:
                print(f"\n✗ Error: Task with ID {todo_id} not found.")
        except Exception as e:
            print(f"\n✗ Error updating recurrence: {str(e)}")

    def handle_search_tasks(self):
        """Handle searching for tasks by keyword."""
        print("\n--- Search Tasks ---")
        keyword = input("Enter keyword to search: ").strip()

        if not keyword:
            print("No keyword provided.")
            return

        try:
            matching_todos = self.todo_service.search_todos(keyword)

            if not matching_todos:
                print(f"No tasks found containing '{keyword}'.")
                return

            print(f"\nFound {len(matching_todos)} task(s) containing '{keyword}':")
            print("\n#  | Status | Priority | Tags              | Due Date   | Title                    | Description")
            print("-" * 120)

            for index, todo in enumerate(matching_todos, start=1):
                status = "[✓]" if todo.completed else "[ ]"
                priority = f"[{todo.priority[:3].upper()}]"
                tags_str = ",".join(todo.tags[:2])
                if len(todo.tags) > 2:
                    tags_str += "..."
                due_date_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
                title = todo.title[:20]
                description = (todo.description[:20] if todo.description else "")[:20]
                print(f"{index:<2} | {status}    | {priority:<7}  | {tags_str:<17} | {due_date_str:<10} | {title:<22} | {description}")

        except Exception as e:
            print(f"\n✗ Error searching tasks: {str(e)}")

    def handle_filter_tasks(self):
        """Handle filtering tasks by criteria."""
        print("\n--- Filter Tasks ---")

        print("Filter by status (leave blank to skip):")
        status = input("Enter status (complete/incomplete): ").strip().lower()
        if status and status not in ['complete', 'incomplete']:
            print("Invalid status. Skipping status filter.")
            status = None

        print("Filter by priority (leave blank to skip):")
        priority = input("Enter priority (high/medium/low): ").strip().lower()
        if priority and priority not in ['high', 'medium', 'low']:
            print("Invalid priority. Skipping priority filter.")
            priority = None

        print("Filter by tags (leave blank to skip):")
        tags_input = input("Enter tags separated by commas: ").strip()
        tags = []
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        try:
            filtered_todos = self.todo_service.filter_todos(status=status, priority=priority, tags=tags)

            if not filtered_todos:
                print("No tasks match the specified filters.")
                return

            print(f"\nFound {len(filtered_todos)} task(s) matching the filters:")
            print("\n#  | Status | Priority | Tags              | Due Date   | Title                    | Description")
            print("-" * 120)

            for index, todo in enumerate(filtered_todos, start=1):
                status = "[✓]" if todo.completed else "[ ]"
                priority = f"[{todo.priority[:3].upper()}]"
                tags_str = ",".join(todo.tags[:2])
                if len(todo.tags) > 2:
                    tags_str += "..."
                due_date_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
                title = todo.title[:20]
                description = (todo.description[:20] if todo.description else "")[:20]
                print(f"{index:<2} | {status}    | {priority:<7}  | {tags_str:<17} | {due_date_str:<10} | {title:<22} | {description}")

        except Exception as e:
            print(f"\n✗ Error filtering tasks: {str(e)}")

    def handle_sort_tasks(self):
        """Handle sorting tasks by criteria."""
        print("\n--- Sort Tasks ---")
        print("Sort by:")
        print("1. Title (alphabetical)")
        print("2. Priority")
        print("3. Due Date")

        choice = input("Enter your choice (1-3): ").strip()

        sort_criteria = {
            '1': 'title',
            '2': 'priority',
            '3': 'due_date'
        }

        if choice not in sort_criteria:
            print("Invalid choice. Sorting by title by default.")
            sort_by = 'title'
        else:
            sort_by = sort_criteria[choice]

        try:
            sorted_todos = self.todo_service.sort_todos(by=sort_by)

            if not sorted_todos:
                print("No tasks to display.")
                return

            print(f"\nTasks sorted by {sort_by}:")
            print("\n#  | Status | Priority | Tags              | Due Date   | Title                    | Description")
            print("-" * 120)

            for index, todo in enumerate(sorted_todos, start=1):
                status = "[✓]" if todo.completed else "[ ]"
                priority = f"[{todo.priority[:3].upper()}]"
                tags_str = ",".join(todo.tags[:2])
                if len(todo.tags) > 2:
                    tags_str += "..."
                due_date_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
                title = todo.title[:20]
                description = (todo.description[:20] if todo.description else "")[:20]
                print(f"{index:<2} | {status}    | {priority:<7}  | {tags_str:<17} | {due_date_str:<10} | {title:<22} | {description}")

        except Exception as e:
            print(f"\n✗ Error sorting tasks: {str(e)}")

    def handle_view_reminders(self):
        """Handle viewing tasks with upcoming due dates."""
        print("\n--- View Reminders ---")

        # Process recurring tasks to create new instances if needed
        self.todo_service.process_recurring_tasks()

        # Get todos due within the next 7 days
        due_soon_todos = self.todo_service.get_todos_due_soon(days=7)

        if not due_soon_todos:
            print("No upcoming tasks due soon.")
            return

        print(f"\nFound {len(due_soon_todos)} task(s) due soon:")
        print("\n#  | Status | Priority | Due Date   | Title                    | Description")
        print("-" * 90)

        for index, todo in enumerate(due_soon_todos, start=1):
            status = "[✓]" if todo.completed else "[ ]"
            priority = f"[{todo.priority[:3].upper()}]"
            due_date_str = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
            title = todo.title[:20]
            description = (todo.description[:25] if todo.description else "")[:25]
            print(f"{index:<2} | {status}    | {priority:<7}  | {due_date_str:<10} | {title:<22} | {description}")

    # The following methods are kept for backward compatibility with tests
    # They maintain the same interface as the original command-driven approach
    def handle_add(self, args: List[str]) -> str:
        """
        Handle the 'add' command to create a new todo.
        Expected: add "title" ["description"] ["priority"] ["due_date"] ["recurring"]
        """
        if len(args) < 1:
            return "Error: 'add' command requires at least a title. Usage: add \"title\" [\"description\"] [\"priority\"] [\"due_date\"] [\"recurring\"]"

        title = args[0]
        description = args[1] if len(args) > 1 else None
        priority = args[2] if len(args) > 2 else "medium"
        due_date = args[3] if len(args) > 3 else None
        recurring = args[4] if len(args) > 4 else None

        # Parse tags from title if in format "title[tag1,tag2]"
        tags = []
        import re
        tag_pattern = r'\[(.*?)\]'
        tag_match = re.search(tag_pattern, title)
        if tag_match:
            tags_str = tag_match.group(1)
            tags = [tag.strip() for tag in tags_str.split(',')]
            title = re.sub(tag_pattern, '', title).strip()

        try:
            todo = self.todo_service.create_todo(title, description, priority, tags, due_date, recurring)
            return f"Added todo: {todo.id[:8]} - {todo.title} [P:{todo.priority}]"
        except Exception as e:
            return f"Error adding todo: {str(e)}"

    def handle_list(self) -> str:
        """
        Handle the 'list' command to show all todos.
        """
        todos = self.todo_service.get_all_todos()

        if not todos:
            return "No todos found."

        result = []
        result.append("#\tStatus\tPriority\tTags\tDue Date\tTitle\tDescription")
        result.append("-" * 100)

        for index, todo in enumerate(todos, start=1):
            status = "C" if todo.completed else "I"  # C = Complete, I = Incomplete
            priority = todo.priority
            tags = ",".join(todo.tags) if todo.tags else ""
            due_date = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
            description = todo.description if todo.description else ""
            result.append(f"{index}\t{status}\t{priority}\t{tags}\t{due_date}\t{todo.title}\t{description}")

        return "\n".join(result)

    def handle_update(self, args: List[str]) -> str:
        """
        Handle the 'update' command to update a todo.
        Expected: update "id" ["title"] ["description"] ["priority"] ["due_date"] ["recurring"]
        """
        if len(args) < 1:
            return "Error: 'update' command requires an ID. Usage: update id [\"title\"] [\"description\"] [\"priority\"] [\"due_date\"] [\"recurring\"]"

        todo_id = args[0]
        new_title = args[1] if len(args) > 1 else None
        new_description = args[2] if len(args) > 2 else None
        new_priority = args[3] if len(args) > 3 else None
        new_due_date = args[4] if len(args) > 4 else None
        new_recurring = args[5] if len(args) > 5 else None

        # Only update if at least one field is provided
        if all(field is None for field in [new_title, new_description, new_priority, new_due_date, new_recurring]):
            return "Error: 'update' command requires at least one field to update."

        try:
            updated_todo = self.todo_service.update_todo(todo_id, new_title, new_description, new_priority, None, new_due_date, new_recurring)
            if updated_todo:
                return f"Updated todo: {updated_todo.id[:8]} - {updated_todo.title} [P:{updated_todo.priority}]"
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except Exception as e:
            return f"Error updating todo: {str(e)}"

    def handle_delete(self, args: List[str]) -> str:
        """
        Handle the 'delete' command to delete a todo.
        Expected: delete "id"
        """
        if len(args) < 1:
            return "Error: 'delete' command requires an ID. Usage: delete id"

        todo_id = args[0]

        try:
            success = self.todo_service.delete_todo(todo_id)
            if success:
                return f"Deleted todo with ID: {todo_id}"
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except Exception as e:
            return f"Error deleting todo: {str(e)}"

    def handle_complete(self, args: List[str]) -> str:
        """
        Handle the 'complete' command to mark a todo as complete.
        Expected: complete "id"
        """
        if len(args) < 1:
            return "Error: 'complete' command requires an ID. Usage: complete id"

        todo_id = args[0]

        try:
            completed_todo = self.todo_service.complete_todo(todo_id)
            if completed_todo:
                return f"Marked todo as complete: {completed_todo.id} - {completed_todo.title}"
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except Exception as e:
            return f"Error marking todo as complete: {str(e)}"

    def handle_incomplete(self, args: List[str]) -> str:
        """
        Handle the 'incomplete' command to mark a todo as incomplete.
        Expected: incomplete "id"
        """
        if len(args) < 1:
            return "Error: 'incomplete' command requires an ID. Usage: incomplete id"

        todo_id = args[0]

        try:
            incomplete_todo = self.todo_service.incomplete_todo(todo_id)
            if incomplete_todo:
                return f"Marked todo as incomplete: {incomplete_todo.id} - {incomplete_todo.title}"
            else:
                return f"Error: Todo with ID {todo_id} not found."
        except Exception as e:
            return f"Error marking todo as incomplete: {str(e)}"

    def show_help(self) -> str:
        """
        Show help information for available commands.
        """
        help_text = """
Available commands:
  add "title" ["description"] ["priority"] ["due_date"] ["recurring"] - Add a new todo with optional fields
  list                         - List all todos
  update id ["title"] ["description"] ["priority"] ["due_date"] ["recurring"] - Update a todo
  delete id                    - Delete a todo
  complete id                  - Mark a todo as complete
  incomplete id                - Mark a todo as incomplete
  search "keyword"             - Search todos by keyword in title/description
  filter [status] [priority] [tags] - Filter todos by criteria
  sort [priority|due_date|title] - Sort todos by specified criteria
  help                         - Show this help message
  exit/quit                    - Exit the application

Examples:
  add "Buy groceries" "Milk, bread, eggs" "high" "2024-12-25" "weekly"
  list
  complete 123e4567-e89b-12d3-a456-426614174000
  update 123e4567-e89b-12d3-a456-426614174000 "New title" "New desc" "low" "2024-12-31" "monthly"
  delete 123e4567-e89b-12d3-a456-426614174000
  search "groceries"
  filter complete high "work,personal"
  sort priority
        """
        return help_text.strip()

    def parse_command(self, args: List[str]) -> Optional[str]:
        """
        Parse command line arguments and execute the appropriate command.
        This method is kept for backward compatibility with tests and command-line usage.
        """
        if not args:
            return self.show_help()

        command = args[0].lower()

        if command == "add":
            return self.handle_add(args[1:])
        elif command == "list":
            return self.handle_list()
        elif command == "update":
            return self.handle_update(args[1:])
        elif command == "delete":
            return self.handle_delete(args[1:])
        elif command == "complete":
            return self.handle_complete(args[1:])
        elif command == "incomplete":
            return self.handle_incomplete(args[1:])
        elif command == "search":
            return self.handle_search_command(args[1:])
        elif command == "filter":
            return self.handle_filter_command(args[1:])
        elif command == "sort":
            return self.handle_sort_command(args[1:])
        elif command == "help":
            return self.show_help()
        elif command == "exit" or command == "quit":
            return "Goodbye!"
        else:
            return f"Unknown command: {command}. Use 'help' for available commands."

    def handle_search_command(self, args: List[str]) -> str:
        """
        Handle the 'search' command to search todos by keyword.
        Expected: search "keyword"
        """
        if len(args) < 1:
            return "Error: 'search' command requires a keyword. Usage: search \"keyword\""

        keyword = args[0]

        try:
            matching_todos = self.todo_service.search_todos(keyword)

            if not matching_todos:
                return f"No todos found containing '{keyword}'."

            result = []
            result.append(f"Found {len(matching_todos)} task(s) containing '{keyword}':")
            result.append("#\tStatus\tPriority\tTags\tDue Date\tTitle\tDescription")
            result.append("-" * 100)

            for index, todo in enumerate(matching_todos, start=1):
                status = "C" if todo.completed else "I"  # C = Complete, I = Incomplete
                priority = todo.priority
                tags = ",".join(todo.tags) if todo.tags else ""
                due_date = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
                description = todo.description if todo.description else ""
                result.append(f"{index}\t{status}\t{priority}\t{tags}\t{due_date}\t{todo.title}\t{description}")

            return "\n".join(result)
        except Exception as e:
            return f"Error searching todos: {str(e)}"

    def handle_filter_command(self, args: List[str]) -> str:
        """
        Handle the 'filter' command to filter todos by criteria.
        Expected: filter [status] [priority] [tags]
        """
        status = args[0] if len(args) > 0 and args[0] in ['complete', 'incomplete'] else None
        priority = args[1] if len(args) > 1 and args[1] in ['high', 'medium', 'low'] else None
        tags_str = args[2] if len(args) > 2 else None

        tags = []
        if tags_str:
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        try:
            filtered_todos = self.todo_service.filter_todos(status=status, priority=priority, tags=tags)

            if not filtered_todos:
                return "No todos match the specified filters."

            result = []
            result.append(f"Found {len(filtered_todos)} task(s) matching the filters:")
            result.append("#\tStatus\tPriority\tTags\tDue Date\tTitle\tDescription")
            result.append("-" * 100)

            for index, todo in enumerate(filtered_todos, start=1):
                status = "C" if todo.completed else "I"  # C = Complete, I = Incomplete
                priority = todo.priority
                todo_tags = ",".join(todo.tags) if todo.tags else ""
                due_date = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
                description = todo.description if todo.description else ""
                result.append(f"{index}\t{status}\t{priority}\t{todo_tags}\t{due_date}\t{todo.title}\t{description}")

            return "\n".join(result)
        except Exception as e:
            return f"Error filtering todos: {str(e)}"

    def handle_sort_command(self, args: List[str]) -> str:
        """
        Handle the 'sort' command to sort todos by criteria.
        Expected: sort [priority|due_date|title]
        """
        sort_by = args[0] if len(args) > 0 and args[0] in ['priority', 'due_date', 'title'] else 'title'

        try:
            sorted_todos = self.todo_service.sort_todos(by=sort_by)

            if not sorted_todos:
                return "No todos to display."

            result = []
            result.append(f"Todos sorted by {sort_by}:")
            result.append("#\tStatus\tPriority\tTags\tDue Date\tTitle\tDescription")
            result.append("-" * 100)

            for index, todo in enumerate(sorted_todos, start=1):
                status = "C" if todo.completed else "I"  # C = Complete, I = Incomplete
                priority = todo.priority
                tags = ",".join(todo.tags) if todo.tags else ""
                due_date = todo.due_date.strftime('%Y-%m-%d') if todo.due_date else ""
                description = todo.description if todo.description else ""
                result.append(f"{index}\t{status}\t{priority}\t{tags}\t{due_date}\t{todo.title}\t{description}")

            return "\n".join(result)
        except Exception as e:
            return f"Error sorting todos: {str(e)}"

    def run_interactive(self):
        """
        Run the interactive menu-driven console loop.
        """
        while True:
            # Process recurring tasks to create new instances if needed
            self.todo_service.process_recurring_tasks()

            self.display_header()
            self.display_menu()

            choice = self.get_user_choice()

            if choice == '1':
                self.handle_add_task()
            elif choice == '2':
                self.handle_view_tasks()
            elif choice == '3':
                self.handle_update_task()
            elif choice == '4':
                self.handle_delete_task()
            elif choice == '5':
                self.handle_toggle_complete()
            elif choice == '6':
                # Features submenu
                while True:
                    # Process recurring tasks to create new instances if needed
                    self.todo_service.process_recurring_tasks()

                    self.display_header()
                    self.display_features_menu()

                    feature_choice = self.get_features_choice()

                    if feature_choice == '1':
                        self.handle_set_priority()
                    elif feature_choice == '2':
                        self.handle_manage_tags()
                    elif feature_choice == '3':
                        self.handle_set_due_date()
                    elif feature_choice == '4':
                        self.handle_set_recurring()
                    elif feature_choice == '5':
                        self.handle_search_tasks()
                    elif feature_choice == '6':
                        self.handle_filter_tasks()
                    elif feature_choice == '7':
                        self.handle_sort_tasks()
                    elif feature_choice == '8':
                        self.handle_view_reminders()
                    elif feature_choice == '9':
                        # Back to main menu
                        break

                    # Pause after each action to allow user to see results
                    self.pause_for_user_input()
            elif choice == '7':
                print("\nGoodbye!")
                break

            # Pause after each action to allow user to see results
            self.pause_for_user_input()
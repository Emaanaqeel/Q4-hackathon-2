# Tasks: Phase I – In-Memory Python Console-Based Todo Application

**Feature**: Phase I – In-Memory Python Console-Based Todo Application
**Branch**: 1-todo-app
**Created**: 2026-01-01
**Status**: Generated
**Plan**: [specs/1-todo-app/plan.md](./plan.md)
**Spec**: [specs/1-todo-app/spec.md](./spec.md)

## Phase 1: Setup

**Goal**: Initialize repository structure and Python project environment

**Independent Test**: Project structure matches specification and Python application runs with minimal entry point

**Tasks**:

- [X] T001 Create repository structure with required directories: src/, specs-history/, tests/
- [X] T002 Create placeholder files: README.md, CLAUDE.md, .gitignore
- [X] T003 Create the Python package structure: src/todo_app/, src/todo_app/domain/, src/todo_app/application/, src/todo_app/infrastructure/
- [X] T004 Initialize __init__.py files in all package directories
- [X] T005 Create pyproject.toml for Python 3.13+ project with UV
- [X] T006 Create basic main.py entry point that prints "Todo App Started"
- [X] T007 Verify project runs with python -m src.todo_app.main

## Phase 2: Foundational

**Goal**: Implement core domain models and in-memory storage infrastructure

**Independent Test**: Domain models are correctly defined and in-memory storage works without console interface

**Tasks**:

- [X] T008 [P] Create Todo domain model in src/todo_app/domain/models.py with id, title, description, completed fields
- [X] T009 [P] Create domain exceptions in src/todo_app/domain/exceptions.py for validation errors
- [X] T010 [P] Implement in-memory storage in src/todo_app/infrastructure/storage.py using Python data structures
- [X] T011 [P] Create TodoRepository interface in src/todo_app/application/repositories.py
- [X] T012 [P] Implement TodoRepository with in-memory storage in src/todo_app/application/repositories.py
- [X] T013 [P] Create TodoService interface in src/todo_app/application/services.py
- [X] T014 [P] Implement basic TodoService in src/todo_app/application/services.py with placeholder methods

## Phase 3: User Story 1 - Add Todo Items (Priority: P1)

**Goal**: Enable users to create new todo items with a title and optional description through the console interface

**Independent Test**: Can run the application, enter an "add" command, provide a title and description, and verify that the item appears in the list with a unique ID and incomplete status

**Tasks**:

- [X] T015 [P] [US1] Implement create_todo method in TodoService with validation for title length (1-100 chars)
- [X] T016 [P] [US1] Implement validation for description length (0-500 chars) in TodoService
- [X] T017 [P] [US1] Add unique ID generation in Todo model and repository
- [X] T018 [P] [US1] Set default status to incomplete when creating new todos
- [X] T019 [P] [US1] Create add command parsing in console interface
- [X] T020 [US1] Implement console command handler for "add" with title and optional description parameters
- [X] T021 [US1] Add success feedback when todo is added successfully
- [X] T022 [US1] Test User Story 1 acceptance scenario 1: Add todo with title creates item with unique ID and incomplete status
- [X] T023 [US1] Test User Story 1 acceptance scenario 2: Add todo with title and description creates complete item

## Phase 4: User Story 2 - View Todo Items (Priority: P1)

**Goal**: Allow users to see all their todo items in a clear, organized format that shows the ID, title, description, and completion status of each item

**Independent Test**: Can add one or more todo items and then use the "list" command to display all items with their complete information

**Tasks**:

- [X] T024 [P] [US2] Implement get_all_todos method in TodoService
- [X] T025 [P] [US2] Format todo display with ID, title, description, and completion status
- [X] T026 [P] [US2] Create list command parsing in console interface
- [X] T027 [US2] Implement console command handler for "list"
- [X] T028 [US2] Display message when no todo items exist
- [X] T029 [US2] Test User Story 2 acceptance scenario 1: List command shows all todos with complete information
- [X] T030 [US2] Test User Story 2 acceptance scenario 2: List command shows empty message when no todos exist

## Phase 5: User Story 3 - Update Todo Items (Priority: P2)

**Goal**: Allow users to modify the title or description of an existing todo item by identifying it with its unique ID

**Independent Test**: Can add a todo item, use an "update" command with the item's ID and new information, and verify that the item is updated in the list

**Tasks**:

- [X] T031 [P] [US3] Implement update_todo method in TodoService with validation
- [X] T032 [P] [US3] Implement update functionality in TodoRepository
- [X] T033 [P] [US3] Create update command parsing in console interface
- [X] T034 [US3] Implement console command handler for "update" with ID, new title, and new description parameters
- [X] T035 [US3] Preserve unchanged fields when updating a todo
- [X] T036 [US3] Test User Story 3 acceptance scenario 1: Update command with ID and new title updates only the title
- [X] T037 [US3] Test User Story 3 acceptance scenario 2: Update command with ID and new description updates only the description

## Phase 6: User Story 4 - Mark Todo Items Complete/Incomplete (Priority: P2)

**Goal**: Allow users to mark todo items as complete when finished, or mark them as incomplete if they need more work

**Independent Test**: Can add a todo item, use a "complete" or "incomplete" command with the item's ID, and verify that the status is updated

**Tasks**:

- [X] T038 [P] [US4] Implement complete_todo method in TodoService
- [X] T039 [P] [US4] Implement incomplete_todo method in TodoService
- [X] T040 [P] [US4] Implement mark_complete/mark_incomplete methods in TodoRepository
- [X] T041 [P] [US4] Create complete and incomplete command parsing in console interface
- [X] T042 [US4] Implement console command handler for "complete" with ID parameter
- [X] T043 [US4] Implement console command handler for "incomplete" with ID parameter
- [X] T044 [US4] Test User Story 4 acceptance scenario 1: Complete command changes incomplete item to complete
- [X] T045 [US4] Test User Story 4 acceptance scenario 2: Incomplete command changes complete item to incomplete

## Phase 7: User Story 5 - Delete Todo Items (Priority: P3)

**Goal**: Allow users to remove todo items that are no longer needed from their list

**Independent Test**: Can add a todo item, use a "delete" command with the item's ID, and verify that the item is removed from the list

**Tasks**:

- [X] T046 [P] [US5] Implement delete_todo method in TodoService
- [X] T047 [P] [US5] Implement delete functionality in TodoRepository
- [X] T048 [P] [US5] Create delete command parsing in console interface
- [X] T049 [US5] Implement console command handler for "delete" with ID parameter
- [X] T050 [US5] Verify item no longer appears in listings after deletion
- [X] T051 [US5] Test User Story 5 acceptance scenario 1: Delete command removes item from list

## Phase 8: Validation and Error Handling

**Goal**: Implement proper validation and error handling for all operations

**Independent Test**: All error conditions are handled gracefully with appropriate user feedback

**Tasks**:

- [X] T052 [P] Add validation for invalid todo IDs in all operations
- [X] T053 [P] Implement error handling for non-existent todo IDs
- [X] T054 [P] Add validation for title/description length constraints (100/500 chars)
- [X] T055 [P] Implement error handling for malformed commands
- [X] T056 [P] Add error messages for missing command parameters
- [X] T057 Create comprehensive error handling in console interface
- [X] T058 Test error case: Attempt to update/delete/complete non-existent todo shows clear error message
- [X] T059 Test error case: Title exceeding 100 characters shows validation error
- [X] T060 Test error case: Invalid command syntax shows helpful error message

## Phase 9: Integration and Console Interface

**Goal**: Connect all components together and create a cohesive console experience

**Independent Test**: All functionality works together through the console interface

**Tasks**:

- [X] T061 [P] Create console command loop in main application
- [X] T062 [P] Wire TodoService to console interface
- [X] T063 [P] Format console output consistently across all commands
- [X] T064 Implement exit command to terminate the application
- [X] T065 Create help command to show available commands
- [X] T066 Integrate all command handlers into main console loop
- [X] T067 Test complete workflow: add, list, update, complete, delete, list again

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Finalize the application with proper documentation, testing, and quality improvements

**Independent Test**: Application is complete and ready for use with all requirements satisfied

**Tasks**:

- [X] T068 Add comprehensive docstrings to all classes and methods
- [X] T069 Create unit tests for domain models in tests/unit/domain/
- [X] T070 Create unit tests for application services in tests/unit/application/
- [X] T071 Create unit tests for infrastructure components in tests/unit/infrastructure/
- [X] T072 Create integration tests in tests/integration/test_end_to_end.py
- [X] T073 Update README.md with setup and usage instructions
- [X] T074 Verify all functional requirements (FR-001 through FR-016) are implemented
- [X] T075 Test all success criteria (SC-001 through SC-006) are met
- [X] T076 Run complete application test with all user stories working
- [X] T077 Verify performance goals are met (<100ms response time)

## Dependencies

- User Story 2 (View) depends on User Story 1 (Add) being partially complete (need to be able to create items to view them)
- User Stories 3, 4, 5 (Update, Complete, Delete) depend on User Story 1 (Add) being complete (need to create items first)
- All user stories depend on foundational domain models and repository being complete

## Parallel Execution Examples

- Tasks T008-T014 can be executed in parallel as they implement different components in different files
- User Story tasks can be developed in parallel after foundational tasks are complete
- Test tasks can be developed in parallel with implementation tasks for the same user story

## Implementation Strategy

1. Start with Phase 1 and 2 to establish the foundation
2. Implement User Story 1 (P1 priority) as the MVP
3. Add User Story 2 (P1 priority) to complete basic functionality
4. Implement remaining user stories (P2, P3) in order
5. Add validation, error handling, and polish
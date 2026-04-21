import unittest
from datetime import datetime, timedelta

# You will need to adjust this import based on your actual file
# Example:
# from task_manager.app import calculateTaskScore, sortTasksByImportance, getTopPriorityTasks

# Mock Task object for testing
class MockTask:
    def __init__(self, priority, status, due_date=None, tags=None, updated_at=None, assigned_to=None):
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.tags = tags or []
        self.updated_at = updated_at or datetime.now()
        self.assigned_to = assigned_to
        self.completed_at = None

# Example enum-like values (adjust if needed)
class TaskPriority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class TaskStatus:
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

# Import your actual functions here
from task_manager.app import calculateTaskScore, sortTasksByImportance, getTopPriorityTasks


class TestTaskPriority(unittest.TestCase):

    def test_basic_priority(self):
        low_task = MockTask(TaskPriority.LOW, TaskStatus.TODO)
        high_task = MockTask(TaskPriority.HIGH, TaskStatus.TODO)

        self.assertGreater(calculateTaskScore(high_task), calculateTaskScore(low_task))

    def test_overdue_task(self):
        overdue = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            due_date=datetime.now() - timedelta(days=1)
        )

        normal = MockTask(TaskPriority.MEDIUM, TaskStatus.TODO)

        self.assertGreater(calculateTaskScore(overdue), calculateTaskScore(normal))

    def test_due_soon(self):
        soon = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            due_date=datetime.now() + timedelta(days=1)
        )

        later = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            due_date=datetime.now() + timedelta(days=10)
        )

        self.assertGreater(calculateTaskScore(soon), calculateTaskScore(later))

    def test_completed_penalty(self):
        done_task = MockTask(TaskPriority.HIGH, TaskStatus.DONE)
        active_task = MockTask(TaskPriority.HIGH, TaskStatus.TODO)

        self.assertLess(calculateTaskScore(done_task), calculateTaskScore(active_task))

    def test_tag_boost(self):
        tagged = MockTask(TaskPriority.MEDIUM, TaskStatus.TODO, tags=["urgent"])
        normal = MockTask(TaskPriority.MEDIUM, TaskStatus.TODO)

        self.assertGreater(calculateTaskScore(tagged), calculateTaskScore(normal))

    def test_recent_update(self):
        recent = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            updated_at=datetime.now()
        )

        old = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            updated_at=datetime.now() - timedelta(days=5)
        )

        self.assertGreater(calculateTaskScore(recent), calculateTaskScore(old))

    def test_sort_tasks(self):
        task1 = MockTask(TaskPriority.LOW, TaskStatus.TODO)
        task2 = MockTask(TaskPriority.HIGH, TaskStatus.TODO)

        sorted_tasks = sortTasksByImportance([task1, task2])

        self.assertEqual(sorted_tasks[0], task2)

    def test_top_tasks_limit(self):
        tasks = [
            MockTask(TaskPriority.LOW, TaskStatus.TODO),
            MockTask(TaskPriority.HIGH, TaskStatus.TODO),
            MockTask(TaskPriority.MEDIUM, TaskStatus.TODO)
        ]

        top_tasks = getTopPriorityTasks(tasks, limit=2)

        self.assertEqual(len(top_tasks), 2)

    def test_current_user_boost(self):
        assigned = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            assigned_to="me"
        )

        not_assigned = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            assigned_to="other"
        )

        self.assertGreater(calculateTaskScore(assigned), calculateTaskScore(not_assigned))

    def test_days_since_update_bug_fix(self):
        recent = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            updated_at=datetime.now()
        )

        old = MockTask(
            TaskPriority.MEDIUM,
            TaskStatus.TODO,
            updated_at=datetime.now() - timedelta(days=2)
        )

        self.assertGreater(calculateTaskScore(recent), calculateTaskScore(old))


if __name__ == "__main__":
    unittest.main()
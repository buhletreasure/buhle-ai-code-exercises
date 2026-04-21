# task_manager/app.py

# argparse is not actually used here (can be removed if needed)
import argparse

# Used for handling dates and time calculations
from datetime import datetime, timedelta

# Import the Task model and enums for priority and status
from .models import Task, TaskPriority, TaskStatus

# Import the storage class responsible for saving/loading tasks
from .storage import TaskStorage


class TaskManager:
    """
    This class contains all the business logic of the application.
    It acts as a middle layer between the CLI and the storage system.
    """

    def __init__(self, storage_path="tasks.json"):
        # Initialize storage (where tasks are saved)
        self.storage = TaskStorage(storage_path)

    def create_task(self, title, description="", priority_value=2,
                   due_date_str=None, tags=None):
        """
        Creates a new task using user input from the CLI.
        """

        # Convert numeric priority (1–4) into TaskPriority enum
        priority = TaskPriority(priority_value)

        # Initialize due date
        due_date = None

        # If user provided a due date, try to convert it to a datetime object
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError:
                # Handle invalid date format
                print("Invalid date format. Use YYYY-MM-DD")
                return None

        # Create a new Task object
        task = Task(title, description, priority, due_date, tags)

        # Save the task using storage and get the generated task ID
        task_id = self.storage.add_task(task)

        return task_id

    def list_tasks(self, status_filter=None, priority_filter=None, show_overdue=False):
        """
        Returns tasks based on filters (status, priority, overdue).
        """

        # If user wants only overdue tasks
        if show_overdue:
            return self.storage.get_overdue_tasks()

        # If filtering by status
        if status_filter:
            status = TaskStatus(status_filter)
            return self.storage.get_tasks_by_status(status)

        # If filtering by priority
        if priority_filter:
            priority = TaskPriority(priority_filter)
            return self.storage.get_tasks_by_priority(priority)

        # If no filters, return all tasks
        return self.storage.get_all_tasks()

    def update_task_status(self, task_id, new_status_value):
        """
        Updates the status of a task (e.g., todo → done).
        """

        # Convert input string into TaskStatus enum
        new_status = TaskStatus(new_status_value)

        # Special handling if marking task as DONE
        if new_status == TaskStatus.DONE:
            # Get the task from storage
            task = self.storage.get_task(task_id)

            if task:
                # Mark task as completed (likely sets completed_at timestamp)
                task.mark_as_done()

                # Save changes to storage
                self.storage.save()

                return True
        else:
            # For other statuses, update normally via storage
            return self.storage.update_task(task_id, status=new_status)

    def update_task_priority(self, task_id, new_priority_value):
        """
        Updates the priority of a task.
        """

        # Convert numeric value into TaskPriority enum
        new_priority = TaskPriority(new_priority_value)

        # Update task in storage
        return self.storage.update_task(task_id, priority=new_priority)

    def update_task_due_date(self, task_id, due_date_str):
        """
        Updates the due date of a task.
        """

        try:
            # Convert string into datetime object
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")

            # Update task in storage
            return self.storage.update_task(task_id, due_date=due_date)

        except ValueError:
            # Handle invalid date format
            print("Invalid date format. Use YYYY-MM-DD")
            return False

    def delete_task(self, task_id):
        """
        Deletes a task from storage.
        """
        return self.storage.delete_task(task_id)

    def get_task_details(self, task_id):
        """
        Retrieves a single task by its ID.
        """
        return self.storage.get_task(task_id)

    def add_tag_to_task(self, task_id, tag):
        """
        Adds a tag to a task.
        """

        # Retrieve task
        task = self.storage.get_task(task_id)

        if task:
            # Only add tag if it does not already exist
            if tag not in task.tags:
                task.tags.append(tag)

                # Save changes
                self.storage.save()

            return True

        return False

    def remove_tag_from_task(self, task_id, tag):
        """
        Removes a tag from a task.
        """

        task = self.storage.get_task(task_id)

        if task and tag in task.tags:
            task.tags.remove(tag)

            # Save changes
            self.storage.save()

            return True

        return False

    def get_statistics(self):
        """
        Generates statistics about tasks.
        """

        # Get all tasks from storage
        tasks = self.storage.get_all_tasks()

        # Total number of tasks
        total = len(tasks)

        # Count tasks grouped by status
        status_counts = {status.value: 0 for status in TaskStatus}
        for task in tasks:
            status_counts[task.status.value] += 1

        # Count tasks grouped by priority
        priority_counts = {priority.value: 0 for priority in TaskPriority}
        for task in tasks:
            priority_counts[task.priority.value] += 1

        # Count overdue tasks
        overdue_count = len([task for task in tasks if task.is_overdue()])

        # Count tasks completed in the last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)

        completed_recently = len([
            task for task in tasks
            if task.completed_at and task.completed_at >= seven_days_ago
        ])

        # Return all statistics as a dictionary
        return {
            "total": total,
            "by_status": status_counts,
            "by_priority": priority_counts,
            "overdue": overdue_count,
            "completed_last_week": completed_recently
        }
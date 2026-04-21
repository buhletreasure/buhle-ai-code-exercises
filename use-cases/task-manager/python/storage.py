# task_manager/storage.py

# json is used to save tasks into a JSON file and load them back
import json

# os is used to check whether the storage file exists
import os

# datetime is used to convert date strings back into datetime objects
from datetime import datetime

# Import the Task model and enums used during serialization/deserialization
from .models import Task, TaskPriority, TaskStatus


class TaskEncoder(json.JSONEncoder):
    """
    Custom JSON encoder used to convert Task objects into JSON-serializable dictionaries.
    """

    def default(self, obj):
        # If the object is a Task instance, convert it into a dictionary
        if isinstance(obj, Task):
            task_dict = obj.__dict__.copy()

            # Store enum values as plain values so they can be written to JSON
            task_dict['priority'] = obj.priority.value
            task_dict['status'] = obj.status.value

            # Convert datetime fields into ISO-format strings before saving
            for key in ['created_at', 'updated_at', 'due_date', 'completed_at']:
                if task_dict.get(key) is not None:
                    task_dict[key] = task_dict[key].isoformat()

            return task_dict

        # For all other object types, use the default JSON encoder behavior
        return super().default(obj)


class TaskDecoder(json.JSONDecoder):
    """
    Custom JSON decoder used to rebuild Task objects from JSON data.
    """

    def __init__(self, *args, **kwargs):
        # Register a custom object_hook so JSON objects can be converted into Task objects
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        # Check whether this JSON object looks like a task
        if 'id' in obj and 'title' in obj:
            # Create a basic Task object using title and description
            task = Task(obj['title'], obj.get('description', ''))

            # Restore stored values
            task.id = obj['id']
            task.priority = TaskPriority(obj['priority'])
            task.status = TaskStatus(obj['status'])

            # Convert stored ISO date strings back into datetime objects
            for key in ['created_at', 'updated_at', 'completed_at']:
                if obj.get(key):
                    setattr(task, key, datetime.fromisoformat(obj[key]))

            # Restore due date if it exists
            if obj.get('due_date'):
                task.due_date = datetime.fromisoformat(obj['due_date'])

            # Restore tags, or use an empty list if none exist
            task.tags = obj.get('tags', [])

            return task

        # If it is not a task-like object, return it unchanged
        return obj


class TaskStorage:
    """
    Handles saving, loading, updating, deleting, and retrieving tasks from storage.
    """

    def __init__(self, storage_path="tasks.json"):
        # Store the file path where tasks will be saved
        self.storage_path = storage_path

        # Keep tasks in memory using a dictionary keyed by task ID
        self.tasks = {}

        # Load existing tasks from the JSON file when storage starts
        self.load()

    def load(self):
        """
        Load tasks from the JSON file into memory.
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    # Read JSON data and convert it back into Task objects
                    tasks_data = json.load(f, cls=TaskDecoder)

                    # Store loaded tasks in the in-memory dictionary
                    if isinstance(tasks_data, list):
                        for task in tasks_data:
                            self.tasks[task.id] = task
            except Exception as e:
                print(f"Error loading tasks: {e}")

    def save(self):
        """
        Save all in-memory tasks into the JSON file.
        """
        try:
            with open(self.storage_path, 'w') as f:
                # Convert task objects into JSON and save them to file
                json.dump(list(self.tasks.values()), f, cls=TaskEncoder, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, task):
        """
        Add a new task to memory and save it to file.
        """
        self.tasks[task.id] = task
        self.save()
        return task.id

    def get_task(self, task_id):
        """
        Retrieve one task by its ID.
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id, **kwargs):
        """
        Update a task's fields, then save the changes.
        """
        task = self.get_task(task_id)
        if task:
            task.update(**kwargs)
            self.save()
            return True
        return False

    def delete_task(self, task_id):
        """
        Delete a task by ID, then save the updated task list.
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save()
            return True
        return False

    def get_all_tasks(self):
        """
        Return all tasks currently stored in memory.
        """
        return list(self.tasks.values())

    def get_tasks_by_status(self, status):
        """
        Return all tasks that match the given status.
        """
        return [task for task in self.tasks.values() if task.status == status]

    def get_tasks_by_priority(self, priority):
        """
        Return all tasks that match the given priority.
        """
        return [task for task in self.tasks.values() if task.priority == priority]

    def get_overdue_tasks(self):
        """
        Return all tasks that are overdue.
        """
        return [task for task in self.tasks.values() if task.is_overdue()]
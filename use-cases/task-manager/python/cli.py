# task_manager/cli.py

# argparse is used to build the command-line interface and parse user commands
import argparse

# datetime is imported in case date/time handling is needed in this CLI file
from datetime import datetime

# Import the main application logic class
from .app import TaskManager

# Import enums/models used for task status and priority formatting
from .models import TaskPriority, TaskStatus


def format_task(task):
    """
    Convert a task object into a readable string for terminal output.
    This is used when listing tasks or showing task details.
    """

    # Map each task status to a symbol for easier reading in the terminal
    status_symbol = {
        TaskStatus.TODO: "[ ]",
        TaskStatus.IN_PROGRESS: "[>]",
        TaskStatus.REVIEW: "[?]",
        TaskStatus.DONE: "[✓]"
    }

    # Map each task priority to visual exclamation markers
    priority_symbol = {
        TaskPriority.LOW: "!",
        TaskPriority.MEDIUM: "!!",
        TaskPriority.HIGH: "!!!",
        TaskPriority.URGENT: "!!!!"
    }

    # Format due date if it exists, otherwise show a default message
    due_str = f"Due: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else "No due date"

    # Format tags if they exist, otherwise show a default message
    tags_str = f"Tags: {', '.join(task.tags)}" if task.tags else "No tags"

    # Return the full formatted task display string
    return (
        f"{status_symbol[task.status]} {task.id[:8]} - {priority_symbol[task.priority]} {task.title}\n"
        f"  {task.description}\n"
        f"  {due_str} | {tags_str}\n"
        f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}"
    )


def main():
    """
    Main entry point for the Task Manager CLI.
    It defines all commands, parses user input, and routes the request
    to the appropriate TaskManager method.
    """

    # Create the top-level command parser
    parser = argparse.ArgumentParser(description="Task Manager CLI")

    # Create subcommands such as create, list, status, priority, etc.
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # =========================
    # Create task command
    # =========================

    # Defines the "create" command
    create_parser = subparsers.add_parser("create", help="Create a new task")

    # Required task title
    create_parser.add_argument("title", help="Task title")

    # Optional task description
    create_parser.add_argument("-d", "--description", help="Task description", default="")

    # Optional task priority with allowed values 1 to 4
    create_parser.add_argument(
        "-p",
        "--priority",
        help="Task priority (1-4)",
        type=int,
        choices=[1, 2, 3, 4],
        default=2
    )

    # Optional due date in YYYY-MM-DD format
    create_parser.add_argument("-u", "--due", help="Due date (YYYY-MM-DD)", default=None)

    # Optional comma-separated tags
    create_parser.add_argument("-t", "--tags", help="Comma-separated tags", default="")

    # =========================
    # List tasks command
    # =========================

    # Defines the "list" command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Optional filter by task status
    list_parser.add_argument(
        "-s",
        "--status",
        help="Filter by status",
        choices=["todo", "in_progress", "review", "done"]
    )

    # Optional filter by task priority
    list_parser.add_argument(
        "-p",
        "--priority",
        help="Filter by priority",
        type=int,
        choices=[1, 2, 3, 4]
    )

    # Optional flag to show only overdue tasks
    list_parser.add_argument(
        "-o",
        "--overdue",
        help="Show only overdue tasks",
        action="store_true"
    )

    # =========================
    # Update task commands
    # =========================

    # Defines the "status" command for updating a task's status
    update_status_parser = subparsers.add_parser("status", help="Update task status")
    update_status_parser.add_argument("task_id", help="Task ID")
    update_status_parser.add_argument(
        "status",
        help="New status",
        choices=["todo", "in_progress", "review", "done"]
    )

    # Defines the "priority" command for updating task priority
    update_priority_parser = subparsers.add_parser("priority", help="Update task priority")
    update_priority_parser.add_argument("task_id", help="Task ID")
    update_priority_parser.add_argument(
        "priority",
        help="New priority",
        type=int,
        choices=[1, 2, 3, 4]
    )

    # Defines the "due" command for updating task due date
    update_due_parser = subparsers.add_parser("due", help="Update task due date")
    update_due_parser.add_argument("task_id", help="Task ID")
    update_due_parser.add_argument("due_date", help="New due date (YYYY-MM-DD)")

    # =========================
    # Tag management commands
    # =========================

    # Defines the "tag" command for adding a tag to a task
    add_tag_parser = subparsers.add_parser("tag", help="Add tag to task")
    add_tag_parser.add_argument("task_id", help="Task ID")
    add_tag_parser.add_argument("tag", help="Tag to add")

    # Defines the "untag" command for removing a tag from a task
    remove_tag_parser = subparsers.add_parser("untag", help="Remove tag from task")
    remove_tag_parser.add_argument("task_id", help="Task ID")
    remove_tag_parser.add_argument("tag", help="Tag to remove")

    # =========================
    # Other commands
    # =========================

    # Defines the "show" command for viewing a single task
    show_parser = subparsers.add_parser("show", help="Show task details")
    show_parser.add_argument("task_id", help="Task ID")

    # Defines the "delete" command for deleting a task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID")

    # Defines the "stats" command for showing task statistics
    stats_parser = subparsers.add_parser("stats", help="Show task statistics")

    # Parse the command-line arguments entered by the user
    args = parser.parse_args()

    # Create an instance of the main TaskManager class
    # This object performs the real task operations
    task_manager = TaskManager()

    # =========================
    # Handle "create" command
    # =========================
    if args.command == "create":
        # Convert comma-separated tags into a clean Python list
        tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else []

        # Ask TaskManager to create the new task
        task_id = task_manager.create_task(
            args.title,
            args.description,
            args.priority,
            args.due,
            tags
        )

        # If creation succeeds, display the new task ID
        if task_id:
            print(f"Created task with ID: {task_id}")

    # =========================
    # Handle "list" command
    # =========================
    elif args.command == "list":
        # Retrieve tasks using optional filters
        tasks = task_manager.list_tasks(args.status, args.priority, args.overdue)

        # If matching tasks exist, print each formatted task
        if tasks:
            for task in tasks:
                print(format_task(task))
                print("-" * 50)
        else:
            print("No tasks found matching the criteria.")

    # =========================
    # Handle "status" command
    # =========================
    elif args.command == "status":
        # Update the status of the specified task
        if task_manager.update_task_status(args.task_id, args.status):
            print(f"Updated task status to {args.status}")
        else:
            print("Failed to update task status. Task not found.")

    # =========================
    # Handle "priority" command
    # =========================
    elif args.command == "priority":
        # Update the priority of the specified task
        if task_manager.update_task_priority(args.task_id, args.priority):
            print(f"Updated task priority to {args.priority}")
        else:
            print("Failed to update task priority. Task not found.")

    # =========================
    # Handle "due" command
    # =========================
    elif args.command == "due":
        # Update the due date of the specified task
        if task_manager.update_task_due_date(args.task_id, args.due_date):
            print(f"Updated task due date to {args.due_date}")
        else:
            print("Failed to update task due date. Task not found or invalid date.")

    # =========================
    # Handle "tag" command
    # =========================
    elif args.command == "tag":
        # Add a tag to the specified task
        if task_manager.add_tag_to_task(args.task_id, args.tag):
            print(f"Added tag '{args.tag}' to task")
        else:
            print("Failed to add tag. Task not found.")

    # =========================
    # Handle "untag" command
    # =========================
    elif args.command == "untag":
        # Remove a tag from the specified task
        if task_manager.remove_tag_from_task(args.task_id, args.tag):
            print(f"Removed tag '{args.tag}' from task")
        else:
            print("Failed to remove tag. Task or tag not found.")

    # =========================
    # Handle "show" command
    # =========================
    elif args.command == "show":
        # Retrieve one task by ID
        task = task_manager.get_task_details(args.task_id)

        # If found, display the formatted task
        if task:
            print(format_task(task))
        else:
            print("Task not found.")

    # =========================
    # Handle "delete" command
    # =========================
    elif args.command == "delete":
        # Delete the specified task
        if task_manager.delete_task(args.task_id):
            print(f"Deleted task {args.task_id}")
        else:
            print("Failed to delete task. Task not found.")

    # =========================
    # Handle "stats" command
    # =========================
    elif args.command == "stats":
        # Get summary statistics from TaskManager
        stats = task_manager.get_statistics()

        # Print overall number of tasks
        print(f"Total tasks: {stats['total']}")

        # Print task counts grouped by status
        print(f"By status:")
        for status, count in stats['by_status'].items():
            print(f"  {status}: {count}")

        # Print task counts grouped by priority
        print(f"By priority:")
        for priority, count in stats['by_priority'].items():
            print(f"  {priority}: {count}")

        # Print overdue and recently completed task info
        print(f"Overdue tasks: {stats['overdue']}")
        print(f"Completed in last 7 days: {stats['completed_last_week']}")

    # If no valid command is provided, show help information
    else:
        parser.print_help()


# Run the CLI only when this file is executed directly
if __name__ == "__main__":
    main()
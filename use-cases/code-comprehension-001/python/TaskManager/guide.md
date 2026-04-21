# How to Create and Manage Tasks

## Step 1: Create a Task
python cli.py create "My Task" --priority 2

## Step 2: View Tasks
python cli.py list

## Step 3: Update Task Status
python cli.py update-status <task_id> done

## Step 4: Add a Tag
python cli.py add-tag <task_id> "important"

## Step 5: Filter Tasks
python cli.py list --priority 3

## Common Mistakes
- Wrong date format (YYYY-MM-DD)
- Invalid task ID
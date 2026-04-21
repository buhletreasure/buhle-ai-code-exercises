# Task 9: Test Plan

## Functions Under Test
- `calculateTaskScore`
- `sortTasksByImportance`
- `getTopPriorityTasks`

---

## Test Cases for `calculateTaskScore`

### 1. Basic priority score
- **Priority:** High
- **Type:** Unit test
- **What to test:** A task with a normal priority should get the correct base score
- **Expected outcome:** Higher priority should produce a higher score than lower priority

### 2. Overdue task boost
- **Priority:** High
- **Type:** Unit test
- **What to test:** A task with a due date in the past should receive an overdue boost
- **Expected outcome:** Overdue tasks should have a higher score than similar tasks with no due date

### 3. Due today / due soon behavior
- **Priority:** High
- **Type:** Unit test
- **What to test:** A task due today or within the next few days should get the correct increase
- **Expected outcome:** Tasks due sooner should score higher than tasks due later

### 4. Completed or review penalty
- **Priority:** High
- **Type:** Unit test
- **What to test:** Tasks marked as `DONE` or `REVIEW` should have reduced scores
- **Expected outcome:** `DONE` tasks should have the biggest reduction, `REVIEW` tasks should also be reduced

### 5. Tag boost
- **Priority:** Medium
- **Type:** Unit test
- **What to test:** Tasks with tags like `blocker`, `critical`, or `urgent` should get extra points
- **Expected outcome:** Tagged urgent tasks should score higher than identical untagged tasks

### 6. Recently updated boost
- **Priority:** Medium
- **Type:** Unit test
- **What to test:** Tasks updated recently should receive a score increase
- **Expected outcome:** Recently updated tasks should score higher than older ones

### 7. Combined behavior
- **Priority:** Medium
- **Type:** Unit test
- **What to test:** A task with high priority, urgent tag, and overdue date should combine all score effects
- **Expected outcome:** Final score should reflect all relevant boosts and penalties

---

## Test Cases for `sortTasksByImportance`

### 8. Sorting order
- **Priority:** High
- **Type:** Unit test
- **What to test:** Tasks should be sorted from highest score to lowest score
- **Expected outcome:** The most important task should appear first

### 9. Stable behavior with mixed tasks
- **Priority:** Medium
- **Type:** Unit test
- **What to test:** Sorting should work with tasks that differ by priority, due date, and status
- **Expected outcome:** Tasks should appear in the expected descending order of importance

---

## Test Cases for `getTopPriorityTasks`

### 10. Top N results
- **Priority:** High
- **Type:** Unit test
- **What to test:** The function should return only the requested number of top tasks
- **Expected outcome:** If limit is 5, only 5 tasks should be returned

### 11. Fewer tasks than limit
- **Priority:** Medium
- **Type:** Unit test
- **What to test:** The function should handle cases where the task list is shorter than the limit
- **Expected outcome:** It should return all available tasks without error

---

## Integration Test Plan

### 12. Full workflow
- **Priority:** High
- **Type:** Integration test
- **What to test:** `calculateTaskScore`, `sortTasksByImportance`, and `getTopPriorityTasks` should work correctly together
- **Expected outcome:** Tasks should be scored, sorted, and trimmed correctly as one workflow

---

## TDD Test Plan

### 13. New feature: current user boost
- **Priority:** High
- **Type:** Unit test
- **What to test:** Tasks assigned to the current user should get a +12 score boost
- **Expected outcome:** Assigned tasks should score 12 points higher than identical unassigned tasks

### 14. Bug fix: days since update
- **Priority:** High
- **Type:** Unit test
- **What to test:** The updated-at calculation should correctly use day difference
- **Expected outcome:** The recent-update boost should apply only when the task was updated within the correct time range

---

## Test Dependencies
- A task object with fields such as priority, due date, status, tags, and updated_at
- Access to the three task prioritization functions
- A test framework such as `unittest`

---

## Expected Outcomes Summary
- Priority should affect base score
- Due dates should affect urgency
- Status should reduce score when appropriate
- Tags should increase score when relevant
- Recent updates should increase score
- Sorting should return highest scores first
- Top-priority function should limit results correctly
- New TDD feature should add +12 for current user tasks
- Bug fix should correct recent-update logic
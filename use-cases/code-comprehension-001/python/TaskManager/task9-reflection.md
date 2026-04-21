# Task 9: Reflection

## What I Learned About Testing
This exercise helped me understand that testing is not only about checking if code runs, but about checking whether the code behaves correctly in different situations.

I learned that when testing a function like `calculateTaskScore`, it is important to think about all the behaviors that affect the result, such as priority, due dates, status, tags, and update time.

I also learned that related functions should not only be tested individually, but also together as a workflow.

---

## What Was Challenging
The most challenging part was identifying all the edge cases that could affect the score calculation.

It was also challenging to think about how to test behavior clearly without focusing too much on implementation details.

Another difficult part was planning TDD tests for a new feature and a bug fix before writing the code.

---

## How AI Helped
AI helped me think more carefully about what to test.

It helped me break the problem into smaller parts:
- what the function is supposed to do
- which behaviors matter most
- which edge cases could be missed
- how to organize tests by priority

AI also helped me understand the difference between unit testing a single function and integration testing multiple functions together.

---

## What I Would Do Differently Next Time
Next time, I would start by listing behaviors and edge cases before trying to write any tests.

I would also separate:
- basic behavior tests
- edge case tests
- integration tests

more clearly from the beginning.

I would use the TDD approach earlier so that features and bug fixes are guided by tests from the start.

---

## Final Thought
This exercise improved my understanding of testing as a structured process.

I now see that good testing requires planning, clear expectations, and careful thinking about both normal behavior and edge cases.
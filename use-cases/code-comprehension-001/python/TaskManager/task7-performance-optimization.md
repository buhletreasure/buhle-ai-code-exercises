# Task 7: Performance Optimization Challenge

## Selected Scenario
I selected the **Slow Code Analysis (Python)** scenario using `inventory_analysis.py`.

---

## Problem Description
The function is used to find pairs of products whose combined price is close to a target price.

According to the exercise, the function typically processes 5,000+ products and currently takes around 20–30 seconds to run. This makes the product recommendation page slow for users. :contentReference[oaicite:2]{index=2}

---

## Why the Code Is Slow
The main reason the code is slow is that it uses nested loops:

```python
for i in range(len(products)):
    for j in range(len(products)):
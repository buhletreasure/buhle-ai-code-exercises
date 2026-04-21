# Task 10: Function Decomposition Challenge

## Selected Function
I selected the `validateUserData` function, which contains many nested conditionals and multiple responsibilities.

---

## Identified Responsibilities

The function performs multiple tasks:

- checking required fields
- validating username
- validating password
- validating email
- validating date of birth
- validating address
- validating phone number
- handling custom validations

This makes the function very long and difficult to maintain.

---

## Decomposition Plan

To improve the function, I split it into smaller helper functions:

- `validateRequiredFields()`
- `validateUsername()`
- `validatePassword()`
- `validateEmail()`
- `validateDateOfBirth()`
- `validateAddress()`
- `validatePhone()`
- `applyCustomValidations()`

Each function handles one responsibility.

---

## Refactored Code

### Main Function
```javascript
function validateUserData(userData, options = {}) {
  const errors = [];

  validateRequiredFields(userData, options, errors);
  validateUsername(userData, options, errors);
  validatePassword(userData, errors);
  validateEmail(userData, options, errors);
  validateDateOfBirth(userData, errors);
  validateAddress(userData, errors);
  validatePhone(userData, errors);
  applyCustomValidations(userData, options, errors);

  return errors;
}
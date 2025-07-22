# CHANGES.md

## Overview

This file summarizes the main issues identified in the legacy user management API and documents the improvements made.

---

## Changes Made

### 1. **Code Organization**

* Grouped all route logic into a single `routes.py` file under a Flask Blueprint for better modularity.
* Ensured consistent naming conventions for functions and variables (`get_user`, `delete_user`, etc.).
* Cleaned up redundant code (e.g., reused SQL cursor logic where applicable).
* Reduced clutter by consolidating similar logic (e.g., `get_user_by_id` and `search_user_by_name`).

### 2. **Error Handling & Status Codes**

* Added proper HTTP status codes:

  * `200 OK` for successful GET/DELETE/PUT
  * `201 Created` for new user creation
  * `400 Bad Request` for input issues
  * `401 Unauthorized` for login failure
  * `409 Conflict` for duplicate email
* All API responses are returned in consistent JSON format (`{"status": "success"}` / `{"error": "..."}`).

### 3. **Validation**

* Added simple email format check in user creation.
* Trimmed incoming user data to prevent unintended whitespace issues.
* Prevented duplicate email insertion on user creation.

### 4. **Functional Consistency**

* Verified all endpoints work using `curl`:

  * `/users` (GET, POST)
  * `/user/<id>` (GET, PUT, DELETE)
  * `/search`
  * `/login`

### 5. **Documentation**

* This `CHANGES.md` explains the key changes, decisions, and assumptions taken during the refactor.

---

## Assumptions

* Passwords are stored in plaintext as provided in `init_db.py`, so **hashing is intentionally skipped** to maintain compatibility.
* Login is a basic credential check (`email` + `password` match exactly with DB).
* Focus is on making the code **clean and maintainable**, not adding new features or security layers.

---

## With More Time

* Switch to SQLAlchemy ORM for better DB abstraction and maintainability.
* Add input validation libraries like `marshmallow` or `pydantic`.
* Centralized error handling using Flask `@app.errorhandler`.
* Add unit tests for core endpoints.
* Implement password hashing and token-based auth (if spec allowed).

---

## AI Usage Disclosure

Used **ChatGPT** to:

* Identify issues in the legacy code structure
* Suggest modularization using Flask Blueprints
* Draft and polish this documentation

All changes and AI suggestions were reviewed and implemented manually.

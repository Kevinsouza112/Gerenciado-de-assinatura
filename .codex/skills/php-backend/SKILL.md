---
name: php-backend
description: Use when writing or refactoring PHP backend code, routes, controllers, database access, forms, login, order creation, or admin features.
---

# PHP Backend

Use simple, secure PHP.

Rules:
- Prefer PDO with prepared statements.
- Separate configuration, database connection, views, and business logic.
- Avoid duplicated code.
- Validate all inputs.
- Escape all HTML output.
- Use clear file and function names.
- Keep functions small.
- Do not mix too much HTML and PHP logic.
- Never store plain text passwords.
- Do not build unnecessary abstractions for the MVP.

For database operations:
- Use transactions when creating an order with multiple items.
- Check permissions before updating restaurant data.
- Handle errors without exposing sensitive details to the user.

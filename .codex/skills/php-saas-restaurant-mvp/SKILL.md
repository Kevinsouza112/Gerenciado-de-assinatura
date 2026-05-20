---
name: php-saas-restaurant-mvp
description: Build, review, and extend secure MVP features for a PHP/MySQL SaaS that provides digital menus and online ordering for small restaurants. Use when Codex is asked to plan or implement features in PHP, MySQL, HTML, CSS, JavaScript, Tailwind, or Bootstrap for restaurant menu management, ordering flows, tenant-aware SaaS behavior, database schema changes, input validation, prepared statements, or security/performance review in this project.
---

# PHP SaaS Restaurant MVP

## Operating Principles

- Prioritize simplicity, MVP scope, and compatibility with the existing system.
- Split large work into small, explainable steps before editing code.
- Review the database schema, relationships, and tenant boundaries before implementing behavior that reads or writes data.
- Preserve existing functionality. Warn before removing or changing behavior outside the requested scope.
- Prefer existing project patterns, helpers, layouts, and CSS framework conventions.
- Avoid new architectural layers unless they remove real duplication or clearly match the codebase.

## Security Baseline

- Never trust user input from `$_GET`, `$_POST`, cookies, headers, route parameters, uploaded files, or JavaScript.
- Validate input by type, required fields, length, range, format, enum membership, and ownership/tenant access.
- Sanitize output for the target context, especially HTML, attributes, URLs, JavaScript, and JSON.
- Use prepared statements for every SQL query with user-controlled values.
- Never concatenate user input into SQL, HTML, shell commands, file paths, redirects, or email headers.
- Check authorization before exposing restaurant, menu, product, order, or admin data.
- Use CSRF protection for state-changing forms when the project has or can support it.
- Hash passwords with PHP password APIs when authentication work is involved.
- Keep errors generic for users and detailed only in logs.

## Workflow

1. Inspect project structure, current routes/pages, database access helpers, and existing validation style.
2. Inspect relevant database tables and relationships before changing a feature.
3. Define the smallest useful MVP behavior and edge cases.
4. Implement in small steps using existing conventions.
5. Validate and sanitize every external input.
6. Use prepared statements for all database operations.
7. Review for security vulnerabilities before finalizing.
8. Run focused checks or tests available in the project.
9. Mention performance considerations when query volume, indexes, N+1 reads, image loading, or order growth may matter.

## MVP Feature Guidance

For restaurant ordering without integrated payment, prefer this core flow:

- Restaurant/admin manages categories, menu items, availability, and prices.
- Customer views a public menu, builds a cart, and submits an order.
- Order stores customer name/contact, optional address/table/notes, items, quantities, prices at purchase time, total, and status.
- Admin views incoming orders and updates status.

Keep payment status, delivery logistics, coupons, loyalty, analytics, multi-branch support, and complex inventory out of scope unless the user asks for them.

## Database Review Checklist

- Identify primary keys, foreign keys, tenant/restaurant ownership fields, and status fields.
- Confirm whether prices and item names must be snapshotted on order items.
- Confirm cascade behavior before deleting restaurants, categories, menu items, or orders.
- Add indexes only where they support real lookups, such as `restaurant_id`, `order_id`, slug fields, status, and timestamps.
- Keep schema migrations minimal and backward-compatible.

## PHP/MySQL Implementation Rules

- Prefer PDO or the project's existing database abstraction.
- Bind parameters with explicit types when practical.
- Normalize server-side validation errors into the project's existing response or template style.
- Escape output with `htmlspecialchars($value, ENT_QUOTES, 'UTF-8')` unless the project has a trusted helper.
- For JSON responses, set the correct content type and use `json_encode`.
- Keep controllers/actions short; extract helpers only when duplication becomes real.

## Final Review

Before final response, check:

- SQL injection risk.
- XSS risk.
- CSRF risk for state-changing requests.
- Authentication and authorization checks.
- Tenant data isolation.
- Input validation and output escaping.
- Error handling.
- Compatibility with existing routes, templates, and database relationships.
- Obvious performance risks and missing indexes.

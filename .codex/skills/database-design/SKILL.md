---
name: database-design
description: Use when designing or reviewing MySQL tables, relationships, indexes, migrations, order schema, product schema, restaurant schema, or multi-tenant data.
---

# Database Design

Design the database for a simple restaurant ordering system.

Review:
- Table names
- Column names
- Primary keys
- Foreign keys
- Indexes
- Required fields
- Status fields
- Data types
- Multi-restaurant separation

Prefer these core entities:
- restaurants
- users
- categories
- products
- orders
- order_items
- customers

Rules:
- Use foreign keys when possible.
- Use decimal for prices.
- Store order snapshots, not only product references.
- Add created_at and updated_at where useful.
- Avoid overcomplicating the MVP.

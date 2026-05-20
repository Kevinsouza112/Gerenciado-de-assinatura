---
name: folder-organization
description: >
  Use this skill when creating or modifying project structure,
  organizing files or scaling application architecture.
---

# Folder Organization Standards

You are a senior software architect.

## Goals

Always create projects that are:

- modular
- scalable
- maintainable
- easy to navigate
- beginner friendly

## Rules

- Never create giant files
- Separate responsibilities
- Group related modules
- Keep routes/controllers thin
- Move business logic to services
- Keep database logic in repositories

## Preferred Structure

app/
├── api/
├── services/
├── repositories/
├── models/
├── schemas/
├── database/
├── core/
├── utils/
├── tests/

## Naming Conventions

Use consistent naming:

- user_service.py
- user_repository.py
- user_schema.py
- auth_routes.py

## File Limits

Avoid files larger than ~300 lines when possible.

If a file grows too much:

- split by feature
- split by responsibility
- create helper modules

## Imports

Prefer:

- absolute imports
- organized imports
- avoid circular dependencies

## Scalability

Structure code so new features can be added without major rewrites.

## Before Coding

Always explain:

- folder structure
- why each folder exists
- where new features should go

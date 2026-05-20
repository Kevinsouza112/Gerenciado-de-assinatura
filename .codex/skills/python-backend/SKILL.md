---
name: python-backend
description: >
  Use this skill when creating, modifying, reviewing or planning Python backend systems.
  Focus on clean architecture, scalability, security and maintainability.
---

# Python Backend Standards

You are a senior Python backend engineer.

## Stack Priority

Prefer:

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker
- Pytest

## Code Standards

Always:

- Use type hints
- Follow PEP8
- Use modular architecture
- Separate responsibilities
- Avoid duplicated logic
- Create reusable services
- Use environment variables
- Validate all inputs
- Use async when appropriate

## Architecture

Prefer structure:

```text
app/
|-- api/
|-- models/
|-- schemas/
|-- services/
|-- repositories/
|-- database/
|-- core/
`-- tests/
```

## API Standards

- Use REST patterns
- Proper HTTP status codes
- JSON responses
- Error handling middleware
- Pagination support
- Authentication middleware

## Database Standards

- Never use raw SQL unless necessary
- Use migrations
- Create indexes when needed
- Normalize relations properly

## Security

Always:

- Validate inputs
- Sanitize data
- Hash passwords
- Protect secrets
- Prevent SQL Injection
- Prevent mass assignment

## Before Coding

Always explain:

- architecture
- file structure
- flow
- security concerns
- scalability considerations

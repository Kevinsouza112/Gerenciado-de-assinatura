---
name: api-design
description: >
  Use this skill when designing REST APIs.
---

# API Design

Design scalable and maintainable APIs.

## Standards

Use:

- REST conventions
- proper status codes
- versioning
- pagination
- filtering
- consistent naming

## Response Format

Prefer:

```json
{
  "success": true,
  "data": {},
  "message": ""
}
```

## Error Format

```json
{
  "success": false,
  "error": {
    "code": "",
    "message": ""
  }
}
```

## Authentication

Prefer JWT authentication.

## Documentation

Always generate Swagger/OpenAPI compatible endpoints.

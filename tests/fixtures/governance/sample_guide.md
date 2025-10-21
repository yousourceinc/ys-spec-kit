---
title: "Backend API Implementation Guide"
division: "SE"
version: "1.0"
rules:
  - id: api-routes-defined
    type: file_exists
    path: "src/api/routes.py"
    description: "API routes module must exist"
  
  - id: tests-present
    type: file_exists
    path: "tests/api/test_routes.py"
    description: "API tests must exist"
  
  - id: fastapi-dependency
    type: dependency_present
    file: "requirements.txt"
    package: "fastapi"
    version: ">=0.95"
    description: "FastAPI version 0.95+ required"
  
  - id: router-decorator-used
    type: text_includes
    file: "src/api/routes.py"
    text: "@router.get"
    description: "Must use FastAPI router decorators"
    case_sensitive: true
---

# Backend API Implementation Guide

## Overview

This guide defines best practices for implementing backend APIs using FastAPI.

## Requirements

1. **API Routes Module**: All API endpoints must be defined in `src/api/routes.py`
2. **Test Coverage**: Comprehensive tests must exist in `tests/api/test_routes.py`
3. **FastAPI Framework**: Use FastAPI version 0.95 or higher
4. **Router Pattern**: Use FastAPI's router decorator pattern (`@router.get`, `@router.post`, etc.)

## Example Implementation

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def list_users():
    return {"users": []}

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

## Testing

All endpoints must have corresponding tests:

```python
def test_list_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert "users" in response.json()
```

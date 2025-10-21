"""Sample API routes file for compliance testing."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
async def list_users():
    """List all users."""
    return {"users": []}


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get a specific user."""
    return {"user_id": user_id}


@router.post("/users")
async def create_user(user_data: dict):
    """Create a new user."""
    return {"created": True}

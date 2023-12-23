from fastapi import APIRouter

router = APIRouter(
    prefix="/password_reset",
    tags=["Password Reset"]
)


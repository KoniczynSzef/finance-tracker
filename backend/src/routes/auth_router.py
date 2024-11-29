from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/current_user")
def get_current_user():
    return {"message": "Hello World"}

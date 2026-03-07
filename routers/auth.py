from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.get("/login", status_code=status.HTTP_200_OK)
def get_user():
    """
        This function is a placeholder for a login endpoint.
        It currently returns a simple message indicating that the login was successful.
        In a real application    , this function would likely include logic to authenticate the user and generate a token or session for them.
    """
    return {"message": "Login successful"}

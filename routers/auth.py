from fastapi import APIRouter

router = APIRouter()


@router.get("/login")
def get_user():
    """
        This function is a placeholder for a login endpoint.
        It currently returns a simple message indicating that the login was successful.
        In a real application    , this function would likely include logic to authenticate the user and generate a token or session for them.
    """
    return {"message": "Login successful"}

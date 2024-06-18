from fastapi import APIRouter, status, HTTPException
from src.schemas.response import HTTPResponses, HttpResponseModel
from src.service.impl.user_service import UserService
from src.schemas.user import UserModel, UserGet, UserList
from uuid import uuid4

router = APIRouter()

@router.post(
    "/",
    response_model=HttpResponseModel,
    status_code=status.HTTP_201_CREATED,
    description="Create a new user",
    tags=["users"],
    responses={
        status.HTTP_201_CREATED: {
            "model": HttpResponseModel,
            "description": "Successfully created a new user",
        }
    },
)
def create_user(user: dict) -> HttpResponseModel:
    """
    Create a user.

    Returns:
    - The created user.

    """
    user_create_response = UserService.create_user(user)
    return user_create_response

@router.put(
    "/{user_id}",
    response_model=HttpResponseModel,
    status_code=status.HTTP_200_OK,
    description="Create a new user",
    tags=["users"],
    responses={
        status.HTTP_200_OK: {
            "model": HttpResponseModel,
            "description": "Successfully update user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        }
    },
)
def update_user(user_id: str, user: dict) -> HttpResponseModel:
    """
    Create a user.

    Returns:
    - The created user.

    """

    user_updated_response = UserService.update_user(user_id, user)
    return user_updated_response


@router.delete(
    "/{user_id}",
    response_model=HttpResponseModel,
    status_code=status.HTTP_200_OK,
    description="Delete an existing user",
    tags=["users"],
    responses={
        status.HTTP_200_OK: {
            "model": HttpResponseModel,
            "description": "Successfully deleted the user",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        }
    },
)
def delete_user(user_id: str) -> HttpResponseModel:
    """
    Delete an existing user.

    Parameters:
    - user_id: The ID of the user to delete.

    Returns:
    - Confirmation of user deletion.

    Raises:
    - HTTPException 404: If the user is not found.

    """
    user_delete_response = UserService.delete_user(user_id)
    if not user_delete_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_delete_response

@router.post(
    "/token",
    response_model=HttpResponseModel,
    status_code=status.HTTP_200_OK,
    description="Authenticate user by password+email",
    tags=["users"],
    responses={
        status.HTTP_200_OK: {
            "model": HttpResponseModel,
            "description": "User's bearer token"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Wrong password or email"
        }
    }
)
def login(user: UserModel) -> HttpResponseModel:
    """
    Authenticate an existing user.

    Returns:
    - User's bearer token.
    """
    if None in [user.email, user.password]:
        return HttpResponseModel(
            message=HTTPResponses.MISSING_PARAMETERS().message,
            status_code=HTTPResponses.MISSING_PARAMETERS().status_code
        )
    
    user_db = UserService.get_user_by_email(user.email)
    if not user_db or user.password != user_db['password']:
        return HttpResponseModel(
            message=HTTPResponses.UNAUTHORIZED().message,
            status_code=HTTPResponses.UNAUTHORIZED().status_code
        )
    user_db['token'] = uuid4().hex
    UserService.update_user(user_id=user_db['id'], user_data=user_db)

    return HttpResponseModel(
        message=HTTPResponses.AUTHORIZED().message,
        status_code=HTTPResponses.AUTHORIZED().status_code,
        data={
            "token": user_db['token']
        }
    )

from fastapi import Depends, APIRouter, Response, status, HTTPException, FastAPI
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from typing import List, Any
from app import schemas
from app.services.userService import userService


# Defining the router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)

"""
    A generic CRUD router can be created. 
    Specifically for employee, client, contact , department endpoints as they use only CRUD functionality
"""


def not_found_exception(id):
    """
    No client found with specific ID exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Client with id= {id} not found"
    )
    
def entities_not_found_for_client_exception(id, entity_name):
    """
    No entities found for client with specific ID exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No {entity_name}s found for client with id= {id} "
    )

@router.get("/{username}", response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    """
    Get a client by its ID
    """
    result = userService.get_user_by_username(db, username)
    if not result:
        raise not_found_exception(id)

    return result



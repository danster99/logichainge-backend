from fastapi import Depends, APIRouter, status, HTTPException, Response
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from app import schemas
from app.models import User
from app.services import userService
from fastapi_jwt_auth import AuthJWT
from typing import List, Any




# Defining the router
router = APIRouter(
	prefix="/users",
	tags=["users"],
	responses={404: {"description": "Not Found"}},
)

"""
	A generic CRUD router can be created. 
	Specifically for employee, client, user , department endpoints as they use only CRUD functionality
"""

def not_found_by_id_exception(id):
	"""
	No client found with specific ID exception
	"""
	return HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail=f"Client with id= {id} not found"
	)

def not_found_by_username_exception(id):
	"""
	No client found with specific ID exception
	"""
	return HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail=f"Client with username= {id} not found"
	)
	
def entities_not_found_for_client_exception(id, entity_name):
	"""
	No entities found for client with specific ID exception
	"""
	return HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail=f"No {entity_name}s found for client with id= {id} "
	)

@router.get("/", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
	"""
	Get all users as LIST
	"""

	all_user = userService.get_multiple(db=db)
	print(all_user)
	return all_user

@router.get("/me", response_model=schemas.UserOut)
def user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
	Authorize.jwt_required()
	current_user = Authorize.get_jwt_subject()
	user = userService.get_user_by_username(db=db, username=current_user)
	return user

@router.get("/get_by_username/{username}", response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
	#Authorize.jwt_required()
	"""
	Get a client by its ID
	"""
	result = userService.get_user_by_username(db, username)
	if not result:
		raise not_found_by_username_exception(username)

	return result

@router.get("/get_by_id/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
	#Authorize.jwt_required()
	"""
	Get a client by its ID
	"""
	result = userService.get_user_by_id(db, id)
	if not result:
		raise not_found_by_id_exception(id)

	return result

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
	"""
	Get all transport_files as LIST
	"""
	Authorize.jwt_required()
	try:
		db_user = userService.create_user(db=db, user_in=user)
	except (exc.IntegrityError) as e:
		print(e.orig)
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

	return db_user

@router.put("/{id}", response_model=schemas.UserOut)
def update_user(*,
                   id: int,
                   db: Session = Depends(get_db),
                   user_update: schemas.UserBase,
                   ) -> Any:
    """
    Update a specific user
    """

    db_user = userService.get(db=db, id=id)
    if not db_user:
        raise not_found_by_id_exception(id)

    try:
        db_user_updated = userService.update(db=db, obj_in=user_update, id=id)
    except (exc.IntegrityError) as e:
        print(e.orig)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

    return db_user_updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(*, db: Session = Depends(get_db), id: int, ):
    """
    Delete a specific user
    """

    db_user = userService.get(db=db, id=id)
    if not db_user:
        raise not_found_by_id_exception(id)

    userService.delete(db=db, id=id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)





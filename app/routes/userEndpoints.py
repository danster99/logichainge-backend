from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session
from app.database.database import get_db
from app import schemas
from app.models import User
from app.services.userService import userService
from fastapi_jwt_auth import AuthJWT



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

@router.get("/me", response_model=schemas.UserOut)
def user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
	Authorize.jwt_required()
	current_user = Authorize.get_jwt_subject()
	user = userService.get_user_by_username(db=db, username=current_user)
	return user

@router.get("/{username}", response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
	Authorize.jwt_required()
	"""
	Get a client by its ID
	"""
	result = userService.get_user_by_username(db, username)
	if not result:
		raise not_found_exception(id)

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





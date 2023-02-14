from app.services.defaultService import DefaultService
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Any
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




class userService(
	DefaultService[models.User, schemas.UserBase, schemas.UserOut],
):


	"""
	User service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning client from child service"

	def get_hashed_password(password: str) -> str:
		return pwd_context.hash(password)

	def get_user_by_username(db : Session, username: str):
		user =  db.query(models.User).filter(models.User.username == username).first()
		return user

	def get_user_by_id(db : Session, id: int):
		user =  db.query(models.User).filter(models.User.id == id).first()
		return user

	def verify_password(plain_password, hashed_passw):
		return pwd_context.verify(plain_password, hashed_passw)

	def authenticate_user(db : Session, username: str, password: str):
		user = userService.get_user_by_username(db, username)
		if not user:
			return False
		if not userService.verify_password(password, user.hashed_pass):
			return False
		return user

	def create_user(db: Session, user_in: schemas.UserIn):
		user_data = jsonable_encoder(user_in)
		user_data["hashed_pass"] = userService.get_hashed_password(user_data["password"])
		user_data.pop("password")
		db_user = models.User(**user_data)
		
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
		return db_user

	def update_user(db: Session, user_in: schemas.UserIn):
		user_data = jsonable_encoder(user_in)
		user_data["hashed_pass"] = userService.get_hashed_password(user_data["password"])
		user_data.pop("password")
		db_user = models.User(**user_data)
		
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
		return db_user

userService = userService(models.User)


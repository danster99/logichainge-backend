from app.services.defaultService import DefaultService
from .tokenService import tokenService
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class userService(
	DefaultService[models.User, schemas.UserBase, schemas.UserOut],
):

	pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

	"""
	User service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning client from child service"


	def get_user_by_username(db : Session, username: str):
		user =  db.query(models.User).filter(models.User.username == username).first()
		return user

	def get_user_by_id(db : Session, id: int):
		user =  db.query(models.User).filter(models.User.id == id).first()
		return user

	def verify_password(plain_password, hashed_passw):
		return userService.pwd_context.verify(plain_password, hashed_passw)

	def authenticate_user(db : Session, username: str, password: str):
		user = userService.get_user_by_username(db, username)
		if not user:
			return False
		if not userService.verify_password(password, user.hashed_pass):
			return False
		return user

	async def get_current_user(db : Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
		credentials_exception = HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Could not validate credentials",
			headers={"WWW-Authenticate": "Bearer"},
		)
		try:
			payload = jwt.decode(token, tokenService.SECRET_KEY, algorithms=[tokenService.ALGORITHM])
			username: str = payload.get("sub")
			if username is None:
				raise credentials_exception
		except JWTError:
			raise credentials_exception
		user = userService.get_user_by_username(db=db, username=username)
		if user is None:
			raise credentials_exception
		return user

	@staticmethod
	async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
		if current_user.disabled:
			raise HTTPException(status_code=400, detail="Inactive user")
		return current_user



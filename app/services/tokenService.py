from app.services.defaultService import DefaultService
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta



class tokenService(
	DefaultService[models.Token, schemas.TokenBase, schemas.TokenOut],
):

	SECRET_KEY = "6fe6eb6647fd49122a1d8fbf8274808fe33a58c0bf828979229423e1c36c06a7"
	ALGORITHM = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES = 30

	def create_access_token(data: dict, expires_delta: timedelta | None = None):
		to_encode = data.copy()
		if expires_delta:
			expire = datetime.utcnow() + expires_delta
		else:
			expire = datetime.utcnow() + timedelta(minutes=15)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, tokenService.SECRET_KEY, algorithm=tokenService.ALGORITHM)
		return encoded_jwt

	@staticmethod
	def validateHeader(authorization: str):
		try:
			if (authorization.startswith('Bearer ')):
				token = authorization.split(' ')
				tokenService.secure(token[1])
			else:
				return "header"
		except:
			return "access"
		return None

	def secure(token):
		# if we want to sign/encrypt the JSON object: {"hello": "world"}, we can do it as follows
		# encoded = jwt.encode({"hello": "world"}, JWT_SECRET, algorithm=JWT_ALGORITHM)
		decoded_token = jwt.decode(token, tokenService.SECRET_KEY, algorithms=tokenService.ALGORITHM)
		# this is often used on the client side to encode the user's email address or other properties
		return decoded_token

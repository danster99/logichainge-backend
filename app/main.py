import time
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .routes import transportFileEndpoints, activityEndpoints, \
    goodsEndpoints, addressEndpoints, \
    clientEndpoints, contactEndpoints, \
    departmentEndpoints, employeeEndpoints, \
    jsonEndpoints, userEndpoints
from fastapi.middleware.cors import CORSMiddleware
from .services.userService import userService
from .services.tokenService import tokenService
from .models import User, Token
from sqlalchemy.orm import Session
from app.database.database import get_db
from datetime import timedelta
from .schemas.user import UserOut



# Declaring main FAST API app
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")
origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Adding middleware for checking process time of each endpoint call
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"message": "Welcome to Logichainge"}

@app.get("/auth")
async def getToken(token: str = Depends(oauth2_scheme)):
	return {"token": token}
	
@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(userService.get_current_active_user)):
    return current_user

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = userService.authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token_expires = timedelta(minutes=tokenService.ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = tokenService.create_access_token(
		data={"user": user.username}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}


""" Declaring all routes as part of the main FAST API app """

app.include_router(transportFileEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(clientEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(contactEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(departmentEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(employeeEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(activityEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(addressEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(goodsEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(jsonEndpoints.router)  # ,dependencies=[Depends(verify_token)])
app.include_router(userEndpoints.router)  # ,dependencies=[Depends(verify_token)])
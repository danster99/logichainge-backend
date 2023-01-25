import time
from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.security import HTTPBearer
from .authZ.utils import VerifyToken
from .routes import transportFileEndpoints, activityEndpoints, \
    goodsEndpoints, addressEndpoints, \
    clientEndpoints, contactEndpoints, \
    departmentEndpoints, employeeEndpoints, \
    jsonEndpoints
from fastapi.middleware.cors import CORSMiddleware

# Declaring main FAST API app
app = FastAPI()

token_auth_scheme = HTTPBearer()

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


def verify_token(token: str = Depends(token_auth_scheme)):
    """
    Logic for verifying each AUTH token
    NOTE: Implementation Not yet finalised and set up without security for testing phase
    """
    result = VerifyToken(token.credentials).verify()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if result.get("status"):
        raise credentials_exception
    return result


@app.get("/")
async def root():
    return {"message": "Welcome to Logichainge"}


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

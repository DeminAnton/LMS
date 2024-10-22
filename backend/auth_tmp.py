import secrets
from time import time
from typing import Annotated
import uuid
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials





app = FastAPI()

security = HTTPBasic()

@app.get("/my-basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    # The credentials parameter must be of type HTTPBasicCredentials.
    # The value for this parameter will be provided by resolving the Depends(security) dependency.
):
    return {
        "message": "Hello!",
        "username": credentials.username,
        "password": credentials.password,
    }
    
    
users = [
    {"name": "john", "pswd": "12345"},
    {"name": "tony", "pswd": "tony"},
]

def get_auth_user_username(
    credantials : Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Basic"},
    )
    for user in users:
        if credantials.username == user["name"]:
            auth_user = user
            break
    else:
        raise unauth_exc
    
    if not secrets.compare_digest(
        credantials.password.encode("utf-8"),
        auth_user["pswd"].encode("utf-8"),
    ):
        raise unauth_exc
    return credantials


@app.get("/my-basic-auth-check/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(get_auth_user_username)],
    # The credentials parameter must be of type HTTPBasicCredentials.
    # The value for this parameter will be provided by resolving the Depends(security) dependency.
):
    return {
        "message": "Hello!",
        "username": credentials.username,
        "password": credentials.password,
    }
    
#----------------------
# TOKEN

tokens = {
    "13abc": ("Tony", "Tony"),
    "abcba": ("Admin", "12345"),
}


def get_credentials_by_token(
    token:str = Header(alias="x-static-auth-token"),
) -> tuple:
    if token not in tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid"
        )
    return tokens[token]

@app.get("/header-auth/")
def header_auth(
    user_credentials = Depends(get_credentials_by_token)
):
    username, password = user_credentials
    return {
        "Message": f"Hi! {username}",
        "Username": username,
        "Password": password,
    }
    
login_cookies: dict[str, dict] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"
    
@app.post("/login-cookie/")
def login_set_cookie(
    response: Response,
    user_credentials = Depends(get_credentials_by_token)
):
    username, password = user_credentials
    session_id = uuid.uuid4().hex
    login_cookies[session_id] = {
        "username": username,
        "password": password,
        "login_in": int(time())
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {
        "Message": f"Hi! {username}",
        "Username": username,
        "Password": password,
        "Cookie": "ok!",
    }  
    
    
def get_session_data(
    session_id:str = Cookie(alias=COOKIE_SESSION_ID_KEY)
) -> dict:
    if session_id not in login_cookies:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid session"
        )
    return login_cookies[session_id]

    
    
@app.get("/check-cookie/")
def auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
        
    return {
        "message": f"{username}, Hello!",
        **user_session_data
    }
    
    
if __name__ == "__main__":
    uvicorn.run("auth_tmp:app", reload=True)

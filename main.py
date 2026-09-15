from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="JWT demo")

SECRET_KEY = "learn-jwt-secret-32-bytes-long!!"
ALGORITHM = "HS256"
bearer = HTTPBearer()

USERS = {
    "student": {"password": "python", "role": "student"},
    "teacher": {"password": "fastapi", "role": "teacher"},
}

class LoginData(BaseModel):
    username: str
    password: str


def create_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(data: LoginData):
    user = USERS.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    role = user["role"] 

    return {"access_token": create_token(data.username, role), "token_type": "bearer" , "role": role}


@app.get("/me")
def me(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    role = payload.get("role")
    if not username:
        raise HTTPException(status_code=401, detail="Token has no username")

    return {"message": f"Hello, {username}!", "role": role}


if __name__ == "__main__":
    token = create_token("student", "student")
    assert jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"] == "student"
    assert jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["role"] == "student"
    print("JWT self-check passed")

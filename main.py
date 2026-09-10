from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI(title="JWT demo")

SECRET_KEY = "learn-jwt-secret-32-bytes-long!!"
ALGORITHM = "HS256"
bearer = HTTPBearer()


class LoginData(BaseModel):
    username: str
    password: str


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/login")
def login(data: LoginData):
    if data.username != "student" or data.password != "python":
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"access_token": create_token(data.username), "token_type": "bearer"}


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
    if not username:
        raise HTTPException(status_code=401, detail="Token has no username")

    return {"message": f"Hello, {username}!"}


if __name__ == "__main__":
    token = create_token("student")
    assert jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"] == "student"
    print("JWT self-check passed")

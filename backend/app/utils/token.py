from jose import jwt
from datetime import datetime, timedelta
from backend.app.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=30)
    data = {"sub": email, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")
def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return email
    except JWTError:
        return None
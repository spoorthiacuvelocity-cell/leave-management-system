from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database.postgres import get_db
from backend.app.models.user import User
from backend.app.models.configuration import Configuration
from backend.app.config import SECRET_KEY, ALGORITHM


# ================= PASSWORD HASHING =================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    # 🔹 Prevent crash if password in DB is invalid
    if not hashed_password:
        return False

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


# ================= OAUTH2 =================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ================= TOKEN EXPIRY =================
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ================= CREATE ACCESS TOKEN =================
def create_access_token(data: dict):
    to_encode = data.copy()

    # Ensure subject is string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# ================= GET CURRENT USER =================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    # 🔹 Block resigned users
    if user.resignation_status == "APPROVED":
        raise HTTPException(
            status_code=403,
            detail="Your resignation has been approved. Please contact HR."
        )

    # 🔹 Block inactive users
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account is deactivated. Please contact HR."
        )

    return user


# ================= HELPER FUNCTION =================
def get_config(db: Session, key: str):

    config = db.query(Configuration).filter(
        Configuration.config_parameter == key
    ).first()

    return config.config_value if config else None
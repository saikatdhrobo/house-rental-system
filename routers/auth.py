from datetime import datetime, timedelta, timezone

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
from models import Users

from passlib.context import CryptContext
from jose import jwt, JWTError

auth_bp = Blueprint("auth", __name__)

# JWT Configuration
SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
ALGORITHM = "HS256"

# Password Hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------
# Pydantic Models
# -----------------------------
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# -----------------------------
# Database Connection
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# -----------------------------
# Authentication Functions
# -----------------------------
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role
    }

    expires = datetime.now(timezone.utc) + expires_delta

    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")

        if username is None or user_id is None:
            return None

        return {
            "username": username,
            "id": user_id,
            "user_role": user_role
        }

    except JWTError:
        return None

    except Exception:
        return None


# -----------------------------
# Routes
# -----------------------------

# CREATE USER
@auth_bp.route("/", methods=["POST"])
def create_user():
    db: Session = get_db()

    try:
        data = request.get_json()

        create_user_request = CreateUserRequest(**data)

        create_user_model = Users(
            email=create_user_request.email,
            username=create_user_request.username,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            role=create_user_request.role,
            hashed_password=bcrypt_context.hash(create_user_request.password),
            is_active=True
        )

        db.add(create_user_model)
        db.commit()

        return jsonify({
            "message": "User created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# LOGIN / TOKEN
@auth_bp.route("/token", methods=["POST"])
def login_for_access_token():
    db: Session = get_db()

    data = request.form

    username = data.get("username")
    password = data.get("password")

    user = authenticate_user(username, password, db)

    if not user:
        return jsonify({
            "detail": "Could not validate user."
        }), 401

    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=20)
    )

    return jsonify({
        "access_token": token,
        "token_type": "bearer"
    }), 200

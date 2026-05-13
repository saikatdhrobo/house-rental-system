from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ValidationError

from models import Users
from database import SessionLocal
from routers.auth import get_current_user
from passlib.context import CryptContext

users_bp = Blueprint("users", __name__)

# Password Hashing
bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


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
# Pydantic Model
# -----------------------------
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


# -----------------------------
# GET CURRENT USER
# -----------------------------
@users_bp.route("/", methods=["GET"])
def get_user():
    user = get_current_user()

    if user is None:
        return jsonify({
            "detail": "Authentication Failed"
        }), 401

    db: Session = get_db()

    user_model = db.query(Users).filter(
        Users.id == user.get("id")
    ).first()

    if user_model is None:
        return jsonify({
            "detail": "User not found"
        }), 404

    return jsonify({
        "id": user_model.id,
        "email": user_model.email,
        "username": user_model.username,
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
        "role": user_model.role,
        "is_active": user_model.is_active
    }), 200


# -----------------------------
# CHANGE PASSWORD
# -----------------------------
@users_bp.route("/password", methods=["PUT"])
def change_password():
    user = get_current_user()

    if user is None:
        return jsonify({
            "detail": "Authentication Failed"
        }), 401

    try:
        user_verification = UserVerification(**request.json)

        db: Session = get_db()

        user_model = db.query(Users).filter(
            Users.id == user.get("id")
        ).first()

        if user_model is None:
            return jsonify({
                "detail": "User not found"
            }), 404

        if not bcrypt_context.verify(
            user_verification.password,
            user_model.hashed_password
        ):
            return jsonify({
                "detail": "Error on password change"
            }), 401

        user_model.hashed_password = bcrypt_context.hash(
            user_verification.new_password
        )

        db.add(user_model)
        db.commit()

        return jsonify({
            "message": "Password updated successfully"
        }), 200

    except ValidationError as e:
        return jsonify({
            "errors": e.errors()
        }), 400

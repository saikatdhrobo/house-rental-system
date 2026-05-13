from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.orm import Session

from models import Todos
from database import SessionLocal
from routers.auth import get_current_user
todos_bp = Blueprint("todos", __name__)


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
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# -----------------------------
# GET ALL TODOS
# -----------------------------
@todos_bp.route("/", methods=["GET"])
def read_all():
    user = get_current_user()

    if user is None:
        return jsonify({
            "detail": "Authentication Failed"
        }), 401

    db: Session = get_db()

    todos = db.query(Todos).filter(
        Todos.owner_id == user.get("id")
    ).all()

    return jsonify([
        {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "priority": todo.priority,
            "complete": todo.complete,
            "owner_id": todo.owner_id
        }
        for todo in todos
    ]), 200


# -----------------------------
# GET SINGLE TODO
# -----------------------------
@todos_bp.route("/todo/<int:todo_id>", methods=["GET"])
def read_todo(todo_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "detail": "Authentication Failed"
        }), 401

    db: Session = get_db()

    todo_model = db.query(Todos).filter(
        Todos.id == todo_id,
        Todos.owner_id == user.get("id")
    ).first()

    if todo_model is not None:
        return jsonify({
            "id": todo_model.id,
            "title": todo_model.title,
            "description": todo_model.description,
            "priority": todo_model.priority,
            "complete": todo_model.complete,
            "owner_id": todo_model.owner_id
        }), 200

    return jsonify({
        "detail": "Todo not found."
    }), 404


# -----------------------------
# CREATE TODO
# -----------------------------
@todos_bp.route("/todo", methods=["POST"])
def create_todo():
    user = get_current_user()

    if user is None:
        return jsonify({
            "detail": "Authentication Failed"
        }), 401

    try:
        todo_request = TodoRequest(**request.json)

        db: Session = get_db()

        todo_model = Todos(
            title=todo_request.title,
            description=todo_request.description,
            priority=todo_request.priority,
            complete=todo_request.complete,
            owner_id=user.get("id")
        )

        db.add(todo_model)
        db.commit()

        return jsonify({
            "message": "Todo created successfully"
        }), 201

    except ValidationError as e:
        return jsonify({
            "errors": e.errors()
        }), 400


# -----------------------------
# UPDATE TODO
# -----------------------------
@todos_bp.route("/todo/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "detail": "Authentication Failed"
        }), 401

    try:
        todo_request = TodoRequest(**request.json)

        db: Session = get_db()

        todo_model = db.query(Todos).filter(
            Todos.id == todo_id,
            Todos.owner_id == user.get("id")
        ).first()

        if todo_model is None:
            return jsonify({
                "detail": "Todo not found."
            }), 404

        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()

        return jsonify({
            "message": "Todo updated successfully"
        }), 200

    except ValidationError as e:
        return jsonify({
            "errors": e.errors()
        }), 400


# -----------------------------
# DELETE TODO
# -----------------------------
@todos_bp.route("/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    user = get_current_user()

    if user is None:
        return jsonify({
            "detail": "Authentication Failed"
        }), 401

    db: Session = get_db()

    todo_model = db.query(Todos).filter(
        Todos.id == todo_id,
        Todos.owner_id == user.get("id")
    ).first()

    if todo_model is None:
        return jsonify({
            "detail": "Todo not found."
        }), 404

    db.query(Todos).filter(
        Todos.id == todo_id,
        Todos.owner_id == user.get("id")
    ).delete()

    db.commit()

    return jsonify({
        "message": "Todo deleted successfully"
    }), 200

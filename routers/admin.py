from flask import Blueprint, jsonify
from sqlalchemy.orm import Session

from models import Todos
from database import SessionLocal
from routers.auth import get_current_user

admin_bp = Blueprint("admin", __name__)


# Database session
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# GET ALL TODOS (Admin only)
@admin_bp.route("/todo", methods=["GET"])
def read_all():
    user = get_current_user()

    if user is None or user.get("user_role") != "admin":
        return jsonify({"detail": "Authentication Failed"}), 401

    db: Session = get_db()

    todos = db.query(Todos).all()

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


# DELETE TODO (Admin only)
@admin_bp.route("/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    user = get_current_user()

    if user is None or user.get("user_role") != "admin":
        return jsonify({"detail": "Authentication Failed"}), 401

    if todo_id <= 0:
        return jsonify({"detail": "Invalid todo ID"}), 400

    db: Session = get_db()

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        return jsonify({"detail": "Todo not found."}), 404

    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()

    return jsonify({"message": "Todo deleted successfully"}), 200

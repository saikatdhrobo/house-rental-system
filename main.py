from flask import Flask, send_from_directory
from flask_cors import CORS

import os

import models
from database import engine

from routers.auth import auth_bp
from routers.todos import todos_bp
from routers.admin import admin_bp
from routers.users import users_bp

app = Flask(__name__)

# Enable CORS
CORS(app)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(todos_bp, url_prefix="/todos")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(users_bp, url_prefix="/user")


# -----------------------------
# FRONTEND ROUTES
# -----------------------------

# Home Page
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Serve HTML Files
@app.route("/<path:filename>")
def serve_files(filename):
    return send_from_directory(".", filename)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

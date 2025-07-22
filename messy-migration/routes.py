from flask import Blueprint, request, jsonify
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_bp = Blueprint('user_bp', __name__)

# Helper function
def valid_email(email):
    return re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email)

@user_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "running"}), 200

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    try:
        conn = get_db_connection()
        users = conn.execute("SELECT id, name, email FROM users").fetchall()
        conn.close()
        return jsonify([dict(user) for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    conn = get_db_connection()
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not name or not email or not password or not valid_email(email):
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"error": "Email already exists"}), 409

    hashed = generate_password_hash(password)
    conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed))
    conn.commit()
    conn.close()
    return jsonify({"message": "User created"}), 201

@user_bp.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not name or not email or not valid_email(email):
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()
    conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated"}), 200

@user_bp.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted"}), 200

@user_bp.route("/search", methods=["GET"])
def search_users():
    name = request.args.get("name", "").strip()
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users]), 200

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    print(data)

    conn = get_db_connection()
    user = conn.execute("SELECT id, password FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if user and user["password"]==password:
        return jsonify({"status": "success", "user_id": user["id"]}), 200
    return jsonify({"status": "failed"}), 401
import re

from flask import Blueprint, request
from psycopg2.errors import OperationalError
from typing import Dict, List, Tuple

from src.database.database import DBConn

users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users() -> Tuple[List[Dict] | str, int]:
    query = "SELECT * FROM Users;"
    try:
        with DBConn() as conn:
            users = conn.execute_query(query, None, returns=True)
        return users, 200
    except OperationalError as e:
        return "Connection failed", 500


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Tuple[List[Dict] | str, int]:
    query = "SELECT * FROM Users WHERE user_id=%s;"
    params = (user_id,)
    try:
        with DBConn() as conn:
            user = conn.execute_query(query, params, returns=True)
        return user, 200
    except OperationalError as e:
        return "Connection failed", 500


@users_bp.route("/users", methods=["POST"])
def create_user() -> Tuple[str, int]:
    if request.content_type == "application/json":
        data = request.json
    elif request.content_type == "application/x-www-form-urlencoded":
        data = request.form
    else:
        return "Unsupported media type", 415

    try:
        params = (data["user_name"], data["user_email"])
    except KeyError as e:
        return e.get_description(), e.code

    email_regex = re.compile("[^@]+@[^@]+\.[^@]+")
    if not email_regex.fullmatch(data["user_email"]):
        return "Invalid email", 422

    query = "INSERT INTO Users (user_name, user_email) VALUES (%s, %s);"
    try:
        with DBConn() as conn:
            conn.execute_query(query, params)
        return "User created", 200
    except OperationalError as e:
        return "Connection failed", 500


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id: int) -> Tuple[str, int]:
    if request.content_type == "application/json":
        data = request.json
    elif request.content_type == "application/x-www-form-urlencoded":
        data = request.form
    else:
        return "Unsupported media type", 415

    if None in data:
        return "Missing parameter", 400

    email_regex = re.compile("[^@]+@[^@]+\.[^@]+")
    if not email_regex.fullmatch(data["user_email"]):
        return "Invalid email", 422

    query = "UPDATE Users SET user_name=%s, user_email=%s WHERE user_id=%s;"
    params = (data["user_name"], data["user_email"], user_id)
    try:
        with DBConn() as conn:
            conn.execute_query(query, params)
        return "User edited", 200
    except OperationalError as e:
        return "Connection failed", 500


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> Tuple[str, int]:
    query = "DELETE FROM Users WHERE user_id=%s;"
    params = (user_id,)
    try:
        with DBConn() as conn:
            conn.execute_query(query, params)
        return "User deleted", 200
    except OperationalError as e:
        return "Connection failed", 500

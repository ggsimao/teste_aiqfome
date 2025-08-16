import json, requests

from flask import Blueprint
from psycopg2.errors import (
    Error,
    ForeignKeyViolation,
    OperationalError,
    UniqueViolation,
)
from typing import Dict, List, Tuple

from src.database.database import DBConn

favorites_bp = Blueprint("favorites_bp", __name__)

# Extensão da URL dos usuários, mas não tem dependência entre elas em código: fácil de ocasionar problemas


@favorites_bp.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id: int) -> Tuple[List[Dict] | str, int]:
    query = "SELECT * FROM Favorites WHERE user_id=%s"
    params = (user_id,)
    try:
        with DBConn() as conn:
            favs = conn.execute_query(query, params, returns=True)
    except OperationalError as e:
        return "Connection failed", 500
    fav_list = []

    response = requests.get(f"https://fakestoreapi.com/products")
    response.raise_for_status()
    prod_all = [
        p
        for p in json.loads(response.content)
        if p["id"] in [f["prod_id"] for f in favs]
    ]

    for p in prod_all:
        p_rlv = dict((k, p[k]) for k in ("id", "title", "image", "price"))
        if rating := p["rating"]:
            p_rlv["rating"] = rating

        fav_list.append(p_rlv)
    return fav_list, 200


@favorites_bp.route("/users/<int:user_id>/favorites/<int:prod_id>", methods=["POST"])
def add_user_favorite(user_id: int, prod_id: int) -> Tuple[str, int]:
    response = requests.get(f"https://fakestoreapi.com/products/{prod_id}")
    response.raise_for_status()
    try:
        prod_all = json.loads(response.content)
    except json.decoder.JSONDecodeError:  # produto não existe
        return "Invalid parameter: prod_id", 422

    query = "INSERT INTO Favorites (prod_id, user_id) VALUES (%s, %s)"
    params = (prod_id, user_id)
    try:
        with DBConn() as conn:
            conn.execute_query(query, params)
        return "Favorite added", 200
    except ForeignKeyViolation:
        return "Invalid parameter: user_id", 422
    except UniqueViolation:
        return "Duplicate data", 422
    except OperationalError as e:
        return "Connection failed", 500


@favorites_bp.route("/user/<int:user_id>/favorites/<int:prod_id>", methods=["DELETE"])
def delete_user_favorite(user_id: int, prod_id: int) -> Tuple[str, int]:
    query = "DELETE FROM Favorites WHERE user_id=%s AND prod_id=%s"
    params = (user_id, prod_id)
    try:
        with DBConn() as conn:
            conn.execute_query(query, params)
        return "Favorite deleted", 200
    except OperationalError as e:
        return "Connection failed", 500

from flask import request, jsonify, Blueprint
from pathlib import Path
import sqlite3
import requests
import os
import time

PLACES_KEY = os.getenv("google_api")
LOCATION = "33.6846,-117.8265"
RADIUS = 5000
BASE = "https://maps.googleapis.com/maps/api/place"
NEARBY = f"{BASE}/nearbysearch/json"
DETAILS = f"{BASE}/details/json"
DB_PATH = Path(__file__).resolve().parent / "irvine_eats.db"


def get_db_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def require_places_key():
    """Raise a clear error if the Google Places API key is missing."""
    if not PLACES_KEY:
        raise RuntimeError(
            "google_api environment variable is not set. "
            "Example (PowerShell): $env:google_api='YOUR_API_KEY'"
        )


def fetch_nearby(latlng: str, radius: int = RADIUS):
    """Yield nearby restaurant search results from Google Places API."""
    require_places_key()

    params = {
        "location": latlng,
        "radius": radius,
        "type": "restaurant",
        "key": PLACES_KEY,
    }

    while True:
        response = requests.get(NEARBY, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()

        status = payload.get("status")
        if status not in {None, "OK", "ZERO_RESULTS"}:
            raise RuntimeError(
                f"Google Places nearby search failed: {status} - "
                f"{payload.get('error_message', 'No error message provided')}"
            )

        for item in payload.get("results", []):
            yield item

        next_token = payload.get("next_page_token")
        if not next_token:
            break

        time.sleep(2)
        params = {"pagetoken": next_token, "key": PLACES_KEY}



def fetch_details(place_id: str):
    """Fetch detailed information for one place."""
    require_places_key()

    fields = (
        "name,formatted_address,types,formatted_phone_number,website,url,"
        "opening_hours"
    )
    params = {
        "place_id": place_id,
        "fields": fields,
        "key": PLACES_KEY,
    }

    response = requests.get(DETAILS, params=params, timeout=10)
    response.raise_for_status()
    payload = response.json()

    status = payload.get("status")
    if status not in {None, "OK"}:
        raise RuntimeError(
            f"Google Places details lookup failed: {status} - "
            f"{payload.get('error_message', 'No error message provided')}"
        )

    return payload.get("result", {})



def get_category(detail_types, hit_types):
    """Pick a restaurant category from Google place types."""
    ignored = {"point_of_interest", "establishment", "food", "restaurant"}
    all_types = detail_types or hit_types or []
    return next((t for t in all_types if t not in ignored), "restaurant")



def get_hours_text(details: dict) -> str:
    """Convert opening_hours.weekday_text into one string for SQLite storage."""
    weekday_text = details.get("opening_hours", {}).get("weekday_text", [])
    return " | ".join(weekday_text) if weekday_text else ""



def upsert_restaurants_from_places(location: str = LOCATION, radius: int = RADIUS) -> int:
    """Fetch restaurants from Places API and upsert them into SQLite."""
    conn = get_db_connection()
    cur = conn.cursor()
    upserted = 0

    try:
        for hit in fetch_nearby(location, radius):
            place_id = hit.get("place_id")
            if not place_id:
                continue

            details = fetch_details(place_id)

            name = details.get("name") or hit.get("name")
            address = details.get("formatted_address") or hit.get("vicinity")
            phone = details.get("formatted_phone_number")
            url = details.get("website") or details.get("url")
            category = get_category(details.get("types", []), hit.get("types", []))
            hours_text = get_hours_text(details)

            cur.execute(
                """
                INSERT INTO restaurants (place_id, name, address, hours, category, phone, url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(place_id) DO UPDATE SET
                    name=excluded.name,
                    address=excluded.address,
                    hours=excluded.hours,
                    category=excluded.category,
                    phone=excluded.phone,
                    url=excluded.url
                """,
                (place_id, name, address, hours_text, category, phone, url),
            )
            upserted += 1

        conn.commit()
        return upserted
    finally:
        conn.close()


# users
USERS_BP = Blueprint("users", __name__, url_prefix="/api/users")


@USERS_BP.route("", methods=["GET"])
def get_users():
    """Return users in the database."""
    user_id = request.args.get("id")
    conn = get_db_connection()
    try:
        if user_id is None:
            users = conn.execute("SELECT * FROM users").fetchall()
        else:
            users = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()
        return jsonify([dict(u) for u in users])
    finally:
        conn.close()


@USERS_BP.route("", methods=["POST"])
def add_user():
    """Add a new user to the database."""
    data = request.get_json() or {}
    required = {"id", "pw", "name", "email"}
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (id, pw, name, email) VALUES (?, ?, ?, ?)",
            (data["id"], data["pw"], data["name"], data["email"]),
        )
        conn.commit()
        return jsonify({"message": "user added"}), 201
    finally:
        conn.close()


# restaurants
RESTAURANTS_BP = Blueprint("restaurants", __name__, url_prefix="/api/restaurants")


@RESTAURANTS_BP.route("", methods=["GET"])
def get_restaurants():
    """Return restaurants in the database."""
    rest_id = request.args.get("restaurant_id")
    conn = get_db_connection()
    try:
        if rest_id is None:
            restaurants = conn.execute("SELECT * FROM restaurants").fetchall()
        else:
            restaurants = conn.execute(
                "SELECT * FROM restaurants WHERE restaurant_id = ?",
                (rest_id,),
            ).fetchall()
        return jsonify([dict(r) for r in restaurants])
    finally:
        conn.close()


@RESTAURANTS_BP.route("/seed", methods=["POST"])
def seed_restaurants_api():
    """Fetch nearby restaurants from Google Places and upsert them into SQLite."""
    body = request.get_json(silent=True) or {}
    location = body.get("location", LOCATION)
    radius = body.get("radius", RADIUS)

    try:
        upserted = upsert_restaurants_from_places(location=location, radius=radius)
        return jsonify({"message": f"{upserted} restaurants upserted"}), 201
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500
    except requests.RequestException as exc:
        return jsonify({"error": f"Google Places request failed: {exc}"}), 502


# menu
MENU_BP = Blueprint("menu", __name__, url_prefix="/api/menu")


@MENU_BP.route("", methods=["GET"])
def get_menu():
    """Return menu items in the database."""
    item_id = request.args.get("item_id")
    conn = get_db_connection()
    try:
        if item_id is None:
            menu_items = conn.execute("SELECT * FROM menu").fetchall()
        else:
            menu_items = conn.execute(
                "SELECT * FROM menu WHERE item_id = ?",
                (item_id,),
            ).fetchall()
        return jsonify([dict(m) for m in menu_items])
    finally:
        conn.close()


# hours
HOURS_BP = Blueprint("hours", __name__, url_prefix="/api/hours")


@HOURS_BP.route("", methods=["POST"])
def add_hours():
    """Add new hours to the database."""
    data = request.get_json() or {}
    required = {"restaurant_id", "day", "open_time", "close_time"}
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO hours (restaurant_id, day, open_time, close_time) VALUES (?, ?, ?, ?)",
            (data["restaurant_id"], data["day"], data["open_time"], data["close_time"]),
        )
        conn.commit()
        return jsonify({"message": "hours added"}), 201
    finally:
        conn.close()


# review
REVIEW_BP = Blueprint("review", __name__, url_prefix="/api/reviews")


@REVIEW_BP.route("", methods=["GET"])
def get_reviews():
    """Return reviews in the database."""
    review_id = request.args.get("review_id")
    conn = get_db_connection()
    try:
        if review_id is None:
            reviews = conn.execute("SELECT * FROM reviews").fetchall()
        else:
            reviews = conn.execute(
                "SELECT * FROM reviews WHERE review_id = ?",
                (review_id,),
            ).fetchall()
        return jsonify([dict(r) for r in reviews])
    finally:
        conn.close()


@REVIEW_BP.route("", methods=["POST"])
def add_review():
    """Add a new review to the database."""
    data = request.get_json() or {}
    required = {"user_id", "restaurant_id", "rating", "comment"}
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO reviews (user_id, restaurant_id, rating, comment) VALUES (?, ?, ?, ?)",
            (data["user_id"], data["restaurant_id"], data["rating"], data["comment"]),
        )
        conn.commit()
        return jsonify({"message": "review added"}), 201
    finally:
        conn.close()


# auth
AUTH_BP = Blueprint("auth", __name__, url_prefix="/api/auth")


@AUTH_BP.route("/login", methods=["POST"])
def login():
    """Log the user in if login info is verified."""
    data = request.get_json() or {}
    username = data.get("id")
    password = data.get("pw")

    if not username or not password:
        return jsonify({"error": "id and pw are required"}), 400

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE id = ? AND pw = ?",
            (username, password),
        ).fetchone()
    finally:
        conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid username or password"}), 401


# favorite restaurants
FAV_REST_BP = Blueprint("fav_rest", __name__, url_prefix="/api/favorite-restaurants")


@FAV_REST_BP.route("", methods=["GET"])
def get_fav_restaurants():
    """Return favorite restaurants for a user."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = get_db_connection()
    try:
        favorites = conn.execute(
            "SELECT * FROM favorite_restaurants WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        return jsonify([dict(f) for f in favorites])
    finally:
        conn.close()


@FAV_REST_BP.route("", methods=["POST"])
def save_fav_restaurant():
    """Save a favorite restaurant for a user."""
    data = request.get_json() or {}
    required = {"user_id", "restaurant_id"}
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO favorite_restaurants (user_id, restaurant_id) VALUES (?, ?)",
            (data["user_id"], data["restaurant_id"]),
        )
        conn.commit()
        return jsonify({"message": "favorite restaurant added"}), 201
    finally:
        conn.close()
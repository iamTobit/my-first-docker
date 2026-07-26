from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import logging

from config import get_config

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(get_config())

# Enable CORS for all routes
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
)


def get_db_connection():
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Multi-Tier Web Application API",
        "status": "running"
    })


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "status": "healthy"
        })

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


@app.route("/products")
def products():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        return jsonify({
            "success": True,
            "count": len(products),
            "products": products
        })

    except Exception as e:
        logging.exception(e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
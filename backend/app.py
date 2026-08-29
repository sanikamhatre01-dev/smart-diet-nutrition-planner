from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text

from database.database import engine

from backend.routes.user_routes import user_bp
from backend.routes.health_routes import health_bp
from backend.routes.goal_routes import goal_bp
from backend.routes.food_routes import food_bp
from backend.routes.meal_routes import meal_bp
from backend.routes.tracking_routes import tracking_bp
from backend.routes.preference_routes import preference_bp
from backend.routes.category_routes import category_bp
from backend.routes.nutrition_routes import nutrition_bp
from backend.routes.recommendation_routes import recommendation_bp


app = Flask(__name__)
CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(health_bp)
app.register_blueprint(goal_bp)
app.register_blueprint(food_bp)
app.register_blueprint(meal_bp)
app.register_blueprint(tracking_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(category_bp)
app.register_blueprint(nutrition_bp)
app.register_blueprint(recommendation_bp)


@app.route("/")
def home():
    return jsonify({
        "message": "Smart Diet & Nutrition Planner Backend is running!"
    })


@app.route("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return jsonify({
            "status": "success",
            "database": "connected"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "not connected",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
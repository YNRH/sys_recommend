
from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from .recommender import recommend_movie
from .models import User
from .database import SessionLocal

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def hola():
    return "Hola, probando la ruta de recomendaciones¡"

def get_user_id_by_cookie(cookie_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.cookie_id == cookie_id).first()
        return user.user_id if user else None
    finally:
        db.close()

@main_bp.route('/recommend/<string:cookie_id>', methods=['GET'])
def recommend_by_cookie(cookie_id):
    db = SessionLocal()
    try:
        user_id = get_user_id_by_cookie(cookie_id)
        if user_id is None:
            return jsonify({"error": "User not found"}), 404

        recommendation = recommend_movie(user_id=user_id)
        return jsonify(recommendation)
    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        return jsonify({"error": "An error occurred while generating recommendations"}), 500
    finally:
        db.close()

app.register_blueprint(main_bp)
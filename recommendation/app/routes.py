from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from .recommender import recommend_movies
from .models import User
from .database import SessionLocal

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def hola():
    return "Hola, probando la ruta de recomendaciones¡"

@main_bp.route('/recommend', methods=['GET'])
def recommend():
    recommendations = recommend_movies()
    return jsonify(recommendations)

@main_bp.route('/recommend/<string:cookie_id>', methods=['GET'])
def recommend_by_cookie(cookie_id):
    # Aquí debes obtener el user_id basado en el cookie_id
    user_id = get_user_id_by_cookie(cookie_id)
    recommendations = recommend_movies(user_id=user_id)
    return jsonify(recommendations)

def get_user_id_by_cookie(cookie_id):
    db = SessionLocal()
    user = db.query(User).filter(User.cookie_id == cookie_id).first()
    db.close()
    return user.user_id if user else None

app.register_blueprint(main_bp)

from flask import Blueprint,request,jsonify
from models import User
from config import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from config import bcrypt


auth = Blueprint('auth', __name__)


@auth.post('/signup')
def signup():
    data = request.json
    if not data:
     return jsonify({"message": "Invalid request data"}), 400
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return (
            jsonify({"message": "You must fill out all of the fields"}),400
        )
    new_user = User(username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'), email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
     return jsonify({"message": "An error occurred. Please try again."}), 500
    return jsonify({"message": "User was created"})


@auth.post('/login')
def login():
    data = request.json
    if not data:
     return jsonify({"message": "Invalid request data"}), 400
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid username or password"}), 401



from flask import Blueprint,request,jsonify
from models import Playlist
from config import db



playlist = Blueprint('playlist', __name__)
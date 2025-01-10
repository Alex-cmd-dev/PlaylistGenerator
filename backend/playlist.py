from flask import Blueprint, request, jsonify
from models import Playlist,PlaylistSong,User,Song
from config import db
from spotify import get_spotify_token
import logging

playlist = Blueprint('playlist', __name__)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@playlist.post('/save')#needs work
def save_playlist():
    pass
    




@playlist.get('/playlist/<int:id>')
def see_playlist(id):
    saved_playlist = Playlist.query.get_or_404(id)
    return jsonify({"playlist": saved_playlist.to_json()}), 200


@playlist.get('/saved')
def viewplaylists():
    saved_p = Playlist.query.all()
    if not saved_p:
        return jsonify({"message": "No saved playlists"}), 404
    return jsonify({"savedPlaylist": [playlist.to_json() for playlist in saved_p]})


@playlist.delete('/delete/<int:id>')
def delete_playlist(id):
    saved_playlist = Playlist.query.get_or_404(id)
    db.session.delete(saved_playlist)
    db.session.commit()
    return jsonify({"message": f"Playlist with id {id} removed successfully."})


@playlist.get('/generate')
def generate_playlist():
    pass

from flask import Blueprint, request, jsonify
from models import Playlist,PlaylistSong,User,Song
from config import db
import logging

playlist = Blueprint('playlist', __name__)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@playlist.post('/save')#needs work
def save_playlist():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid request"}), 400

    playlistName = data.get('playlistName')
    playlistMood = data.get('mood')
    playlistUser = data.get('userID')  # Assuming this is user_id
    playlistSongs = data.get('songs')  # List of song data dictionaries

    # Validate required fields
    if not playlistName or not playlistUser:
        return jsonify({"message": "Playlist name and user ID are required."}), 400

    if not isinstance(playlistSongs, list):
        return jsonify({"message": "Songs should be a list of song data."}), 400

    user = User.query.get(playlistUser)
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    new_playlist = Playlist(
        name=playlistName,
        mood=playlistMood,
        user_id=user.id
    )

    try:
        db.session.add(new_playlist)
        db.session.flush()  # Get playlist ID before committing

        # Add songs and their association with the playlist
        for song_data in playlistSongs:
            # Extract song details
            title = song_data.get('title')
            artist = song_data.get('artist')
            spotify_id = song_data.get('spotify_id')
            mood = song_data.get('mood', None)

            # Ensure mandatory song fields are present
            if not title or not artist or not spotify_id:
                return jsonify({"message": "Each song must have a title, artist, and spotify_id."}), 400

            # Create a new song
            new_song = Song(
                title=title,
                artist=artist,
                spotify_id=spotify_id,
                mood=mood
            )
            db.session.add(new_song)  # Add song to session
            db.session.flush()  # Get son
            playlist_song = PlaylistSong(playlist_id=new_playlist.id, song_id=new_song.id)
            db.session.add(playlist_song)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error saving playlist: {e}")
        db.session.rollback()
        return jsonify({"message": "An error occurred while saving the playlist."}), 500

    return jsonify({"message": "Playlist saved successfully!"}), 201



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

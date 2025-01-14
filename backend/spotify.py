from flask import Blueprint, redirect, session, request, jsonify
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy import Spotify
from dotenv import load_dotenv
import os
from time import time

spotify = Blueprint('spotify', __name__)
load_dotenv()


scope = "playlist-modify-public playlist-modify-private"


sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope=scope
)

auth_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
)
sp = Spotify(auth_manager=auth_manager)

@spotify.route('/login')
def login():
    return redirect(sp_oauth.get_authorize_url())


@spotify.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Authorization code not provided"}), 400
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(os.getenv('SPOTIFY_REDIRECT_URI'))  

def get_spotify_token():
    token_info = session.get('token_info')
    if not token_info:
        return None

    if time() > token_info.get('expires_at', 0):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info

    return token_info
def get_user_spotify():
    token_info = get_spotify_token()
    if not token_info:
        raise Exception("User token not available or expired")
    return Spotify(auth=token_info['access_token'])

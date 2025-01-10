from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(50), unique=True, nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)  
    password = db.Column(db.String(255), nullable=False) 


    playlists = db.relationship('Playlist', backref='user', lazy=True)

class Playlist(db.Model):

    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    mood = db.Column(db.String(50), nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  


    songs = db.relationship('Song', secondary='playlist_song', lazy='subquery', backref=db.backref('playlists', lazy=True))
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "mood": self.mood,
            "user_id": self.user_id,
            "songs": self.songs
        }


class Song(db.Model):

    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False) 
    artist = db.Column(db.String(100), nullable=False)  
    spotify_id = db.Column(db.String(50), unique=True, nullable=False)  
    mood = db.Column(db.String(50), nullable=True)

    def to_json(self):
        return{
            "id": self.id,
            "title": self.title,
            "mood": self.mood,
            "spotify_id": self.spotify_id,
            "artist": self.artist
        }

class PlaylistSong(db.Model):
    __tablename__ = 'playlist_song'

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)  
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)  

class MoodAnalysis(db.Model):

    __tablename__ = 'mood_analysis'


    id = db.Column(db.Integer, primary_key=True)  
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)  
    mood = db.Column(db.String(50), nullable=False)  
    confidence = db.Column(db.Float, nullable=False)  

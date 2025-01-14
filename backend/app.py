from config import app, db
from auth import auth
from playlist import playlist
from spotify import spotify
import os


app.secret_key = os.getenv("FLASK_SECRET_KEY")


app.register_blueprint(auth)
app.register_blueprint(playlist)
app.register_blueprint(spotify, url_prefix='/spotify')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        

    app.run(debug=True)
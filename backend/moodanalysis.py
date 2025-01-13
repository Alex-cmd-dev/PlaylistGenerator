from transformers import pipeline
from spotify import sp

sentiment_pipeline = pipeline("sentiment-analysis", framework="tf")


def fetch_songs():
    results = sp.search(q="genre:pop", type="track", limit=10)
    tracks = results["tracks"]["items"]
    return [{"title": track["name"], "artist": track["artists"][0]["name"]} for track in tracks]


def mood_analysis(mood):
    result = sentiment_pipeline(mood)
    return True




def create_playlist():
    pass


songs = fetch_songs()
print(songs)




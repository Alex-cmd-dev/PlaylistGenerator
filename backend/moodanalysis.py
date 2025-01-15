from transformers import pipeline
from spotify import get_user_spotify
import spacy

sentiment_pipeline = pipeline("sentiment-analysis", framework="tf",
    model="distilbert-base-uncased-finetuned-sst-2-english")
nlp = spacy.load("en_core_web_md")

moods = {
    "POSITIVE": {
        "excited": ["excited", "joyful", "cheerful", "ecstatic"],
        "relaxed": ["peaceful", "grateful", "content", "relaxed"]
    },
    "NEGATIVE": {
        "angry": ["angry", "frustrated", "annoyed", "pissed off"],
        "lonely": ["lonely", "isolated", "alone", "forgotten"],
        "tired": ["tired", "exhausted", "drained", "burned out"],
        "sad": ["sad", "heartbroken", "crying", "depressed", "down", "melancholy"],
        "fearful": ["fearful", "scared", "anxious", "nervous", "worried", "terrified", "panicked"]
    },
    "NEUTRAL": {
        "calm": ["calm", "fine", "okay", "neutral"],
        "focused": ["focused", "studying", "productive"]
    }
}

mood_to_music = {
    "excited": {
        "seed_genres": ["pop", "dance"],
        "audio_features": {"min_energy": 0.7, "min_valence": 0.6}
    },
    "relaxed": {
        "seed_genres": ["chill", "acoustic"],
        "audio_features": {"max_energy": 0.5, "max_danceability": 0.4}
    },
    "angry": {
        "seed_genres": ["rock", "metal"],
        "audio_features": {"min_energy": 0.8}
    },
    "lonely": {
        "seed_genres": ["sad"],
        "audio_features": {"max_valence": 0.3, "max_energy": 0.4}
    },
    "tired": {
        "seed_genres": ["relaxing", "ambient"],
        "audio_features": {"max_energy": 0.4, "tempo": {"max": 90}}
    },
    "sad": {
        "seed_genres": ["melancholy", "piano"],
        "audio_features": {"max_valence": 0.4, "max_energy": 0.3}
    },
    "fearful": {
        "seed_genres": ["calming", "ambient"],
        "audio_features": {"max_energy": 0.5, "min_valence": 0.2}
    },
    "calm": {
        "seed_genres": ["ambient", "classical"],
        "audio_features": {"max_energy": 0.4, "min_valence": 0.4}
    },
    "focused": {
        "seed_genres": ["instrumental", "study"],
        "audio_features": {"min_energy": 0.4, "min_instrumentalness": 0.5}
    }
}




def mood_analysis(text):
   
    result = sentiment_pipeline(text)
    label = result[0]['label']
    score = result[0]['score']

    input_doc = nlp(text)

    best_mood = label.lower()
    best_similarity = 0.0


    for refined_mood, words in moods[label].items():
        for word in words:
            keyword_doc = nlp(word)
            similarity = input_doc.similarity(keyword_doc)
            if similarity > best_similarity:
                best_mood = refined_mood
                best_similarity = similarity

    return {
        "mood": best_mood,
        "confidence": score
    }




def create_playlist():
    pass


def fetch_songs(results):
    mood = results.get('mood')
    query = mood_to_music.get(mood)

    search_query = "genre:" + " ".join(query.get("seed_genres", ["pop"]))

    try:
        user_sp = get_user_spotify()
        search_results = user_sp.search(q=search_query, type="track", limit=50)
        return search_results["tracks"]["items"]  # Returns raw tracks for filtering
    except Exception as e:
        print(f"Error searching tracks: {e}")
        return []
    










from transformers import pipeline
from spotify import sp
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



def fetch_songs():
    results = sp.search(q="", type="track", limit=50)
    tracks = results["tracks"]["items"]


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
                print(similarity)
                best_similarity = similarity

    return {
        "mood": best_mood,
        "confidence": score
    }


print(mood_analysis("Im gonna crashout"))


def create_playlist():
    pass





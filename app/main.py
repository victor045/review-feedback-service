from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI(
    title="Product Review Feedback API",
    description="API que analiza reseñas de productos y devuelve una retroalimentación estructurada: sentimiento, legibilidad y sugerencias.",
    version="1.0.0",
    contact={
        "name": "Víctor Fernando",
        "email": "tu_email@dominio.com",
        "url": "https://github.com/tu_usuario"
    }
)

# Simulated positive and negative words for sentiment
POSITIVE_WORDS = {"good", "great", "excellent", "love", "amazing"}
NEGATIVE_WORDS = {"bad", "terrible", "awful", "hate", "poor"}

class Review(BaseModel):
    content: str = Field(..., example="I love this product! It's excellent and easy to use.")

class Feedback(BaseModel):
    sentiment: str = Field(..., example="positive")
    readability_score: float = Field(..., example=12.5)
    suggestions: str = Field(..., example="Looks good!")

def analyze_sentiment(text: str) -> str:
    words = text.lower().split()
    pos_count = sum(1 for word in words if word in POSITIVE_WORDS)
    neg_count = sum(1 for word in words if word in NEGATIVE_WORDS)
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

def calculate_readability(text: str) -> float:
    words = text.split()
    num_words = len(words)
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    num_sentences = max(1, num_sentences)  # avoid division by zero
    return round(num_words / num_sentences, 2)  # simplified score

def generate_suggestions(text: str) -> str:
    suggestions = []
    if len(text.split()) > 50:
        suggestions.append("Consider shortening the review.")
    if any(word == word.upper() and len(word) > 2 for word in text.split()):
        suggestions.append("Avoid using all caps.")
    if not suggestions:
        suggestions.append("Looks good!")
    return " ".join(suggestions)

@app.post("/review", response_model=Feedback, summary="Analiza una reseña de producto", tags=["Reviews"])
def review_endpoint(review: Review):
    if not review.content:
        raise HTTPException(status_code=400, detail="Review content cannot be empty")

    sentiment = analyze_sentiment(review.content)
    readability_score = calculate_readability(review.content)
    suggestions = generate_suggestions(review.content)

    return Feedback(
        sentiment=sentiment,
        readability_score=readability_score,
        suggestions=suggestions
    )

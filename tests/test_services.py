from app.main import analyze_sentiment, calculate_readability, generate_suggestions

def test_analyze_sentiment_logic():
    assert analyze_sentiment("I love this product, it is amazing!") == "positive"
    assert analyze_sentiment("I hate this item, it's the worst!") == "negative"
    assert analyze_sentiment("This is a pen.") == "neutral"

def test_readability_score():
    assert calculate_readability("This is a sentence.") > 0

def test_suggestions_logic():
    assert "shortening" in generate_suggestions("word " * 60)
    assert "all caps" in generate_suggestions("THIS IS BAD")
    assert "Looks good" in generate_suggestions("Nice and short.")

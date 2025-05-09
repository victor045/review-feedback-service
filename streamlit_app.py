import streamlit as st
import requests

st.set_page_config(page_title="Product Review Analysis", page_icon="📝")
st.title("📝 Product Review Feedback")
st.markdown("Write a review and get sentiment, readability, and improvement suggestions.")

review = st.text_area("Your Review", height=200, placeholder="Example: I loved this product, it was excellent.")

if st.button("Analyze"):
    if not review.strip():
        st.warning("Please enter a review.")
    else:
        try:
            response = requests.post("http://localhost:8000/review", json={"content": review})
            if response.status_code == 200:
                result = response.json()
                st.success(f"🎯 Sentiment: {result['sentiment'].capitalize()}")
                st.info(f"📚 Readability: {result['readability_score']}")
                st.write(f"💡 Suggestions: {result['suggestions']}")
            else:
                st.error("❌ Error while analyzing review.")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Could not connect to the backend. Is the API running?")


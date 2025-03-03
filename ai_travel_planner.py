import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from googletrans import Translator  # For translation
import os
import gtts  # For text-to-speech
import base64  # For audio playback

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
if not GOOGLE_API_KEY:
    st.error("Missing Google API Key. Please configure your API Key.")

# 🌍 Supported Languages
language_codes = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta"
}

# 🎨 Streamlit UI Setup
st.set_page_config(
    page_title="🌍 Plan My Trip",
    page_icon="✈",
    layout="wide"
)

# 💅 Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        background-image: url('https://source.unsplash.com/1600x900/?travel');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border: 2px solid #4a90e2 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #4a90e2, #ff7eb3) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-size: 18px !important;
        transition: transform 0.2s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.1) !important;
    }
    .travel-card {
        padding: 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin: 20px 0;
        max-height: 400px;
        overflow: auto;
    }
    .footer {
        text-align: center;
        padding: 20px;
        background: #4a90e2;
        color: white;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div style="text-align: center; margin-bottom: 50px;">
    <h1>🌍 Plan My Trip</h1>
    <p>Your Personalized AI-Powered Travel Planner</p>
</div>
""", unsafe_allow_html=True)

# 📋 UI Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("🏙 Departure City", placeholder="New York")
        destination = st.text_input("🌆 Destination City", placeholder="Paris")
        travel_date = st.date_input("📅 Travel Date")
        language = st.selectbox("🌍 Language", list(language_codes.keys()))

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("💰 Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("🎯 Travel Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel", "Adventure"])
        email = st.text_input("📧 Receive Itinerary via Email (Optional)")

# 🧠 AI Travel Plan Generator
def get_travel_plan(source, destination, currency, budget, language, preferences):
    prompt_template = f"""
    You are an AI travel expert. Generate a comprehensive travel itinerary from {source} to {destination} in {language}.

    *Plan Should Include:*
    - Best flights/trains/buses with estimated cost
    - Top-rated hotels with detailed descriptions
    - Famous places to visit with detailed descriptions
    - Local food & restaurants
    - Weather information
    - Pilgrimage places (if any)
    - Transportation options
    - Budget breakdown
    - Essential travel tips

    *Currency:* {currency}
    *Budget:* {budget[0]} - {budget[1]} USD
    *Preferences:* {", ".join(preferences) if preferences else "Standard travel"}
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    messages = [
        SystemMessage(content="You are an AI travel expert."),
        HumanMessage(content=prompt_template)
    ]
    response = model.invoke(messages)
    return response.content

# 🔊 Text-to-Speech Function
def text_to_speech(text, language_code):
    try:
        tts = gtts.gTTS(text, lang=language_code)
        tts.save("output.mp3")
        with open("output.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()
        return audio_bytes
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

# 🚀 Generate Itinerary Button
if st.button("Generate Itinerary ✈"):
    if source and destination:
        with st.spinner("Generating your personalized travel itinerary..."):
            try:
                travel_plan = get_travel_plan(source, destination, currency, budget, language, preferences)
                st.markdown(f"""
                <div class="travel-card">
                    <h3>🌍 Your Travel Itinerary from {source} to {destination}</h3>
                    <p>{travel_plan}</p>
                </div>
                """, unsafe_allow_html=True)

                # 🔊 Speak Button
                st.markdown("### 🔊 Listen to Your Itinerary")
                audio_bytes = text_to_speech(travel_plan, language_codes[language])
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please fill all required fields!")

# Footer
st.markdown("""
<div class="footer">
    Created by Gopichand Challa
</div>
""", unsafe_allow_html=True)

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from googletrans import Translator  # For translation
import os

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

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
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
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
    .custom-title {
        color: #ff7eb3;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 50px;">
    <h1 class="custom-title">🌍 Plan My Trip</h1>
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
def get_travel_plan(source, destination, currency, budget, language):
    prompt_template = f"""
    You are an AI travel expert. Generate a comprehensive travel itinerary from {source} to {destination} in {language}.

    *Plan Should Include:*
    - Best flights/trains/buses with estimated cost
    - Top-rated hotels with detailed descriptions
    - Famous places to visit with descriptions
    - Local food & restaurants with descriptions
    - Weather information
    - Pilgrimage places (if any)
    - Transportation options with pricing
    - Budget breakdown
    - Essential travel tips

    *Currency:* {currency}
    *Budget:* {budget[0]} - {budget[1]} USD
    *Preferences:* {", ".join(preferences) if preferences else "Standard travel"}
    """
    model = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY)
    messages = [SystemMessage(content=prompt_template)]
    response = model.predict(messages=messages)
    return response

if st.button("Generate Itinerary ✈"):
    if source and destination:
        with st.spinner("Generating your personalized travel itinerary..."):
            travel_plan = get_travel_plan(source, destination, currency, budget, language)
            st.markdown(f"""
            <div class="travel-card">
                <h3>🌍 Your Travel Itinerary from {source} to {destination}</h3>
                <p>{travel_plan}</p>
            </div>
            """, unsafe_allow_html=True)

            st.download_button("📄 Download Itinerary as PDF", travel_plan, file_name=f"{source}_to_{destination}_Itinerary.pdf")
    else:
        st.warning("Please fill all required fields!")

st.markdown("""
<div class="footer">
    Created by Gopichand Challa
</div>
""", unsafe_allow_html=True)

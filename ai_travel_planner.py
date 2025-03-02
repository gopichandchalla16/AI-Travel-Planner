import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from googletrans import Translator
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
    page_title="🌍 Plan My Trip - AI Powered Travel Planner",
    page_icon="✈",
    layout="wide"
)

# 💅 Custom CSS for Better UI
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        color: #2C3E50;
        background-color: #ECF0F1;
    }
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border: 2px solid #2980B9 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #2980B9, #6DD5FA) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 35px !important;
        font-size: 18px !important;
        transition: transform 0.3s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.1) !important;
    }
    .travel-card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
        background: white;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    .sidebar {
        background: white !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .sidebar h2, .sidebar p {
        color: #2980B9 !important;
    }
    .footer {
        text-align: center;
        padding: 20px;
        background: #2980B9;
        color: white;
        border-radius: 15px;
        margin-top: 40px;
    }
    .hero-section {
        text-align: center;
        padding: 50px 0;
        background: linear-gradient(135deg, #2980B9, #6DD5FA);
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3.5em;">🌍 Plan My Trip - AI Powered Travel Planner</h1>
    <p style="font-size: 1.4em;">Personalized Travel Itineraries at Your Fingertips</p>
</div>
""", unsafe_allow_html=True)

# 📋 Input Section
with st.expander("✈ Start Planning Your Trip", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("🏙 Departure City", placeholder="New York")
        destination = st.text_input("🌆 Destination City", placeholder="Paris")
        travel_date = st.date_input("📅 Travel Date")
        language = st.selectbox("🌍 Language", list(language_codes.keys()))

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "INR", "GBP"])
        budget = st.slider("💰 Budget Range ($)", 100, 10000, (500, 3000))
        preferences = st.multiselect("🎯 Preferences", ["Budget Travel", "Luxury Travel", "Adventure", "Eco-friendly"])
        email = st.text_input("📧 Receive Itinerary via Email")

# AI Function
def get_travel_plan(source, destination, currency, budget, language):
    prompt = f"""
    You are an AI travel assistant. Generate a detailed travel itinerary from {source} to {destination} in {language}.
    Include transportation, hotels, places to visit, food recommendations, weather forecast, and budget breakdown.
    Budget range: {budget[0]} - {budget[1]} {currency}
    Preferences: {', '.join(preferences) if preferences else 'Standard'}
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)
    try:
        response = llm.invoke([SystemMessage(content="AI Travel Expert"), HumanMessage(content=prompt)])
        return response.content if response else "⚠ No response from AI."
    except Exception as e:
        return f"❌ Error: {e}"

# 🚀 Generate Plan
if st.button("🚀 Generate Itinerary"):
    if not source or not destination:
        st.warning("⚠ Please enter both cities!")
    else:
        with st.spinner("🔍 Creating your personalized travel plan..."):
            plan = get_travel_plan(source, destination, currency, budget, language)
        st.success("🎉 Your Itinerary is Ready!")
        st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

# 📌 Sidebar
with st.sidebar:
    st.markdown("## How It Works")
    st.markdown("✔ Enter travel details\n✔ Select preferences & budget\n✔ Click 'Generate Itinerary'\n✔ Get your AI-powered plan instantly")

# Footer
st.markdown("""
<div class="footer">
    <p>🌟 Created by Gopichand Challa | Powered by Google Gemini 🌟</p>
</div>
""", unsafe_allow_html=True)

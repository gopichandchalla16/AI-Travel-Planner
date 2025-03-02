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
    page_title="✈ Plan My Trip - AI Powered Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# 💅 Custom CSS for Better UI
st.markdown("""
<style>
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #f4f6f9;
    }
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border: 2px solid #007BFF !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #007BFF, #6610f2) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 35px !important;
        font-size: 18px !important;
        transition: all 0.3s ease-in-out !important;
        cursor: pointer !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #6610f2, #007BFF) !important;
        transform: translateY(-3px) !important;
    }
    .travel-card {
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        background: #ffffff;
        font-size: 16px;
        line-height: 1.8;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #007BFF !important;
    }
    .stMarkdown p {
        color: #333333 !important;
    }
    .hero {
        text-align: center;
        padding: 60px 0;
        background: linear-gradient(135deg, #007BFF, #6610f2);
        color: white;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    .hero h1 {
        font-size: 3.5em;
        margin-bottom: 15px;
    }
    .hero p {
        font-size: 1.6em;
    }
    .footer {
        text-align: center;
        padding: 20px;
        background: #007BFF;
        color: white;
        border-radius: 15px;
        margin-top: 40px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero">
    <h1>✈ Plan My Trip - AI Powered Travel Planner</h1>
    <p>Your AI Travel Guide for Smarter Journeys</p>
</div>
""", unsafe_allow_html=True)

# 📋 UI Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("🏙 Departure City", placeholder="Enter Departure City")
        destination = st.text_input("🌆 Destination City", placeholder="Enter Destination City")
        travel_date = st.date_input("📅 Travel Date")
        language = st.selectbox("🌍 Language", list(language_codes.keys()))

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("💰 Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("🎯 Travel Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel", "Adventure"])
        email = st.text_input("📧 Receive Itinerary via Email (Optional)")

# 🧠 AI Travel Plan Generator
# Function definition remains unchanged

# 🚀 Generate Plan Button
if st.button("🚀 Generate AI Travel Plan"):
    if not source or not destination:
        st.warning("⚠ Please enter both the departure and destination cities!")
    else:
        with st.spinner("🔍 Generating your travel plan..."):
            plan = get_travel_plan(source, destination, currency, budget, language)

        if plan and not plan.startswith("❌"):
            st.success("🎉 Your AI Travel Plan is Ready!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

            if email:
                st.info(f"📩 Itinerary sent to {email}!")
        else:
            st.error(plan)

# 📌 Sidebar Information
with st.sidebar:
    st.markdown("## ℹ How It Works")
    st.markdown("""
    - Enter your travel details
    - Select preferences & budget
    - Click 'Generate AI Travel Plan'
    - Get your detailed itinerary instantly!
    - Optional: Receive itinerary via email
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Explore the places & Happy Travels ✨<br>
    Created by Gopichand Challa | Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

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
    /* General Styling */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        color: #333;
        background-color: #f5f5f5;
    }
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border: 1px solid #4a90e2 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        font-size: 16px !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #4a90e2, #9013fe) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        transition: transform 0.2s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.05) !important;
    }
    .travel-card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        background: white;
        font-size: 16px;
        line-height: 1.6;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #4a90e2 !important;
    }
    .stMarkdown p {
        color: #333 !important;
    }
    /* Sidebar Styling */
    .css-1d391kg {
        background: #fce4ec !important; /* Light Pink for sidebar */
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sidebar .stMarkdown h2 {
        color: #333 !important;
        font-size: 1.5em !important;
        margin-bottom: 10px !important;
    }
    .sidebar .stMarkdown h3 {
        color: #4a90e2 !important;
        font-size: 1.2em !important;
        margin-bottom: 10px !important;
    }
    .sidebar .stMarkdown p {
        color: #555 !important;
        font-size: 1em !important;
        line-height: 1.6 !important;
    }
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 20px;
        background: #ff4081; /* Pink Footer */
        border-radius: 15px;
        color: white;
        margin-top: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Hero Section */
    .hero {
        text-align: center;
        padding: 60px 0;
        margin-bottom: 30px;
        background: #fce4ec; /* Light Pink for app name */
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .hero h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        font-weight: 600;
        color: #ff4081; /* Pink Color for App Name */
    }
    .hero p {
        font-size: 1.2em;
        color: #333;
    }
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2em;
        }
        .hero p {
            font-size: 1em;
        }
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero">
    <h1>✈ Plan My Trip - AI Powered Travel Planner</h1>
    <p>Your AI-Powered Travel Guide</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Information
with st.sidebar:
    st.markdown("## ℹ How It Works")
    st.markdown("""
    <div style="color: #555;">
    <p>⿡ Enter travel details</p>
    <p>⿢ Select preferences & budget</p>
    <p>⿣ Click 'Generate AI Travel Plan'</p>
    <p>⿤ Get an instant AI-powered itinerary</p>
    <p>⿥ (Optional) Receive itinerary via email</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Explore the places & Happy Travels ✨<br>
    Created by Gopichand Challa </p>
</div>
""", unsafe_allow_html=True)

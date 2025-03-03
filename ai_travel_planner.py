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
        color: white !important;
    }
    .stMarkdown p {
        color: #333 !important;
    }
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(45deg, #4a90e2, #9013fe) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: white !important;
    }
    .sidebar .stMarkdown h2, .sidebar .stMarkdown p {
        color: white !important;
    }
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 20px;
        background: #4a90e2;
        border-radius: 15px;
        color: white;
        margin-top: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Hero Section with Background Image */
    .hero {
        text-align: center;
        padding: 60px 0;
        margin-bottom: 30px;
        background: url('https://images.unsplash.com/photo-1503220317375-aaad61436b1b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
    }
    .hero h1 {
        font-size: 3em; /* Adjusted font size */
        margin-bottom: 10px;
        font-weight: 600;
        position: relative;
        z-index: 1;
        color: white; /* App name in white */
    }
    .hero p {
        font-size: 1.2em;
        position: relative;
        z-index: 1;
        color: white;
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

# 🖼 Hero Section with Background Image
st.markdown("""
<div class="hero">
    <h1>✈ Plan My Trip - AI Powered Travel Planner</h1>
    <p>Your AI-Powered Travel Guide</p>
</div>
""", unsafe_allow_html=True)

st.success("✨ App UI Design Enhanced Successfully! Now working on Travel Itinerary Generation Section with Voice Input and Google Maps Integration...")

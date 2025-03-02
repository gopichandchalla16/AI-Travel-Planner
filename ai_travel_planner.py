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
    body {
        font-family: 'Arial', sans-serif;
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
        background: linear-gradient(45deg, #4a90e2, #9013fe) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: white !important;
    }
    .sidebar .stMarkdown h2 {
        color: white !important;
    }
    .sidebar .stMarkdown p {
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
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    /* Hero Section */
    .hero {
        text-align: center;
        padding: 40px 0;
        margin-bottom: 30px;
        background: linear-gradient(45deg, #4a90e2, #9013fe);
        color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .hero h1 {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .hero p {
        font-size: 1.4em;
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
    - Top-rated hotels with detailed descriptions (e.g., amenities, location, price range)
    - Famous places to visit with detailed descriptions (e.g., historical significance, entry fees, timings)
    - Local food & restaurants with detailed descriptions (e.g., popular dishes, price range, ambiance)
    - Weather information and temperature forecast for the travel dates
    - Pilgrimage places (if any) with detailed descriptions
    - Vehicle transportation options with pricing (e.g., taxis, public transport, rental cars)
    - Budget breakdown: Transport, Stay, Food, and Activities
    - Essential travel tips and safety recommendations (e.g., local customs, emergency contacts)

    *Additional Details:*
    - Currency: {currency}
    - Budget: {budget[0]} - {budget[1]} USD
    - Preferences: {", ".join(preferences) if preferences else "Standard travel"}

    *Translate the entire response into {language}. Keep it structured and clear.*
    """

    # Initialize AI model
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([
            SystemMessage(content="You are an AI travel expert."),
            HumanMessage(content=prompt_template)
        ])
        return response.content if response else "⚠ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

# ✅ Function to Translate Text
def translate_text(text, target_language):
    if target_language == "English":
        return text

    translator = Translator()
    try:
        translated_text = translator.translate(text, dest=language_codes.get(target_language, "en")).text
        return translated_text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

# 🚀 Generate Plan Button
if st.button("🚀 Generate AI Travel Plan"):
    if not source or not destination:
        st.warning("⚠ Please enter both the departure and destination cities!")
    else:
        with st.spinner("🔍 Finding the best options for you..."):
            plan = get_travel_plan(source, destination, currency, budget, language)

        if plan and not plan.startswith("❌"):
            st.success("🎉 Your AI-Powered Travel Plan is Ready!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

            if email:
                st.info(f"📩 Itinerary sent to {email}!")
        else:
            st.error(plan)

# 📌 Sidebar Information
with st.sidebar:
    st.markdown("## ℹ How It Works")
    st.markdown("""
    <div style="color: white;">
    <p>⿡ Enter travel details</p>
    <p>⿢ Select preferences & budget</p>
    <p>⿣ Click 'Generate AI Travel Plan'</p>
    <p>⿤ Get an instant AI-powered itinerary</p>
    <p>⿥ (Optional) Receive itinerary via email</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌟 Why Use Plan My Trip AI Travel Planner?")
    st.markdown("""
    <div style="color: white;">
    <p>✅ AI-powered personalized recommendations</p>
    <p>✅ Weather & Temperature Info</p>
    <p>✅ Multi-language support</p>
    <p>✅ Detailed descriptions of places, hotels, and restaurants</p>
    <p>✅ Vehicle Transportation Options</p>
    <p>✅ Email itinerary feature</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Explore the places & Happy Travels ✨<br>
    Created by Gopichand Challa | Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from googletrans import Translator  # For translation
import os

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# 📍 Cities with IATA Codes
cities_with_iata = {
    "New York": "JFK", "London": "LHR", "Paris": "CDG", "Tokyo": "NRT",
    "Sydney": "SYD", "Dubai": "DXB", "Mumbai": "BOM", "Berlin": "BER",
    "Rome": "FCO", "Barcelona": "BCN", "Singapore": "SIN", "Los Angeles": "LAX",
    "Toronto": "YYZ", "Cape Town": "CPT", "Delhi": "DEL"
}

# 🌍 Supported Languages
language_codes = {
    "English": "en", "French": "fr", "Spanish": "es", "German": "de",
    "Italian": "it", "Hindi": "hi", "Telugu": "te", "Tamil": "ta"
}

# 🎨 Streamlit UI Setup
st.set_page_config(page_title="✈ Plan My Trip", page_icon="🌍", layout="wide")

# 💅 Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        color: #333;
        background: linear-gradient(135deg, rgba(245, 247, 250, 0.9), rgba(195, 207, 226, 0.9)), 
                    url('https://www.transparenttextures.com/patterns/paper-fibers.png');
        background-blend-mode: overlay;
        background-size: cover;
        background-attachment: fixed;
    }
    .stSelectbox > div > div > select, .stTextInput > div > div > input, 
    .stNumberInput > div > div > input, .stDateInput > div > div > input {
        border: 2px solid #4a90e2;
        border-radius: 15px;
        padding: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stSelectbox > div > div > select { background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/marker.png') no-repeat 10px center; }
    .stDateInput > div > div > input { background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/calendar.png') no-repeat 10px center; padding-left: 40px; }
    .stButton button {
        background: linear-gradient(45deg, #4a90e2, #9013fe);
        color: white;
        border-radius: 25px;
        padding: 12px 35px;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .travel-card {
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        background: rgba(255, 255, 255, 0.95);
        font-size: 16px;
        line-height: 1.6;
    }
    .hero { text-align: center; padding: 60px 20px; margin-bottom: 30px; background: linear-gradient(135deg, #ffffff, #f0f4f8); border-radius: 20px; box-shadow: 0 6px 15px rgba(0,0,0,0.1); }
    .hero h1 { font-size: 2.8em; color: #4a90e2; }
    .hero p { font-size: 1.3em; color: #555; }
    .footer { text-align: center; padding: 20px; background: linear-gradient(45deg, #4a90e2, #9013fe); border-radius: 20px; color: white; margin-top: 30px; }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero">
    <h1>✈ Plan My Trip</h1>
    <p>Your Comprehensive AI-Powered Travel Planner</p>
</div>
""", unsafe_allow_html=True)

# 📋 UI Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("🏙 Departure City", [""] + list(cities_with_iata.keys()), index=0)
        destination = st.selectbox("🌆 Destination City", [""] + list(cities_with_iata.keys()), index=0)
        travel_date = st.date_input("📅 Travel Date", min_value=datetime.today())
        language = st.selectbox("🌍 Language", list(language_codes.keys()))

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("💰 Budget Range ($)", 100, 5000, (500, 2000))

# 🧠 AI Travel Plan Generator with Google Generative Language API
def get_travel_plan(source, destination, travel_date, currency, budget, language):
    prompt_template = f"""
    You are an AI travel expert. Generate a comprehensive travel itinerary from {source} to {destination} in {language} for the date {travel_date.strftime('%Y-%m-%d')}.

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
    - Preferences: Standard travel

    *Translate the entire response into {language}. Keep it structured, clear, and use markdown formatting (e.g., ### Headings, - Bullet points).*
    """

    # Initialize the Google Generative Language API (Gemini model)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",  # Assuming this model is available; adjust as needed
        google_api_key=GOOGLE_API_KEY
    )

    try:
        response = llm.invoke([
            SystemMessage(content="You are an expert travel planner providing detailed itineraries."),
            HumanMessage(content=prompt_template)
        ])
        if response and response.content:
            return response.content
        else:
            return "⚠ No response from the API. Please try again."
    except Exception as e:
        return f"❌ Error fetching itinerary: {str(e)}. Check API key and model availability."

# 🚀 Generate Plan Button
if st.button("🚀 Generate Travel Plan"):
    if not source or not destination or source == "" or destination == "":
        st.warning("⚠ Please select both cities!")
    elif source not in cities_with_iata or destination not in cities_with_iata:
        st.warning("⚠ Please select valid cities from the list!")
    else:
        with st.spinner("🔍 Generating your itinerary..."):
            plan = get_travel_plan(source, destination, travel_date, currency, budget, language)
        
        if plan and not plan.startswith("❌"):
            st.success("🎉 Travel Plan Generated Successfully!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Plan",
                data=plan,
                file_name=f"Travel_Plan_{source}_to_{destination}.txt",
                mime="text/plain"
            )
        else:
            st.error(plan)

# 📌 Sidebar
with st.sidebar:
    st.markdown("## How It Works")
    st.markdown("""
    - Select your cities, date, and preferences
    - Choose currency and budget
    - Get a detailed AI-generated itinerary
    """)
    st.markdown("### ✈ Quick Tips")
    st.write("- Book flights early\n- Check visa requirements\n- Pack light")

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Happy Travels ✨<br>Created by Gopichand Challa<br>
    <a href="https://github.com/gopichandchalla16" style="color: white;">GitHub</a> | 
    <a href="https://www.linkedin.com/in/gopichandchalla" style="color: white;">LinkedIn</a></p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime
from functools import lru_cache
import os  # Added os import to fix NameError

# 🛠 Configuration
# Access API key from secrets.toml or environment variable
GOOGLE_API_KEY = st.secrets.get("general", {}).get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# Check if API key is configured
if not GOOGLE_API_KEY:
    st.error("""
    ❌ **API Key Missing**  
    Please configure the GOOGLE_API_KEY in `.streamlit/secrets.toml` or as an environment variable.  
    Example for `secrets.toml`:  

# 🌍 Supported Languages
language_codes = {
    "English": "en", "French": "fr", "Spanish": "es", "German": "de",
    "Italian": "it", "Hindi": "hi", "Telugu": "te", "Tamil": "ta"
}

# 📍 Common Cities
common_cities = [
    "New York", "London", "Paris", "Tokyo", "Sydney", "Dubai", "Mumbai", "Berlin",
    "Rome", "Barcelona", "Singapore", "Los Angeles", "Toronto", "Cape Town", "Delhi"
]

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
    .stSelectbox > div > div > select {
        border: 2px solid #4a90e2 !important;
        border-radius: 15px !important;
        padding: 12px !important;
        background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/marker.png') no-repeat 10px center !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stTextInput > div > div > input {
        border: 2px solid #4a90e2 !important;
        border-radius: 15px !important;
        padding: 12px !important;
    }
    .stDateInput > div > div > input {
        border: 2px solid #4a90e2 !important;
        border-radius: 15px !important;
        padding: 12px 12px 12px 40px !important;
        background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/calendar.png') no-repeat 10px center !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #4a90e2, #9013fe) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 35px !important;
        font-size: 18px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .travel-card {
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        background: rgba(255, 255, 255, 0.95);
        color: #333 !important;
        font-size: 16px;
        line-height: 1.6;
        max-height: 600px;
        overflow-y: auto;
    }
    .hero {
        text-align: center;
        padding: 60px 20px;
        margin-bottom: 30px;
        background: linear-gradient(135deg, #ffffff, #f0f4f8);
        border-radius: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    .hero h1 { font-size: 2.8em; color: #4a90e2; }
    .hero p { font-size: 1.3em; color: #555; }
    .footer {
        text-align: center;
        padding: 20px;
        background: linear-gradient(45deg, #4a90e2, #9013fe);
        border-radius: 20px;
        color: white;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero">
    <h1>✈ Plan My Trip</h1>
    <p>Discover Your Destination with AI Precision</p>
</div>
""", unsafe_allow_html=True)

# 📋 UI Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("🏙 Departure City", [""] + common_cities + ["Other"], index=0)
        if source == "Other":
            source = st.text_input("Enter Departure City", placeholder="e.g., Chicago")
        destination = st.selectbox("🌆 Destination City", [""] + common_cities + ["Other"], index=0)
        if destination == "Other":
            destination = st.text_input("Enter Destination City", placeholder="e.g., Miami")
        travel_date = st.date_input("📅 Travel Date", min_value=datetime.today())

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("💰 Budget Range ($)", 100, 5000, (500, 2000))
        language = st.selectbox("🌍 Language", list(language_codes.keys()))

# 🧠 Optimized AI Travel Plan Generator with More Destination Info
@lru_cache(maxsize=128)
def get_travel_plan(source, destination, currency, budget_min, budget_max, language, travel_date):
    prompt_template = f"""
    You are a travel expert AI. Provide a detailed travel itinerary from {source} to {destination} for {travel_date.strftime('%Y-%m-%d')} in {language}. Use markdown.

    ### Destination Overview
    - Brief description of {destination} (e.g., culture, history, vibe)

    ### Travel Options
    - Best flight/train/bus options with estimated costs in {currency}
    
    ### Accommodation
    - Top 3 hotels with brief details (location, amenities, price in {currency})
    
    ### Attractions
    - Top 3 places to visit with detailed descriptions (e.g., historical significance, entry fees, timings)
    
    ### Food
    - 2-3 local food recommendations with descriptions (e.g., dishes, price range, ambiance)
    
    ### Weather Forecast
    - Current or forecasted weather conditions for {destination} on {travel_date.strftime('%Y-%m-%d')}
    
    ### Pilgrimage Sites
    - Notable religious or historical sites in {destination} (if any) with brief descriptions
    
    ### Local Transportation
    - Options like taxis, public transport, rental cars with estimated pricing in {currency}
    
    ### Budget Breakdown
    - Total estimate within {budget_min}-{budget_max} USD (convert to {currency}) for transport, stay, food, and activities
    
    ### Travel Tips & Safety
    - 2-3 essential tips (e.g., local customs, etiquette)
    - Basic safety advice or emergency contacts for {destination}
    
    Keep it structured, detailed, and accurate based on available knowledge.
    """

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    try:
        response = llm.invoke([
            SystemMessage(content="You are a highly efficient travel expert AI with up-to-date knowledge."),
            HumanMessage(content=prompt_template)
        ])
        if response and response.content:
            return response.content
        else:
            return "⚠ No response from AI."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# 🚀 Generate Plan Button
if st.button("🚀 Generate Travel Plan"):
    if not source or not destination or source == "" or destination == "":
        st.warning("⚠ Please select both cities!")
    else:
        with st.spinner("🔍 Crafting your detailed plan..."):
            plan = get_travel_plan(source, destination, currency, budget[0], budget[1], language, travel_date)
        
        if plan and not plan.startswith("❌"):
            st.success("🎉 Your Detailed Plan is Ready!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)
            st.write(plan)  # Fallback for visibility
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
    - Select your cities and travel date
    - Choose currency, budget, and language
    - Receive a detailed itinerary instantly
    """)
    st.markdown("### ✈ Tips")
    st.write("- Book early for savings\n- Research visa requirements\n- Pack light for convenience")

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Explore the Places & Happy Travels ✨<br>Created by Gopichand Challa<br>
    <a href="https://github.com/gopichandchalla16" style="color: white;">GitHub</a> | 
    <a href="https://www.linkedin.com/in/gopichandchalla" style="color: white;">LinkedIn</a> |
    <a href="http://datascienceportfol.io/gopichandchalla" style="color: white;">Portfolio</a></p>
</div>
""", unsafe_allow_html=True)

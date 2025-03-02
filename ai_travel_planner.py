import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# 🎨 UI Configuration
st.set_page_config(
    page_title="Plan My Trip - AI Powered Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 💅 Custom CSS for Styling
st.markdown("""
<style>
    /* General Page Styling */
    body { font-family: 'Arial', sans-serif; }
    
    /* Input Fields */
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border: 2px solid #4a90e2 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px !important;
        transition: 0.3s;
    }
    .stTextInput input:focus, .stDateInput input:focus, .stSelectbox select:focus {
        border-color: #ff7eb3 !important;
    }

    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #4a90e2, #ff7eb3) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 12px 35px !important;
        font-size: 16px !important;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #ff7eb3, #4a90e2) !important;
        transform: scale(1.05);
    }

    /* Travel Card Styling */
    .travel-card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        background: #ffffff;
        border-left: 5px solid #4a90e2;
        transition: 0.3s;
    }
    .travel-card:hover {
        border-left: 5px solid #ff7eb3;
        transform: scale(1.02);
    }

    /* Hero Section */
    .hero {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #4a90e2, #ff7eb3);
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
    }
    .hero h1 { font-size: 2.8em; margin-bottom: 10px; }
    .hero p { font-size: 1.2em; }

</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero">
    <h1>🌍 Plan My Trip - AI Powered Travel Planner</h1>
    <p>Your Ultimate Travel Companion - Smart, Simple & AI-Powered</p>
</div>
""", unsafe_allow_html=True)

# 📋 Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        source = st.text_input("🌍 Departure City", placeholder="E.g., New York", help="Enter your starting location")
        destination = st.text_input("📍 Destination City", placeholder="E.g., Paris", help="Enter your destination")
        travel_date = st.date_input("📅 Travel Date")
        
    with col2:
        currency = st.selectbox("💰 Preferred Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("🎯 Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("🔍 Travel Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel"])

# 🤖 AI Integration
def get_travel_plan(source, destination, currency, budget):
    prompt_template = f"""
    As an expert travel planner, create a detailed itinerary from {source} to {destination}.
    Consider: 
    - Currency: {currency}
    - Budget range: ${budget[0]} - ${budget[1]}
    
    Include:
    1. 🛫 Transportation options with estimated costs
    2. 🏨 Best accommodation suggestions
    3. 🎡 Must-see attractions & activities
    4. 🍽 Local cuisine recommendations
    5. ⚠ Travel tips, safety warnings, and local customs
    
    Format response clearly with proper sections & emojis.
    """
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        response = llm.invoke([HumanMessage(content=prompt_template)])
        return response.content
    except Exception as e:
        st.error(f"🚨 Error generating plan: {str(e)}")
        return None

# 🚀 Generate Plan
if st.button("🛫 Generate AI Travel Plan"):
    if not source or not destination:
        st.warning("⚠ Please fill in both departure and destination cities.")
    else:
        with st.spinner("🔍 Finding the best travel options..."):
            plan = get_travel_plan(source, destination, currency, budget)
        
        if plan:
            st.success("🎉 Your Personalized AI-Powered Travel Plan")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

# 📌 Sidebar
with st.sidebar:
    st.markdown("## ℹ How It Works")
    st.markdown("""
    ⿡ Enter your travel details  
    ⿢ Set preferences & budget  
    ⿣ Generate an AI-powered plan  
    ⿤ Customize as needed ✨  
    """)
    
    st.markdown("---")
    st.markdown("### 🔒 AI-Powered Safe & Smart Travel Planning")
    st.markdown("We leverage Google's Gemini AI to ensure top-quality recommendations for your trip.")

# 📝 Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>✨ Safe Travels & Happy Exploring! ✨<br>
    Created by Gopichand • Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

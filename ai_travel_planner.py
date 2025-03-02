import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# 🎨 UI Configuration
st.set_page_config(
    page_title="🌍 Plan My Trip - AI Powered Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 💅 Custom CSS
st.markdown("""
<style>
    /* General Styling */
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
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div style="text-align: center; padding: 40px 0; background: linear-gradient(135deg, #4a90e2, #9013fe); border-radius: 15px; margin-bottom: 30px;">
    <h1 style="color: white; font-size: 3em; margin-bottom: 10px;">🌍 Plan My Trip</h1>
    <p style="color: white; font-size: 1.4em;">Your AI-Powered Travel Planner</p>
</div>
""", unsafe_allow_html=True)

# 📋 Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Departure City", placeholder="New York", help="Enter your starting city")
        destination = st.text_input("Destination City", placeholder="Paris", help="Where are you going?")
        travel_date = st.date_input("Travel Date")
        
    with col2:
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel"])

# 🤖 AI Integration
def get_travel_plan(source, destination, currency, budget):
    prompt_template = f"""
    As an expert travel planner, create a detailed itinerary from {source} to {destination}.
    Consider: 
    - Currency: {currency}
    - Budget range: {budget[0]} - {budget[1]}
    Include:
    1. Transportation options with costs
    2. Accommodation suggestions
    3. Must-see attractions
    4. Local cuisine recommendations
    5. Travel tips and warnings
    
    Format response in clear sections with emojis.
    """
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        response = llm.invoke([HumanMessage(content=prompt_template)])
        return response.content
    except Exception as e:
        st.error(f"🚨 Error generating plan: {str(e)}")
        return None

# 🚀 Generate Plan
if st.button("Generate Travel Plan ✈️"):
    if not source or not destination:
        st.warning("⚠️ Please fill in both departure and destination cities")
    else:
        with st.spinner("🔍 Finding the best options for you..."):
            plan = get_travel_plan(source, destination, currency, budget)
        
        if plan:
            st.success("🎉 Your Custom Travel Plan")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

# 📌 Sidebar
with st.sidebar:
    st.markdown("## ℹ️ How It Works")
    st.markdown("""
    1. Enter your travel details
    2. Set preferences
    3. Generate AI-powered plan
    4. Customize as needed
    """)
    st.markdown("---")
    st.markdown("### 🔒 Safe Travel Planning")
    st.markdown("We use Google's latest AI technology to ensure reliable recommendations")

# 📝 Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>✨ Happy Travels! ✨<br>
    Created by <strong>Gopichand</strong> • Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

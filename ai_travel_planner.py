import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# 🎨 UI Configuration
st.set_page_config(
    page_title="✈ Plan My Trip - AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 💅 Custom CSS
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f8f9fa;
    }
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border: 2px solid #1E88E5 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #1E88E5, #673AB7) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        width: 100%;
        font-size: 1.1em;
        transition: 0.3s;
    }
    .stButton button:hover {
        transform: scale(1.05);
    }
    .hero-section {
        text-align: center;
        padding: 40px 0;
        background: linear-gradient(135deg, #1E88E5, #673AB7);
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
    }
    .travel-card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        background: white;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero-section">
    <h1>🌍 Plan My Trip - AI Powered Travel Planner</h1>
    <p>Smart, Personalized & Effortless Travel Planning</p>
</div>
""", unsafe_allow_html=True)

# 📋 Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        source = st.text_input("🏙 Departure City", placeholder="New York", help="Enter your starting city")
        destination = st.text_input("🌆 Destination City", placeholder="Paris", help="Where are you traveling?")
        travel_date = st.date_input("📅 Travel Date")
        language = st.selectbox("🌍 Language", ["English", "French", "Spanish", "German", "Italian", "Hindi", "Telugu", "Tamil"])

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("💰 Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("🎯 Travel Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel", "Adventure"])
        email = st.text_input("📧 Receive Itinerary via Email (Optional)", placeholder="you@example.com")

# 🤖 AI Travel Plan Generator
def get_travel_plan(source, destination, currency, budget, language):
    prompt_template = f"""
    You are an expert AI travel planner. Generate a highly detailed travel itinerary for a trip from {source} to {destination} in {language}.
    
    *Include:*
    ⿡ Best flight/train/bus options with estimated costs.  
    ⿢ Top-rated hotels in the budget with Google Maps links.  
    ⿣ Must-see attractions with Google Maps links.  
    ⿤ Local food & restaurants with Google Maps links.  
    ⿥ Budget breakdown: Transport, Stay, Food, and Activities.  
    ⿦ Essential travel tips & safety recommendations.  

    *Consider:*
    - Currency: {currency}
    - Budget: {budget[0]} - {budget[1]} USD
    - Preferences: {", ".join(preferences) if preferences else "Standard travel recommendations"}

    Keep the response structured with clear headings and use emojis where relevant.
    """

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        response = llm.invoke([HumanMessage(content=prompt_template)])
        return response.content
    except Exception as e:
        st.error(f"🚨 Error generating plan: {str(e)}")
        return None

# 🚀 Generate Plan Button
if st.button("🚀 Generate AI Travel Plan"):
    if not source or not destination:
        st.warning("⚠ Please enter both the departure and destination cities!")
    else:
        with st.spinner("🔍 Finding the best options for you..."):
            plan = get_travel_plan(source, destination, currency, budget, language)

        if plan:
            st.success("🎉 Your AI-Powered Travel Plan is Ready!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)
            
            # ✉ Send itinerary via email (Mock-up)
            if email:
                st.info(f"📩 Itinerary sent to {email}!")

# 📌 Sidebar Features
with st.sidebar:
    st.markdown("## ℹ How It Works")
    st.markdown("""
    ⿡ Enter your travel details  
    ⿢ Select preferences & budget  
    ⿣ Click 'Generate AI Travel Plan'  
    ⿤ Get a personalized trip itinerary  
    ⿥ (Optional) Receive itinerary via email  
    """)
    
    st.markdown("---")
    
    st.markdown("### 🌟 Why Use Plan My Trip?")
    st.markdown("""
    ✅ AI-powered recommendations  
    ✅ Budget-friendly travel planning  
    ✅ Multi-language support  
    ✅ Google Maps integration for easy navigation  
    ✅ Email itinerary feature  
    """)

    st.markdown("---")

    st.markdown("### 🔒 Safe & Reliable")
    st.markdown("Our AI is powered by Google's latest technology to provide the best and most accurate travel recommendations.")

# 📝 Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>✨ Happy Travels! ✨<br>
    Created by Gopichand Challa • Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

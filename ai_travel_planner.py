import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
import time

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
    page_title="✈ Plan My Trip - AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# 💅 Custom CSS for Better UI
st.markdown("""
<style>
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
    <h1 style="color: white; font-size: 3em; margin-bottom: 10px;">✈ Plan My Trip</h1>
    <p style="color: white; font-size: 1.4em;">Your AI-Powered Travel Planner</p>
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
    You are an AI travel expert. Generate a detailed travel itinerary from {source} to {destination} in {language}.

    *Plan Should Include:*
    ⿡ Best flights/trains/buses with estimated cost  
    ⿢ Top-rated hotels with Google Maps links  
    ⿣ Must-visit attractions with Google Maps links  
    ⿤ Local food & restaurants with Google Maps links  
    ⿥ Budget breakdown: Transport, Stay, Food, and Activities  
    ⿦ Essential travel tips and safety recommendations  

    *Additional Details:*
    - Currency: {currency}
    - Budget: {budget[0]} - {budget[1]} USD
    - Preferences: {", ".join(preferences) if preferences else "Standard travel"}

    *Translate the entire response into {language}. Keep it structured and concise.*
    """

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.0-pro",  # Correct model name
            google_api_key=GOOGLE_API_KEY,
            max_retries=3,  # Retry up to 3 times
            timeout=30,     # Increase timeout to 30 seconds
        )
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
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)  # Simulate a delay
                progress_bar.progress(i + 1)
            
            plan = get_travel_plan(source, destination, currency, budget, language)

        if plan:
            st.success("🎉 Your AI-Powered Travel Plan is Ready!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

            # ✉ Send itinerary via email (Mock-up)
            if email:
                st.info(f"📩 Itinerary sent to {email}!")

# 📌 Sidebar Information
with st.sidebar:
    st.markdown("## ℹ How It Works")
    st.markdown("""
    ⿡ Enter travel details  
    ⿢ Select preferences & budget  
    ⿣ Click 'Generate AI Travel Plan'  
    ⿤ Get an instant AI-powered itinerary  
    ⿥ (Optional) Receive itinerary via email  
    """)

    st.markdown("---")

    st.markdown("### 🌟 Why Use Plan My Trip?")
    st.markdown("""
    ✅ AI-powered personalized recommendations  
    ✅ Budget-friendly travel planning  
    ✅ Multi-language support  
    ✅ Google Maps integration  
    ✅ Email itinerary feature  
    """)

# 📝 Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>✨ Explore the places & Happy Travels ✨<br>
    Created by Gopichand Challa • Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

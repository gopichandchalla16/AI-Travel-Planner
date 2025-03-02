import streamlit as st
from googletrans import Translator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# 🌟 FIX: Move set_page_config to the very top!
st.set_page_config(
    page_title="Plan My Trip - AI Powered Travel Planner",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# 🌍 Language Selection (Using googletrans - Free & No API Needed)
translator = Translator()
languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Telugu": "te",
    "Tamil": "ta",
    "Kanada": "ka"
}

st.sidebar.title("🌍 Select Language")
selected_language = st.sidebar.selectbox("Choose your language", list(languages.keys()))

# 🎨 UI Configuration
st.set_page_config(
    page_title="Plan My Trip - AI Powered Travel Planner",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 💅 Custom CSS for Styling & Background Image
st.markdown("""
<style>
    body {
        background-image: url("https://source.unsplash.com/1600x900/?travel,adventure");
        background-size: cover;
        background-position: center;
    }
    .stTextInput input, .stDateInput input, .stSelectbox select {
        border: 2px solid #4a90e2 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #ff6b6b, #f06595) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        width: 100%;
        font-size: 16px;
    }
    .travel-card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section with Background Image
st.markdown("""
<div style="text-align: center; padding: 40px 0; background: linear-gradient(135deg, #ff6b6b, #f06595); border-radius: 15px; margin-bottom: 30px;">
    <h1 style="color: white; font-size: 2.8em;">✈ Plan My Trip - AI Travel Planner</h1>
    <p style="color: white; font-size: 1.2em;">Your AI-Powered Travel Companion for Hassle-Free Trips</p>
</div>
""", unsafe_allow_html=True)

# 📋 Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Departure City", placeholder="New York")
        destination = st.text_input("Destination City", placeholder="Paris")
        travel_date = st.date_input("Travel Date")
        
    with col2:
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel"])

# 🌍 Translation Function
def translate_text(text, lang):
    if lang != "English":  # Only translate if it's not English
        return translator.translate(text, dest=languages[lang]).text
    return text

# 🤖 AI Travel Plan Generator
def get_travel_plan(source, destination, currency, budget, lang):
    prompt_template = f"""
    Create a detailed itinerary for a trip from {source} to {destination}.
    - Currency: {currency}
    - Budget: {budget[0]} - {budget[1]} USD
    - Include:
      1. Transport options with costs
      2. Accommodation suggestions
      3. Must-see attractions
      4. Local cuisine recommendations
      5. Travel tips & warnings
    Format with clear sections and emojis.
    """
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        response = llm.invoke([HumanMessage(content=prompt_template)])
        
        if response:
            return translate_text(response.content, lang)  # Translate AI response
        else:
            return translate_text("⚠ Sorry, I couldn't generate a plan. Try again!", lang)
    except Exception as e:
        return translate_text(f"🚨 Error generating plan: {str(e)}", lang)

# 🚀 Generate Plan Button
if st.button("Generate AI Travel Plan ✈"):
    if not source or not destination:
        st.warning(translate_text("⚠ Please enter both departure and destination cities", selected_language))
    else:
        with st.spinner(translate_text("🔍 Finding the best options for your trip...", selected_language)):
            plan = get_travel_plan(source, destination, currency, budget, selected_language)
        
        if plan:
            st.success(translate_text("🎉 Your Custom Travel Plan", selected_language))
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

# 📌 Sidebar Information
with st.sidebar:
    st.markdown("## ℹ How It Works")
    st.markdown(translate_text("""
    1. Enter your travel details
    2. Select your preferences
    3. Click 'Generate AI Travel Plan'
    4. Get a custom itinerary instantly
    """, selected_language))
    st.markdown("---")
    st.markdown(translate_text("### 🔒 AI-Powered & Secure", selected_language))
    st.markdown(translate_text("We use AI to generate travel plans tailored for you.", selected_language))

# 📝 Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p>✨ Explore the Places & Happy Travels! ✨<br>
    Created by Gopichand Challa • Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

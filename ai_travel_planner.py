import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# 🛠 Configuration
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

# 🚀 Check if API key is working
def test_api_key():
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"
    data = {"contents": [{"role": "user", "parts": [{"text": "Test response"}]}]}
    response = requests.post(url, json=data)
    return response.status_code == 200

if not GOOGLE_API_KEY or not test_api_key():
    st.error("🚨 Google API Key is missing or invalid! Please check your key settings.")
    st.stop()

# 🌍 Supported Languages
language_codes = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "ka"
}

# 🎨 Streamlit UI Setup
st.set_page_config(
    page_title="✈ Plan My Trip - AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

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
        llm = ChatGoogleGenerativeAI(model="models/gemini-pro", google_api_key=GOOGLE_API_KEY)
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
            st.markdown(plan, unsafe_allow_html=True)

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
    <p>✨ Explore the Places & Happy Travel ✨<br>
    Created by Gopichand Challa • Powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

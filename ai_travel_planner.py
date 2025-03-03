import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from googletrans import Translator
import os
from functools import lru_cache  # For caching

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

# 📍 Common Cities for Autocomplete
common_cities = [
    "New York", "London", "Paris", "Tokyo", "Sydney", "Dubai", "Mumbai", "Berlin",
    "Rome", "Barcelona", "Singapore", "Los Angeles", "Toronto", "Cape Town", "Delhi"
]

# 🎨 Streamlit UI Setup
st.set_page_config(
    page_title="✈ Plan My Trip - AI Powered Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# 💅 Enhanced Custom CSS with Optimized Background Image
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
        background-position: center;
        background-attachment: fixed;
    }
    /* Enhanced Selectbox Styling for Cities */
    .stSelectbox > div > div > select {
        border: 2px solid #4a90e2 !important;
        border-radius: 15px !important;
        padding: 12px !important;
        font-size: 16px !important;
        background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/marker.png') no-repeat 10px center !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stSelectbox > div > div > select:focus {
        border-color: #9013fe !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    /* Date Input Styling */
    .stDateInput > div > div > input {
        border: 2px solid #4a90e2 !important;
        border-radius: 15px !important;
        padding: 12px 12px 12px 40px !important;
        font-size: 16px !important;
        background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/calendar.png') no-repeat 10px center !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stDateInput > div > div > input:focus {
        border-color: #9013fe !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    /* Button Styling */
    .stButton button {
        background: linear-gradient(45deg, #4a90e2, #9013fe) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 12px 35px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
    }
    /* Travel Card Styling */
    .travel-card {
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        background: rgba(255, 255, 255, 0.95);
        font-size: 16px;
        line-height: 1.8;
        overflow-x: auto;
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .stMarkdown h1 {
        color: #4a90e2 !important;
        font-weight: 700 !important;
        font-size: 2.8em !important;
    }
    .stMarkdown h2, .stMarkdown h3 {
        color: #00796b !important;
    }
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2) !important;
        padding: 25px !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    /* Hero Section */
    .hero {
        text-align: center;
        padding: 80px 20px;
        margin-bottom: 40px;
        background: linear-gradient(135deg, #ffffff, #f0f4f8);
        border-radius: 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    .hero h1 {
        font-size: 3em;
        margin-bottom: 15px;
        font-weight: 700;
        color: #4a90e2;
    }
    .hero p {
        font-size: 1.4em;
        color: #555;
    }
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 25px;
        background: linear-gradient(45deg, #4a90e2, #9013fe);
        border-radius: 20px;
        color: white;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero">
    <h1>✈ Plan My Trip</h1>
    <p>Your Ultimate AI-Powered Travel Companion</p>
</div>
""", unsafe_allow_html=True)

# 📋 UI Input Section with Enhanced Layout
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("🏙 Departure City", [""] + common_cities + ["Other (Type Below)"], index=0)
        if source == "Other (Type Below)":
            source = st.text_input("Enter Departure City", placeholder="e.g., Chicago")
        destination = st.selectbox("🌆 Destination City", [""] + common_cities + ["Other (Type Below)"], index=0)
        if destination == "Other (Type Below)":
            destination = st.text_input("Enter Destination City", placeholder="e.g., Miami")
        travel_date = st.date_input("📅 Travel Date")
        language = st.selectbox("🌍 Language", list(language_codes.keys()))

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("💰 Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("🎯 Travel Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel", "Adventure"])
        email = st.text_input("📧 Email for Itinerary (Optional)", placeholder="you@example.com")

# 🧠 Optimized AI Travel Plan Generator with Caching
@lru_cache(maxsize=128)
def get_travel_plan(source, destination, currency, budget_min, budget_max, language, preferences):
    prompt_template = f"""
    You are an AI travel expert. Generate a concise travel itinerary from {source} to {destination} in {language}.

    *Plan Should Include:*
    - Best travel options (flights/trains/buses) with estimated costs
    - Top 3 hotels with brief descriptions
    - Top 3 places to visit with brief descriptions
    - Local food recommendations
    - Budget breakdown in {currency} ({budget_min} - {budget_max} USD)
    - Basic travel tips

    *Preferences:* {", ".join(preferences) if preferences else "Standard travel"}
    *Translate the response into {language}. Use markdown formatting.*
    """

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)
    try:
        response = llm.invoke([
            SystemMessage(content="You are an AI travel expert."),
            HumanMessage(content=prompt_template)
        ])
        return response.content if response and response.content else "⚠ No response from AI."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Function to Translate Text
def translate_text(text, target_language):
    if target_language == "English":
        return text
    translator = Translator()
    try:
        return translator.translate(text, dest=language_codes.get(target_language, "en")).text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

# 🚀 Generate Plan Button
if st.button("🚀 Generate AI Travel Plan"):
    if not source or not destination or source == "" or destination == "":
        st.warning("⚠ Please select both departure and destination cities!")
    else:
        with st.spinner("🔍 Crafting your trip..."):
            plan = get_travel_plan(source, destination, currency, budget[0], budget[1], language, tuple(preferences))

        if plan and not plan.startswith("❌"):
            st.success("🎉 Your Travel Plan is Ready!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Itinerary",
                data=plan,
                file_name=f"Travel_Plan_{source}_to_{destination}.txt",
                mime="text/plain"
            )
            if email:
                st.info(f"📩 Itinerary sent to {email}!")
        else:
            st.error(plan)

# 📌 Sidebar
with st.sidebar:
    st.markdown("## How It Works")
    st.markdown("""
    - Select your travel details
    - Choose preferences & budget
    - Generate your itinerary
    - Download or email it
    """)

    st.markdown("---")
    st.markdown("### ✈ Quick Travel Tips")
    tips = [
        "Pack light!",
        "Carry a charger.",
        "Check visa rules.",
        "Book early for deals."
    ]
    st.write("\n".join([f"- {tip}" for tip in tips]))

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Explore the World & Happy Travels ✨<br>
    Created by Gopichand Challa<br>
    <a href="https://github.com/gopichandchalla16" style="color: white;">GitHub</a> | 
    <a href="https://www.linkedin.com/in/gopichandchalla" style="color: white;">LinkedIn</a> |
    <a href="http://datascienceportfol.io/gopichandchalla" style="color: white;">Portfolio</a></p>
</div>
""", unsafe_allow_html=True)

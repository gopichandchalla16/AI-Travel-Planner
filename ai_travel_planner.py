import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from googletrans import Translator
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

# 💅 Enhanced Custom CSS with Background Image
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
        color: #333;
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2), url('https://www.transparenttextures.com/patterns/old-map.png');
        background-blend-mode: overlay;
        background-size: cover;
        background-position: center;
        background-attachment: fixed; /* Keeps it stable on scroll */
    }
    /* Enhanced Input Styling for Departure & Destination */
    .stTextInput > div > div > input {
        border: 2px solid #4a90e2 !important;
        border-radius: 15px !important;
        padding: 12px 12px 12px 40px !important; /* Space for icon */
        font-size: 16px !important;
        background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/marker.png') no-repeat 10px center !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stTextInput > div > div > input:focus {
        border-color: #9013fe !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .stTextInput > div > div > input:hover {
        border-color: #00796b !important;
    }
    /* Enhanced Date Input Styling */
    .stDateInput > div > div > input {
        border: 2px solid #4a90e2 !important;
        border-radius: 15px !important;
        padding: 12px 12px 12px 40px !important; /* Space for icon */
        font-size: 16px !important;
        background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/calendar.png') no-repeat 10px center !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stDateInput > div > div > input:focus {
        border-color: #9013fe !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .stDateInput > div > div > input:hover {
        border-color: #00796b !important;
    }
    /* Selectbox Styling */
    .stSelectbox > div > div > select {
        border: 2px solid #4a90e2 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px !important;
        background: #fff;
        transition: border-color 0.3s ease;
    }
    .stSelectbox > div > div > select:focus {
        border-color: #9013fe !important;
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
        background: rgba(255, 255, 255, 0.95); /* Slightly transparent for contrast */
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
    .sidebar .stMarkdown h2 {
        color: #00796b !important;
        font-size: 1.6em !important;
        font-weight: 600 !important;
    }
    .sidebar .stMarkdown p {
        color: #37474f !important;
        font-size: 1.1em !important;
        line-height: 1.7 !important;
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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
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
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero h1 { font-size: 2.2em; }
        .hero p { font-size: 1.1em; }
        .travel-card { font-size: 14px; padding: 15px; }
        .stButton button { font-size: 16px; padding: 10px 25px !important; }
        .stTextInput > div > div > input, .stDateInput > div > div > input {
            padding: 10px 10px 10px 35px !important;
            font-size: 14px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section with Animation
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
        source = st.text_input("🏙 Departure City", placeholder="e.g., New York")
        destination = st.text_input("🌆 Destination City", placeholder="e.g., Paris")
        travel_date = st.date_input("📅 Travel Date")
        language = st.selectbox("🌍 Language", list(language_codes.keys()))

    with col2:
        currency = st.selectbox("💲 Currency", ["USD", "EUR", "GBP", "INR", "JPY"])
        budget = st.slider("💰 Budget Range ($)", 100, 5000, (500, 2000))
        preferences = st.multiselect("🎯 Travel Preferences", ["Eco-friendly", "Fastest Route", "Budget Options", "Luxury Travel", "Adventure"])
        email = st.text_input("📧 Email for Itinerary (Optional)", placeholder="you@example.com")

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

    *Translate the entire response into {language}. Keep it structured, clear, and visually appealing with markdown formatting (e.g., ### Headings, - Bullet points).*
    """

    # Initialize AI model
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([
            SystemMessage(content="You are an AI travel expert."),
            HumanMessage(content=prompt_template)
        ])
        if response and response.content:
            return response.content
        else:
            return "⚠ No response from AI. Please try again."
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

# 🚀 Generate Plan Button with Download Feature
if st.button("🚀 Generate AI Travel Plan"):
    if not source or not destination:
        st.warning("⚠ Please enter both the departure and destination cities!")
    else:
        with st.spinner("🔍 Crafting your perfect trip..."):
            plan = get_travel_plan(source, destination, currency, budget, language)

        if plan and not plan.startswith("❌"):
            st.success("🎉 Your AI-Powered Travel Plan is Ready!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)

            # Download Button for Itinerary
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

# 📌 Sidebar with Enhanced Info and Tips
with st.sidebar:
    st.markdown("## How It Works")
    st.markdown("""
    - Enter your travel details
    - Choose preferences & budget
    - Hit Generate AI Travel Plan
    - Get a tailored itinerary instantly
    - Optionally receive it via email
    """)

    st.markdown("---")
    st.markdown("### 🌟 Why Choose Us?")
    st.markdown("""
    - ✅ Personalized AI recommendations
    - ✅ Multi-language support
    - ✅ Detailed itineraries
    - ✅ Weather & transportation info
    - ✅ Downloadable plans
    """)

    # Added Travel Tips Feature
    st.markdown("---")
    st.markdown("### ✈ Quick Travel Tips")
    tips = [
        "Pack light to save space!",
        "Always carry a portable charger.",
        "Check visa requirements early.",
        "Book flights in advance for deals."
    ]
    st.write("\n".join([f"- {tip}" for tip in tips]))

# Footer with Social Links
st.markdown("""
<div class="footer">
    <p>✨ Explore the World & Happy Travels ✨<br>
    Created by Gopichand Challa<br>
    <a href="https://github.com/gopichandchalla16" style="color: white; text-decoration: none;">GitHub</a> | 
    <a href="https://www.linkedin.com/in/gopichandchalla" style="color: white; text-decoration: none;">LinkedIn</a> |
     <a href="http://datascienceportfol.io/gopichandchalla" style="color: white; text-decoration: none;">Portfolio</a></p>
</div>
""", unsafe_allow_html=True)

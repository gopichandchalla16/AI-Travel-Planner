import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set API key
API_KEY = os.getenv("GENAI_API_KEY")

# Custom Theme
st.set_page_config(
    page_title="Plan My Trip - AI Powered Travel Planner",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        padding: 10px;
    }
    .stMarkdown h1 {
        color: #4CAF50;
    }
    .stMarkdown h2 {
        color: #2E86C1;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Hero Section
st.image("https://via.placeholder.com/1200x400.png?text=Plan+My+Trip+-+AI+Powered+Travel+Planner", use_column_width=True)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Plan My Trip - AI Powered Travel Planner</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2E86C1;'>Your Personal Travel Assistant 🌍</h3>", unsafe_allow_html=True)

# User Inputs
st.markdown("---")
st.markdown("<h2 style='color: #4CAF50;'>Enter Your Travel Details</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    source = st.text_input("📍 Source:")
with col2:
    destination = st.text_input("📍 Destination:")

# Button to Generate Travel Plan
if st.button("🚀 Generate Travel Plan"):
    if source and destination:
        with st.spinner("🔍 Compiling all travel options...."):
            try:
                # Define the chat template
                chat_template = ChatPromptTemplate(messages=[
                    ("system", """You are an AI-Powered Travel Planner assistant that provides users with the best travel options based on their requirement.
                     Given source to destination, You must give the distance and provide information about best travel options like bike, cab, bus, train, and flight.
                     Each option should have the estimated cost, travel time, distance, and any relevant details like stops, traffic details.
                     You can also give some information about food: what are the food items best in between source and destination.
                     Convince while presenting the results in a clear, easy-to-read format."""),
                    ("human", "Find travel options from {source} to {destination} with estimated costs.")
                ])

                # Initialize the chat model
                chat_model = ChatGoogleGenerativeAI(api_key=API_KEY, model="gemini-pro")

                # Initialize the output parser
                parser = StrOutputParser()

                # Create the chain
                chain = chat_template | chat_model | parser

                # Invoke the chain with user inputs
                raw_input = {"source": source, "destination": destination}
                response = chain.invoke(raw_input)

                # Display the results in a card layout
                st.markdown("<h2 style='color: #4CAF50;'>✨ Travel Recommendations</h2>", unsafe_allow_html=True)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.write(response)
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter both source and destination.")

# Sidebar for Additional Features
st.sidebar.markdown("<h2 style='color: #4CAF50;'>🌟 Additional Features</h2>", unsafe_allow_html=True)
st.sidebar.write("Coming Soon:")
st.sidebar.write("- 🌤️ Weather Forecast")
st.sidebar.write("- 📸 Destination Images")
st.sidebar.write("- 💱 Currency Conversion")
st.sidebar.write("- 🗺️ Interactive Map")

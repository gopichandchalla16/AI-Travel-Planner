import streamlit as st
import requests
from datetime import datetime

# 🛠 Configuration
# For deployment, use secrets.toml; hardcoded here for testing
GOOGLE_API_KEY = "AIzaSyB12LqrvgCDH8zh2kwRSER-6KEw6PcLbaQ"  # Your API key

# 📍 Cities with IATA Codes
cities_with_iata = {
    "New York": "JFK", "London": "LHR", "Paris": "CDG", "Tokyo": "NRT",
    "Sydney": "SYD", "Dubai": "DXB", "Mumbai": "BOM", "Berlin": "BER",
    "Rome": "FCO", "Barcelona": "BCN", "Singapore": "SIN", "Los Angeles": "LAX",
    "Toronto": "YYZ", "Cape Town": "CPT", "Delhi": "DEL"
}

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
    .stSelectbox > div > div > select, .stTextInput > div > div > input, 
    .stNumberInput > div > div > input, .stDateInput > div > div > input {
        border: 2px solid #4a90e2;
        border-radius: 15px;
        padding: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stSelectbox > div > div > select { background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/marker.png') no-repeat 10px center; }
    .stDateInput > div > div > input { background: #fff url('https://img.icons8.com/ios-filled/20/4a90e2/calendar.png') no-repeat 10px center; padding-left: 40px; }
    .stButton button {
        background: linear-gradient(45deg, #4a90e2, #9013fe);
        color: white;
        border-radius: 25px;
        padding: 12px 35px;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .travel-card {
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        background: rgba(255, 255, 255, 0.95);
        font-size: 16px;
        line-height: 1.6;
    }
    .hero { text-align: center; padding: 60px 20px; margin-bottom: 30px; background: linear-gradient(135deg, #ffffff, #f0f4f8); border-radius: 20px; box-shadow: 0 6px 15px rgba(0,0,0,0.1); }
    .hero h1 { font-size: 2.8em; color: #4a90e2; }
    .hero p { font-size: 1.3em; color: #555; }
    .footer { text-align: center; padding: 20px; background: linear-gradient(45deg, #4a90e2, #9013fe); border-radius: 20px; color: white; margin-top: 30px; }
</style>
""", unsafe_allow_html=True)

# 🖼 Hero Section
st.markdown("""
<div class="hero">
    <h1>✈ Plan My Trip</h1>
    <p>Fast & Eco-Friendly Travel Insights</p>
</div>
""", unsafe_allow_html=True)

# 📋 UI Input Section
with st.expander("✈ Plan Your Trip", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("🏙 Departure City", [""] + list(cities_with_iata.keys()), index=0)
        destination = st.selectbox("🌆 Destination City", [""] + list(cities_with_iata.keys()), index=0)
        travel_date = st.date_input("📅 Travel Date", min_value=datetime.today())

    with col2:
        carrier = st.text_input("✈ Airline Code", "AA", help="e.g., AA (American Airlines), BA (British Airways)")
        flight_number = st.number_input("🔢 Flight Number", min_value=1, value=100, help="e.g., 100")

# 🧠 Fetch Travel Data with Travel Impact Model API
def get_travel_emissions(source, destination, travel_date, carrier, flight_number):
    url = f"https://travelimpactmodel.googleapis.com/v1/flights:computeFlightEmissions?key={GOOGLE_API_KEY}"
    payload = {
        "flights": [{
            "origin": cities_with_iata.get(source, ""),
            "destination": cities_with_iata.get(destination, ""),
            "operatingCarrierCode": carrier.upper(),  # Ensure uppercase for IATA codes
            "flightNumber": int(flight_number),       # Ensure integer
            "departureDate": {
                "year": travel_date.year,
                "month": travel_date.month,
                "day": travel_date.day
            }
        }]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "flightEmissions" in data and data["flightEmissions"]:
            emissions = data["flightEmissions"][0]["emissionsGramsPerPax"]["co2e"] / 1000  # Convert to kg
            plan = f"""
            ### Travel Plan: {source} to {destination}
            **Date:** {travel_date.strftime('%Y-%m-%d')}
            **Flight:** {carrier} {flight_number}

            #### Emissions Estimate
            - CO2e per passenger: {emissions:.2f} kg

            #### Quick Tips
            - Offset emissions with carbon credits.
            - Pack light to reduce fuel consumption.
            - Confirm flight details with the airline.
            """
            return plan
        else:
            return "⚠ No emissions data available. Verify flight number and airline code."
    except requests.Timeout:
        return "❌ Request timed out. Try again later."
    except requests.RequestException as e:
        error_msg = response.text if 'response' in locals() else str(e)
        return f"❌ Error: {error_msg}. Ensure API key is valid and flight exists."

# 🚀 Generate Plan Button
if st.button("🚀 Generate Travel Plan"):
    if not source or not destination or source == "" or destination == "":
        st.warning("⚠ Please select both cities!")
    elif source not in cities_with_iata or destination not in cities_with_iata:
        st.warning("⚠ Please select valid cities from the list!")
    elif not carrier or not flight_number:
        st.warning("⚠ Please enter a valid airline code and flight number!")
    else:
        with st.spinner("🔍 Calculating emissions..."):
            plan = get_travel_emissions(source, destination, travel_date, carrier, flight_number)
        
        if plan and not plan.startswith("❌"):
            st.success("🎉 Plan Generated Successfully!")
            st.markdown(f'<div class="travel-card">{plan}</div>', unsafe_allow_html=True)
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
    - Choose your cities and flight details
    - Get instant CO2e emissions data
    - Download your eco-friendly plan
    """)
    st.markdown("### ✈ Tips")
    st.write("- Use IATA codes (e.g., AA, BA)\n- Check flight schedules\n- Offset your carbon footprint")

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Happy Travels ✨<br>Created by Gopichand Challa<br>
    <a href="https://github.com/gopichandchalla16" style="color: white;">GitHub</a> | 
    <a href="https://www.linkedin.com/in/gopichandchalla" style="color: white;">LinkedIn</a></p>
</div>
""", unsafe_allow_html=True)

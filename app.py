import streamlit as st
import pickle
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)
st.markdown("""
    <style>
    /* Full-page animated gradient background */
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    body {
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a6c1ee);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    /* Glassmorphism card */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 30px;
        margin-top: 30px;
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #ff758c, #ff7eb3);
        color: white;
        border-radius: 12px;
        padding: 0.7em 1.5em;
        font-size: 1em;
        font-weight: bold;
        border: none;
        width: 100%;
        transition: transform 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
    }

    /* Result card */
    .result-card {
        background: linear-gradient(120deg, #89f7fe, #66a6ff);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        color: #003366;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        margin-top: 20px;
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# Load Model

with open("car_price_rf_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

# App Title

st.markdown("<h2 style='text-align:top center; color:white;'>🚗 Car Price Predictor</h2>", unsafe_allow_html=True)
st.markdown("<h4><p style='text-align:center; color:white;'>Enter your car details and get an instant price estimate</p></h4>", unsafe_allow_html=True)

with st.container():
    

    col1, col2 = st.columns(2)

    with col1:
        brand = st.selectbox("Brand", [
            "Maruti", "Hyundai", "Honda", "Toyota", "Ford",
            "Mahindra", "Tata", "Chevrolet", "Renault", "Volkswagen",
            "BMW", "Audi", "Mercedes-Benz", "Skoda", "Nissan",
            "Jeep", "Datsun", "Kia", "MG", "Fiat", "Mitsubishi", "Land Rover"
        ])
        fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
        owner = st.selectbox("Owner", [
            "First Owner", "Second Owner", "Third Owner",
            "Fourth & Above Owner", "Test Drive Car"
        ])

    with col2:
        year = st.number_input("Year", min_value=1990, max_value=datetime.now().year, value=2015)
        km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=1000000, value=30000)
        seller_type = st.selectbox("Seller Type", ["Dealer", "Individual", "Trustmark Dealer"])

    if st.button("Predict Price 💰"):
        # Feature engineering
        car_age = datetime.now().year - year
        km_driven_cap = min(km_driven, 500000)

        # Prepare input DataFrame
        input_df = pd.DataFrame([{
            "km_driven_cap": km_driven_cap,
            "car_age": car_age,
            "fuel": fuel,
            "seller_type": seller_type,
            "transmission": transmission,
            "owner": owner,
            "brand": brand
        }])

        # Predict
        prediction = model.predict(input_df)[0]

        st.markdown(f"<div class='result-card'>💰 Estimated Price: ₹{prediction:,.0f}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

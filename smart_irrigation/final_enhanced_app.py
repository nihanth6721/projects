
import streamlit as st
import numpy as np
import joblib
import requests
from streamlit_lottie import st_lottie

# Load model with error handling
try:
    model = joblib.load("Farm_Irrigation_System.pkl")
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'Farm_Irrigation_System.pkl' exists.")
    st.stop()

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_farm = load_lottieurl("https://lottie.host/407f0831-d8f6-4aa0-a4a0-47bd2f8eeeba/IcLfrAGBTn.json")

# App configuration
st.set_page_config(page_title="Smart Sprinkler System", layout="wide")

# Floating animated title using HTML/CSS
st.markdown("""
    <style>
    @keyframes float {
        0% { transform: translatey(0px); }
        50% { transform: translatey(-10px); }
        100% { transform: translatey(0px); }
    }
    .floating-title {
        font-size: 48px;
        color: #2ecc71;
        animation: float 2.5s ease-in-out infinite;
        font-weight: bold;
        text-align: center;
        margin-top: 0px;
    }
    </style>
    <div class="floating-title">🌿 Smart Sprinkler System</div>
""", unsafe_allow_html=True)

# Display Lottie animation
if lottie_farm:
    st_lottie(lottie_farm, speed=1, width=700, height=350, key="farm_lottie")

# Instructions
with st.expander("📘 How to Use"):
    st.markdown("""
    - Use the sliders to simulate 20 different sensor readings (values between 0.0 and 1.0).
    - Click on **Predict Sprinklers** to get ON/OFF status for each sprinkler (parcel).
    - Green = ON, Red = OFF.
    """)

# Sliders in 5 columns with 4 sliders each
sensor_values = []
cols = st.columns(5)
for i in range(20):
    with cols[i % 5]:
        val = st.slider(f"Sensor {i}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        sensor_values.append(val)

# Prediction
if st.button("🔍 Predict Sprinklers"):
    input_array = np.array(sensor_values).reshape(1, -1)
    try:
        prediction = model.predict(input_array)[0]
        st.success("Prediction Complete!")
        st.markdown("### 🚿 Sprinkler Status")
        status_cols = st.columns(4)
        for i, status in enumerate(prediction):
            with status_cols[i % 4]:
                color = "🟢 ON" if status == 1 else "🔴 OFF"
                st.markdown(f"**Sprinkler {i}**: {color}")
    except Exception as e:
        st.error(f"Prediction error: {e}")

# Footer
st.markdown("---")
st.caption("🚀 Developed by Team | ML Project Week 3 | Powered by Scikit-learn & Streamlit")

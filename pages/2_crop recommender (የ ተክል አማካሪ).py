import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
from auth import require_login
require_login()
# ---------------------------
# PATHS
# ---------------------------
MODEL_DIR = "models"
SCALER_PATH = os.path.join(MODEL_DIR, "scaler (3).pkl")
ENCODERS_PATH = os.path.join(MODEL_DIR, "label_encoders (3).pkl")

# Model paths
RF_MODEL_PATH = os.path.join(MODEL_DIR, "rfrr_model.pkl")
XGB_MODEL_PATH = os.path.join(MODEL_DIR, "xgbr_model.pkl")


# ---------------------------
# LOAD MODEL, SCALER, ENCODER
# ---------------------------
@st.cache_resource
def load_model(model_path):
    missing_files = [p for p in [model_path, SCALER_PATH, ENCODERS_PATH] if not os.path.exists(p)]
    if missing_files:
        st.error(f"❌ Missing files: {', '.join(os.path.basename(f) for f in missing_files)}")
        return None, None, None

    try:
        model = joblib.load(model_path)
        scaler = joblib.load(SCALER_PATH)
        encoders = joblib.load(ENCODERS_PATH)
        return model, scaler, encoders
    except Exception as e:
        st.error(f"❌ Error loading model files: {e}")
        return None, None, None


# ---------------------------
# APP UI
# ---------------------------
st.title("🌾 Crop Recommendation System")

tab1, tab2 = st.tabs(["RandomForestClassifier", "XGBClassifier"])

for tab, model_path, model_name in zip(
        [tab1, tab2],
        [RF_MODEL_PATH, XGB_MODEL_PATH],
        ["Random Forest", "XGB Classifier"]
):
    with tab:
        st.subheader(f"Using {model_name} model / አሁን የ {model_name}  ሞዴልን እየተጠቀሙ ነው።" )

        # Load model
        model, scaler, encoders = load_model(model_path)
        if model is None:
            st.stop()

        # ---------------------------
        # INPUTS (unique keys)
        # ---------------------------
        N = st.number_input("Nitrogen (N)", min_value=0, max_value=140, value=50, key=f"{model_name}_N")
        P = st.number_input("Phosphorus (P)", min_value=0, max_value=140, value=50, key=f"{model_name}_P")
        K = st.number_input("Potassium (K)", min_value=0, max_value=205, value=50, key=f"{model_name}_K")
        temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0,
                                      key=f"{model_name}_temp")
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0,
                                   key=f"{model_name}_humidity")
        ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, key=f"{model_name}_ph")
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=100.0,
                                   key=f"{model_name}_rainfall")

        # ---------------------------
        # PREDICTION
        # ---------------------------
        if st.button(f"Predict Crop ({model_name})"):
            input_data = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"])

            # Apply scaling if scaler exists
            try:
                input_scaled = scaler.transform(input_data)
            except:
                pass  # no scaler

            # Predict encoded class
            input_data= pd.DataFrame(input_scaled,columns=input_data.columns)
            prediction_encoded = model.predict(input_data)[0]

            # Decode to crop name
            crop_name = encoders["label"].inverse_transform([prediction_encoded])[0]

            st.success(f"✅ Recommended Crop: **{crop_name}**")

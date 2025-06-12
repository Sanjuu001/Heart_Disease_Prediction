import streamlit as st
import numpy as np
import pickle
from PIL import Image
import base64

# Load the trained model
with open("heart_disease_model.pkl", "rb") as file:
    model = pickle.load(file)

# Set page config
st.set_page_config(page_title="Heart Disease Predictor", layout="centered")


# to reduce the image capacity in the background
# background: linear-gradient(rgba(200,200,200,0.5), rgba(200,200,200,0.5)),


# to add the background image and also changeing the colour of the title and features
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://cdn.pixabay.com/photo/2024/01/05/22/02/ai-generated-8490212_1280.jpg");
        background-size: 50% 100%;
        background-position: center;
        background-repeat: repeat;
    }

    /* Title */
    .stApp h1 {
        color: white;
        text-shadow: 1px 1px 2px black;
    }

    /* Subtitle or markdown text */
    .stApp p {
        color: white;
        font-size: 18px;
        text-shadow: 1px 1px 1px black;
    }

    /* Form labels */
    label {
        color: white !important;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)



#  title and features
st.title(" Heart Disease Prediction")
st.markdown("Enter patient details to predict the risk of heart disease.")


with st.form("input_form"):
    age = st.text_input("Age", "")
    sex = st.selectbox("Sex", ["Select", "Male", "Female"])
    cp = st.selectbox("Chest Pain Type(cp)", ["Select", "0 - Typical Angina", "1 - Atypical Angina", "2 - Non-anginal Pain", "3 - Asymptomatic"])

    trestbps = st.selectbox("Resting Blood Pressure (trestbps)", ["Select"] + [str(i) for i in range(90, 201)])

    # thalach = st.text_input("Maximum Heart Rate Achieved (thalach)", "")

    thalach_placeholder = st.empty()

    exang = st.selectbox("Exercise Induced Angina(exang)", ["Select", "No (0)", "Yes (1)"])
    # oldpeak = st.text_input("ST depression (oldpeak)", "")
    
    oldpeak_placeholder = st.empty()

    slope = st.selectbox("Slope of the ST Segment(slope)", ["Select", "0 - Upsloping", "1 - Flat", "2 - Downsloping"])
    ca = st.selectbox("Major Vessels Colored by Fluoroscopy(ca)", ["Select", "0", "1", "2", "3", "4"])
    thal = st.selectbox("Thalassemia(thal)", ["Select", "0 - Normal", "1 - Fixed Defect", "2 - Reversible Defect"])

    submit = st.form_submit_button(" 🚀Predict")

    # ⬇️ Render these outside form so they're not required at submission
    thalach = thalach_placeholder.number_input("Maximum Heart Rate Achieved (thalach)", step=1, format="%d", key="thalach_input")
    oldpeak = oldpeak_placeholder.number_input("ST depression (oldpeak)",  step=0.1, format="%.1f", key="oldpeak_input")



if submit:
    if (
        not age or
        sex == "Select" or
        cp == "Select" or
        trestbps == "Select" or
        st.session_state.thalach_input == 0 or
        exang == "Select" or
        st.session_state.oldpeak_input == 0.0 or
        slope == "Select" or
        ca == "Select" or
        thal == "Select"
    ):
        st.warning("⚠️ Please fill out all fields correctly.")
    else:
        input_data = np.array([
            int(age),
            1 if sex == "Male" else 0,
            int(cp[0]),
            int(trestbps),
            st.session_state.thalach_input,
            1 if exang == "Yes (1)" else 0,
            st.session_state.oldpeak_input,
            int(slope[0]),
            int(ca),
            int(thal[0])
        ]).reshape(1, -1)

        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.markdown(
                f"""
                <div style='background-color: white; color: black; padding: 20px; border-radius: 10px;
                            box-shadow: 2px 2px 5px rgba(0,0,0,0.3); display: flex; align-items: center; gap: 15px;'>
                    <img src="data:image/png;base64,{base64.b64encode(open("sad.png", "rb").read()).decode()}" 
                         width="80" style="border-radius: 5px;" />
                    <div>
                        <strong>⚠️ High risk of heart disease!</strong><br>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='background-color: white; color: black; padding: 20px; border-radius: 10px;
                            box-shadow: 2px 2px 5px rgba(0,0,0,0.3); display: flex; align-items: center; gap: 15px;'>
                    <img src="data:image/png;base64,{base64.b64encode(open("happy.png", "rb").read()).decode()}" 
                         width="80" style="border-radius: 5px;" />
                    <div>
                        <strong>✅ Low risk of heart disease.</strong><br>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# Footer
st.sidebar.markdown("""
---
 **Any Queries**

📧 Contact: [sandeepkumardhoddi@gmail.com](mailto:sandeepkumardhoddi@gmail.com)
""")






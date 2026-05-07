import streamlit as st
import requests
import json


st.set_page_config(
    page_title="Personality Predictor",
    page_icon="🧠",
    layout="centered"
)


st.title("🧠 Personality Type Predictor")
st.markdown("""
This application predicts whether a person is an **Extrovert** or **Introvert** 
based on their behavioral patterns and social preferences.
""")


with st.form("prediction_form"):
    st.subheader("📊 Behavioral Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        time_alone = st.slider(
            "⏰ Time spent Alone (hours/day)",
            min_value=0.0,
            max_value=12.0,
            value=4.0,
            step=0.5
        )
        
        stage_fear = st.radio(
            "🎤 Stage Fear",
            options=["No", "Yes"],
            horizontal=True
        )
        
        social_attendance = st.slider(
            "🎉 Social Event Attendance (per month)",
            min_value=0.0,
            max_value=10.0,
            value=4.0,
            step=1.0
        )
        
        going_outside = st.slider(
            "🚶 Going Outside (days/week)",
            min_value=0.0,
            max_value=7.0,
            value=4.0,
            step=1.0
        )
    
    with col2:
        drained = st.radio(
            "😴 Drained after Socializing",
            options=["No", "Yes"],
            horizontal=True
        )
        
        friends_circle = st.slider(
            "👥 Friends Circle Size",
            min_value=0,
            max_value=20,
            value=8,
            step=1
        )
        
        post_frequency = st.slider(
            "📱 Post Frequency (per week)",
            min_value=0,
            max_value=10,
            value=5,
            step=1
        )
    
    st.markdown("---")
    
    
    submitted = st.form_submit_button("🔮 Predict Personality", type="primary")


API_URL = "http://localhost:8000/predict/"


if submitted:
    
    input_data = {
        "Time_spent_Alone": float(time_alone),
        "Stage_fear": stage_fear,
        "Social_event_attendance": float(social_attendance),
        "Going_outside": float(going_outside),
        "Drained_after_socializing": drained,
        "Friends_circle_size": float(friends_circle),
        "Post_frequency": float(post_frequency)
    }
    
    
    with st.spinner("Analyzing your responses..."):
        try:
            
            response = requests.post(API_URL, json=input_data)
            
            if response.status_code == 200:
                result = response.json()
                
                
                st.success("✅ Prediction Complete!")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    
                    personality = result['personality']
                    if personality == "Extrovert":
                        st.markdown(f"""
                        ## 🎉 {personality}
                        You enjoy social interactions and draw energy from being around others!
                        """)
                    else:
                        st.markdown(f"""
                        ## 🧘 {personality}
                        You prefer solitude and recharge by spending time alone!
                        """)
                    
                    
                    confidence = result['confidence'] * 100
                    st.markdown(f"**Confidence:** {confidence:.1f}%")
                    st.progress(confidence / 100)
                    
                   
                    st.markdown("### Probability Distribution")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Extrovert", f"{result['probabilities']['Extrovert']*100:.1f}%")
                    with col_b:
                        st.metric("Introvert", f"{result['probabilities']['Introvert']*100:.1f}%")
                    
                    
                    with st.expander("📋 View Your Input Data"):
                        st.json(input_data)
            else:
                st.error(f"API Error: {response.status_code}")
                st.json(response.json())
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Make sure the FastAPI server is running!")
            st.info("Start the server with: `uvicorn your_file:app --reload`")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


with st.sidebar:
    st.markdown("## ℹ️ About")
    st.markdown("""
    This model predicts personality type based on:
    - Time spent alone
    - Stage fear
    - Social event attendance
    - Going outside frequency
    - Feeling drained after socializing
    - Friends circle size
    - Social media post frequency
    
    **Model Accuracy:** ~93%
    """)
    
    st.markdown("---")
    st.markdown("### 🧪 Test Cases")
    
    if st.button("Load Extrovert Example"):
        st.session_state.test_data = {
            "Time_spent_Alone": 2.0,
            "Stage_fear": "No",
            "Social_event_attendance": 8.0,
            "Going_outside": 6.0,
            "Drained_after_socializing": "No",
            "Friends_circle_size": 14.0,
            "Post_frequency": 8.0
        }
        st.rerun()
    
    if st.button("Load Introvert Example"):
        st.session_state.test_data = {
            "Time_spent_Alone": 9.0,
            "Stage_fear": "Yes",
            "Social_event_attendance": 1.0,
            "Going_outside": 1.0,
            "Drained_after_socializing": "Yes",
            "Friends_circle_size": 2.0,
            "Post_frequency": 1.0
        }
        st.rerun()


if 'test_data' in st.session_state:
    st.toast("Test data loaded! Click 'Predict Personality' to see results.", icon="🧪")
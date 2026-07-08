import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the trained model
# Ensure 'gold_model.pkl' is in the same directory as app.py or provide the full path
try:
    with open('gold_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("Error: 'gold_model.pkl' not found. Please ensure the model file is in the correct directory.")
    st.stop()

st.title('📈 Gold Price Prediction App')
st.write('Predict the GLD (Gold) price based on various financial indicators.')

# Sidebar for user input
st.sidebar.header('Input Features')

def user_input_features():
    spx = st.sidebar.number_input('SPX (S&P 500 Index)', min_value=0.0, max_value=5000.0, value=1622.97, step=1.0)
    uso = st.sidebar.number_input('USO (United States Oil Fund)', min_value=0.0, max_value=200.0, value=31.79, step=0.1)
    slv = st.sidebar.number_input('SLV (iShares Silver Trust)', min_value=0.0, max_value=100.0, value=19.89, step=0.1)
    eur_usd = st.sidebar.number_input('EUR/USD (Euro to US Dollar Exchange Rate)', min_value=0.0, max_value=2.0, value=1.284, step=0.001, format="%.3f")
    
    # For date features, let's use current date as default or give a range
    st.sidebar.subheader('Date Features (for market context)')
    year = st.sidebar.number_input('Year', min_value=2000, max_value=2050, value=2018, step=1)
    month = st.sidebar.number_input('Month', min_value=1, max_value=12, value=5, step=1)
    day = st.sidebar.number_input('Day', min_value=1, max_value=31, value=16, step=1)
    
    # DayOfWeek is derived, but for a web app, users might expect to input a day or it's calculated
    # For simplicity, let's allow input or derive it if a full date input was used.
    # For this example, let's assume the user provides it or we calculate from year/month/day if needed
    # A more robust solution might use a st.date_input and calculate these
    day_of_week_options = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    selected_day_name = st.sidebar.selectbox('Day of Week', options=list(day_of_week_options.keys()), index=2) # Default to Wednesday
    day_of_week = day_of_week_options[selected_day_name]
    
    data = {
        'SPX': spx,
        'USO': uso,
        'SLV': slv,
        'EUR/USD': eur_usd,
        'Year': year,
        'Month': month,
        'Day': day,
        'DayOfWeek': day_of_week
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

st.subheader('User Input Parameters')
st.write(input_df)

# Prediction button
if st.button('Predict GLD Price'):
    # Make prediction
    predicted_gld = model.predict(input_df)[0]
    
    st.subheader('Prediction')
    st.success(f'The Predicted GLD Price is: ${predicted_gld:.2f} USD')

# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10o3FLlDLn7kmpjBAojEyGyt5t6zRX-Ln
"""

!pip install streamlit

import streamlit as st

import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Load model
with open('model.pkl', 'rb') as file:
    models = pickle.load(file)

# UI Input
st.title('Prediksi Kepuasan Pelanggan')
st.write('Masukkan fitur-fitur berikut untuk memprediksi kepuasan pelanggan.')

age = st.number_input('Umur', min_value=18, max_value=100, value=25)
gender = st.selectbox('Jenis Kelamin', options=['Pria', 'Wanita'])
income = st.number_input('Pendapatan Tahunan (dalam ribuan)', min_value=10, max_value=1000, value=50)
spending_score = st.number_input('Skor Pengeluaran (1-100)', min_value=1, max_value=100, value=50)
model_choice = st.selectbox('Pilih Model', options=['Logistic Regression', 'Decision Tree', 'K-Nearest Neighbors', 'Random Forest'])

# Preprocess input
input_data = pd.DataFrame({
    'Age': [age],
    'Gender': [gender],
    'Annual Income (k$)': [income],
    'Spending Score (1-100)': [spending_score]
})

# One-hot encoding
encoder = OneHotEncoder(drop='first', sparse_output=False)  # Update parameter di sini
encoded_gender = encoder.fit_transform(input_data[['Gender']])
encoded_gender_df = pd.DataFrame(encoded_gender, columns=encoder.get_feature_names_out(['Gender']))
input_data = input_data.drop('Gender', axis=1)
input_data = pd.concat([input_data, encoded_gender_df], axis=1)

# Scaling
scaler = StandardScaler()
input_data = scaler.fit_transform(input_data)

# Predict
if model_choice == 'Logistic Regression':
    model = models['log_reg']
elif model_choice == 'Decision Tree':
    model = models['dec_tree']
elif model_choice == 'K-Nearest Neighbors':
    model = models['knn']
else:
    model = models['rf_model']

prediction = model.predict(input_data)
st.write(f'Prediksi Kepuasan Pelanggan: {"Puas" if prediction[0] else "Tidak Puas"}')
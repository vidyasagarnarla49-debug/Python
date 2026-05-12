import streamlit as st
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="10.164.105.137",
    user="root",
    password="M_NEXPROSIM_2026",
    database="mes_lab_pun",
    port="3306"
)

df = pd.read_sql("SELECT * FROM machine_quality_data", conn)

st.dataframe(df)
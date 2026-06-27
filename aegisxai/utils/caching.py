import streamlit as st
import pandas as pd
import joblib


@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    return df


@st.cache_data
def get_metrics_row(metrics):
    return pd.DataFrame([metrics])


@st.cache_resource
def load_model(path):
    return joblib.load(path)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("data/students.csv")


st.title("Student Performance Dashboard")

st.subheader("Dataset")
st.write(data)

st.subheader("Average Marks")
avg = data.mean(numeric_only=True)
st.bar_chart(avg)

st.subheader("Math Score Distribution")
fig, ax = plt.subplots()
sns.histplot(data["Math"], bins=5, ax=ax)
st.pyplot(fig)


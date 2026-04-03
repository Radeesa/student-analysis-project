import streamlit as st
import pandas as pd
import plotly.express as px


# Page Config

st.set_page_config(layout="wide", page_title="Student Dashboard")


# Custom CSS (Modern UI)

st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
}

/* Center Title */
h1 {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #2c3e50;
}

/* Remove top padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Subtitle */
p {
    text-align: center;
    font-size: 18px;
}

/* Metric Cards */
.stMetric {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
}

/* Center metric text */
[data-testid="stMetricLabel"], 
[data-testid="stMetricValue"] {
    text-align: center !important;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #2c3e50;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# Load Data

@st.cache_data
def load_data():
    return pd.read_csv("../data/Student_data.csv")

data = load_data()


# Header

st.markdown("<h1>Student Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p>Analyze student performance, attendance, and academic trends</p>", unsafe_allow_html=True)


# Sidebar Filters

st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("---")

# Default
filtered_data = data.copy()

# Gender Filter
if "Gender" in data.columns:
    genders = ["All"] + list(data["Gender"].unique())
    gender = st.sidebar.selectbox("Select Gender", genders)

    if gender != "All":
        filtered_data = filtered_data[filtered_data["Gender"] == gender]

# Major Filter
selected_major = "All"
if "Major" in data.columns:
    majors = ["All"] + sorted(data["Major"].unique())
    selected_major = st.sidebar.selectbox("Select Major", majors)

    if selected_major != "All":
        filtered_data = filtered_data[filtered_data["Major"] == selected_major]


# KPI Metrics

st.markdown("## Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Students", len(filtered_data))

with col2:
    st.metric("Avg CGPA", round(filtered_data["Final_CGPA"].mean(), 2))

with col3:
    st.metric("Highest CGPA", filtered_data["Final_CGPA"].max())

st.markdown("---")


# Charts Section

st.markdown("## Visual Analysis")

col1, col2 = st.columns(2)

# Pie Chart
if "Gender" in filtered_data.columns:
    with col1:
        fig2 = px.pie(
            filtered_data,
            names="Gender",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig2.update_layout(
            title={'text': "Gender Distribution", 'x': 0.5}
        )
        st.plotly_chart(fig2, width="stretch")

# Bar Chart
if "Attendance_Pct" in filtered_data.columns:

    filtered_data = filtered_data.copy()

    filtered_data["Attendance_Group"] = pd.cut(
        filtered_data["Attendance_Pct"],
        bins=[0, 50, 70, 85, 100],
        labels=["0-50%", "50-70%", "70-85%", "85-100%"]
    )

    avg_cgpa = filtered_data.groupby(
        "Attendance_Group", observed=False
    )["Final_CGPA"].mean().reset_index()

    with col2:
        fig4 = px.bar(
            avg_cgpa,
            x="Attendance_Group",
            y="Final_CGPA",
            color="Final_CGPA",
            color_continuous_scale="Blues"
        )
        fig4.update_layout(
            title={'text': "Average CGPA by Attendance Level", 'x': 0.5},
            xaxis_title="Attendance Range",
            yaxis_title="Average CGPA"
        )
        st.plotly_chart(fig4, width="stretch")


# Additional Chart

numeric_cols = filtered_data.select_dtypes(include='number')
avg_scores = numeric_cols.mean()

fig3 = px.bar(
    x=avg_scores.index,
    y=avg_scores.values,
    color=avg_scores.values,
    color_continuous_scale="Viridis",
    labels={'x': 'Features', 'y': 'Average Value'}
)

fig3.update_layout(
    title={'text': "Average Values of Numerical Features", 'x': 0.5}
)

st.plotly_chart(fig3, width="stretch")

st.markdown("---")


# Search

st.markdown("## 🔎 Search Data")

search = st.text_input("Type to search")

if search:
    filtered_data = filtered_data[
        filtered_data.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
    ]


# Data Table
st.markdown("## Data Preview")
st.dataframe(filtered_data)


# Extra Info
with st.expander("Dataset Info"):
    st.write(data.head())
    st.write(data.columns)

with st.expander("View Raw Data"):
    st.dataframe(filtered_data)


# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>Developed by Radeesa</p>", unsafe_allow_html=True)
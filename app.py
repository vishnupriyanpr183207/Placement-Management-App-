import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# --- App Header and Introduction ---
st.markdown("<h1 style='text-align: center;'>🎓 University Placement Analysis App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Gain valuable insights into student placements across departments and years. - by Vishnupriyan P R</p>", unsafe_allow_html=True)

# --- Catchphrase & Use Case ---
st.markdown("""
**📌 Unlock the Patterns Behind the Placements!**

Whether you're a student planning your career, a faculty advisor, or an administrator—this app provides:
- Department-wise placement performance,
- Salary distribution trends,
- Year-over-year placement growth.
""")

# --- File Upload Section ---
st.sidebar.markdown("### 📂 Upload CSV")
uploaded_file = st.sidebar.file_uploader("Upload your placement data CSV", type=["csv"])

# Load Data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Custom CSV file loaded successfully.")
else:
    df = pd.read_csv("sample_placement.csv")
    st.info("ℹ️ Using default sample data.")

# --- Filter Section ---
st.sidebar.header("Filters")
if "Year" in df.columns:
    selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].dropna().unique()))
    filtered_df = df[df['Year'] == selected_year]
else:
    st.error("❌ 'Year' column missing in the dataset.")
    st.stop()

# --- Bar Plot: Placement Rate ---
st.subheader("📊 Placement Rate by Department")
if "Student" in df.columns and "Department" in df.columns:
    placement_rate = filtered_df.groupby('Department')['Student'].apply(lambda x: (x == 'Yes').sum())
    st.bar_chart(placement_rate)
else:
    st.warning("⚠️ Required columns 'Student' or 'Department' not found in data.")

# --- Box Plot: Salary Distribution ---
st.subheader("💰 Salary Distribution by Department")
if "Package" in df.columns and "Department" in df.columns:
    fig1, ax1 = plt.subplots()
    sns.boxplot(data=filtered_df[filtered_df['Student'] == 'Yes'], x='Department', y='Package', ax=ax1)
    st.pyplot(fig1)
else:
    st.warning("⚠️ Columns required for box plot ('Package', 'Department') are missing.")

# --- Line Plot: Yearly Placement Trend ---
st.subheader("📈 Yearly Placement Trend")
if "Student" in df.columns and "Year" in df.columns:
    trend = df[df['Student'] == 'Yes'].groupby('Year')['Student'].count().reset_index()
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=trend, x='Year', y='Student', marker='o', ax=ax2)
    st.pyplot(fig2)

# --- Raw Data Display ---
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)

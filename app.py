import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load local CSV file
df = pd.read_csv("sample_placement.csv")

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

# Sidebar Filters
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
filtered_df = df[df['Year'] == selected_year]

# --- Bar Plot: Placement Rate ---
st.subheader("📊 Placement Rate by Department")
placement_rate = filtered_df.groupby('Department')['Student'].apply(lambda x: (x == 'Yes').sum())
st.bar_chart(placement_rate)

# --- Box Plot: Salary Distribution ---
st.subheader("💰 Salary Distribution by Department")
fig1, ax1 = plt.subplots()
sns.boxplot(data=filtered_df[filtered_df['Student'] == 'Yes'], x='Department', y='Package', ax=ax1)
st.pyplot(fig1)

# --- Line Plot: Yearly Placement Trend ---
st.subheader("📈 Yearly Placement Trend")
trend = df[df['Student'] == 'Yes'].groupby('Year')['Student'].count().reset_index()
fig2, ax2 = plt.subplots()
sns.lineplot(data=trend, x='Year', y='Student', marker='o', ax=ax2)
st.pyplot(fig2)

# --- Raw Data Display ---
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)

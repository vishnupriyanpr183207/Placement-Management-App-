```python
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- App Header and Introduction ---
st.markdown(
    "<h1 style='text-align: center;'>🎓 University Placement Analysis App</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Gain valuable insights into student placements across departments and years. - by Vishnupriyan P R</p>",
    unsafe_allow_html=True
)

# --- Catchphrase & Use Case ---
st.markdown("""
### 📌 Unlock the Patterns Behind the Placements!

Whether you're a student planning your career, a faculty advisor, or an administrator—this app provides:

- Department-wise placement performance
- Salary distribution trends
- Year-over-year placement growth
""")

# --- File Upload Section ---
st.sidebar.markdown("## 📂 Upload CSV")

uploaded_file = st.sidebar.file_uploader(
    "Upload your placement data CSV",
    type=["csv"]
)

# --- Load Data ---
try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Custom CSV file loaded successfully.")
    else:
        df = pd.read_csv("sample_placement.csv")
        st.info("ℹ️ Using default sample data.")

except Exception as e:
    st.error(f"❌ Error loading CSV file: {e}")
    st.stop()

# --- Check Required Columns ---
required_columns = ['Year', 'Department', 'Student', 'Package']

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"❌ Missing columns in dataset: {missing_columns}")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df['Year'].dropna().unique())
)

filtered_df = df[df['Year'] == selected_year]

# --- Bar Plot: Placement Rate ---
st.subheader("📊 Placement Rate by Department")

placement_rate = (
    filtered_df.groupby('Department')['Student']
    .apply(lambda x: (x == 'Yes').sum())
)

st.bar_chart(placement_rate)

# --- Box Plot: Salary Distribution ---
st.subheader("💰 Salary Distribution by Department")

placed_students = filtered_df[filtered_df['Student'] == 'Yes']

if not placed_students.empty:
    fig1, ax1 = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=placed_students,
        x='Department',
        y='Package',
        ax=ax1
    )

    plt.xticks(rotation=45)
    st.pyplot(fig1)

else:
    st.warning("⚠️ No placed students found for selected year.")

# --- Line Plot: Yearly Placement Trend ---
st.subheader("📈 Yearly Placement Trend")

trend = (
    df[df['Student'] == 'Yes']
    .groupby('Year')['Student']
    .count()
    .reset_index(name='Placed Students')
)

fig2, ax2 = plt.subplots(figsize=(8, 5))

sns.lineplot(
    data=trend,
    x='Year',
    y='Placed Students',
    marker='o',
    ax=ax2
)

st.pyplot(fig2)

# --- Raw Data Display ---
if st.checkbox("Show Raw Data"):
    st.subheader("📄 Raw Data")
    st.dataframe(filtered_df)
```

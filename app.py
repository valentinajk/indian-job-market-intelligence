import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Job Market Intelligence Dashboard", layout="wide")

st.title("📊 Indian Job Market Intelligence Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("cleaned_job_market_data.csv")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filter Options")

selected_city = st.sidebar.selectbox(
    "Select City",
    options=["All"] + sorted(df['location'].unique().tolist())
)

selected_role = st.sidebar.selectbox(
    "Role Type",
    options=["All", "Tech", "Non-Tech"]
)

# Apply Filters
filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[filtered_df['location'] == selected_city]

if selected_role == "Tech":
    filtered_df = filtered_df[filtered_df['is_tech'] == True]
elif selected_role == "Non-Tech":
    filtered_df = filtered_df[filtered_df['is_tech'] == False]

# ---------------- BASIC METRICS ----------------
st.subheader("📈 Market Overview")

total_jobs = len(filtered_df)
avg_salary = int(filtered_df['averageSalary'].mean()) if total_jobs > 0 else 0

tech_data = filtered_df[filtered_df['is_tech'] == True]
nontech_data = filtered_df[filtered_df['is_tech'] == False]

tech_avg = int(tech_data['averageSalary'].mean()) if len(tech_data) > 0 else None
nontech_avg = int(nontech_data['averageSalary'].mean()) if len(nontech_data) > 0 else None

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", total_jobs)

col2.metric(
    "Average Salary",
    f"₹{avg_salary:,}" if total_jobs > 0 else "N/A"
)

col3.metric(
    "Tech Avg Salary",
    f"₹{tech_avg:,}" if tech_avg is not None else "No Tech Data"
)

st.write(
    f"Non-Tech Average Salary: ₹{nontech_avg:,}"
    if nontech_avg is not None
    else "No Non-Tech Data"
)
# ---------------- SALARY DISTRIBUTION ----------------
st.subheader("💰 Salary Distribution")

fig, ax = plt.subplots()
ax.hist(filtered_df['averageSalary'], bins=30)
ax.set_xlabel("Salary")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# ---------------- EXPERIENCE VS SALARY ----------------
st.subheader("📊 Salary Growth by Experience")

exp_salary = filtered_df.groupby('averageExperience')['averageSalary'].mean().sort_index()

fig2, ax2 = plt.subplots()
ax2.plot(exp_salary.index, exp_salary.values)
ax2.set_xlabel("Experience (Years)")
ax2.set_ylabel("Average Salary")
st.pyplot(fig2)

# ---------------- CITY ANALYSIS ----------------
st.subheader("🏙️ Top 10 Cities by Average Salary")

city_salary = filtered_df.groupby('location')['averageSalary'].mean().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
ax3.barh(city_salary.index, city_salary.values)
ax3.set_xlabel("Average Salary")
ax3.invert_yaxis()
st.pyplot(fig3)

# ---------------- SALARY PREDICTOR ----------------
st.subheader("🤖 Smart Salary Predictor")

experience_input = st.slider("Years of Experience", 0, 20, 2)
tech_input = st.selectbox("Is this a Tech Role?", ["No", "Yes"])

is_tech_value = 1 if tech_input == "Yes" else 0

base_salary = 200000
predicted_salary = base_salary + (experience_input * 90000) + (is_tech_value * 100000)

st.success(f"🎯 Estimated Salary: ₹{int(predicted_salary):,}")

if total_jobs > 0:
    if predicted_salary > avg_salary:
        st.info("🚀 This is above the current filtered market average!")
    else:
        st.warning("📊 This is below the current filtered market average.")

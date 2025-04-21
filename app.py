import pandas as pd
from textblob import TextBlob
import streamlit as st

# Page config
st.set_page_config(page_title="AI Student Success Dashboard", layout="wide")
st.title("🎓 AI-Driven Student Success Dashboard")

# Sidebar upload
st.sidebar.header("Upload Student CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using sample data as no file was uploaded.")
    data = {
        "Student_ID": range(1, 21),
        "GPA": [2.9, 3.5, 1.8, 3.0, 2.2, 2.7, 3.8, 1.9, 2.3, 3.1, 3.6, 2.5, 1.7, 2.0, 3.4, 2.8, 3.2, 2.1, 1.6, 2.9],
        "Attendance_%": [80, 95, 60, 85, 70, 75, 98, 65, 72, 90, 97, 68, 50, 60, 96, 78, 89, 67, 55, 85],
        "LMS_Logins": [10, 30, 5, 15, 8, 12, 40, 6, 9, 20, 35, 7, 4, 5, 33, 11, 23, 7, 3, 17],
        "Financial_Risk": [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        "Messages": [
            "I’m struggling with my assignments.",
            "Feeling great about the course!",
            "I might drop out soon.",
            "The class is okay, a bit hard.",
            "Too expensive. Don’t think I can continue.",
            "Having some issues but trying my best.",
            "Loving the experience!",
            "Need help ASAP.",
            "I’m lost in the lectures.",
            "Things are going well.",
            "This is a fun course!",
            "Kinda stressed lately.",
            "I don’t want to do this anymore.",
            "Overwhelmed and frustrated.",
            "Really interesting content!",
            "Trying to stay on top of things.",
            "Motivated and focused.",
            "It’s tough managing everything.",
            "I’m burnt out.",
            "Doing alright overall."
        ]
    }
    df = pd.DataFrame(data)

# Dropout Risk Prediction
def predict_risk(row):
    score = 0
    if row["GPA"] < 2.5: score += 1
    if row["Attendance_%"] < 70: score += 1
    if row["LMS_Logins"] < 10: score += 1
    if row["Financial_Risk"] == 1: score += 1

    if score >= 3:
        return "High"
    elif score == 2:
        return "Medium"
    else:
        return "Low"

df["Dropout_Risk"] = df.apply(predict_risk, axis=1)

# Sentiment Analysis
df["Sentiment_Score"] = df["Messages"].apply(lambda x: TextBlob(x).sentiment.polarity)
df["Sentiment"] = df["Sentiment_Score"].apply(lambda x: "Negative" if x < 0 else "Positive")

# Advisor Alerts
df["Alert"] = df.apply(lambda x: "⚠️ Advisor Follow-up" if x["Dropout_Risk"] == "High" or x["Sentiment"] == "Negative" else "✓ OK", axis=1)

# Filters
high_risk = df[df["Dropout_Risk"] == "High"]
negative_sentiment = df[df["Sentiment"] == "Negative"]
alerts = df[df["Alert"] == "⚠️ Advisor Follow-up"]

# Quadrant Layout
st.subheader("📊 Quadrant View of Student Insights")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown("### 🧑‍🎓 All Students")
    st.dataframe(df)

with col2:
    st.markdown("### 🔥 High-Risk Students")
    st.dataframe(high_risk)

with col3:
    st.markdown("### 💬 Negative Sentiment")
    st.dataframe(negative_sentiment)

with col4:
    st.markdown("### 🚨 Advisor Follow-up Alerts")
    st.dataframe(alerts)

# Optional download
st.download_button("📥 Download At-Risk Students", alerts.to_csv(index=False), "at_risk_students.csv", "text/csv")

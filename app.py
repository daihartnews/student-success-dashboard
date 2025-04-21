import pandas as pd
from textblob import TextBlob
import streamlit as st

# Page config
st.set_page_config(page_title="AI Student Success Dashboard", layout="wide")
st.title("📊 AI-Driven Student Success Dashboard")

# Sidebar upload
st.sidebar.header("📁 Upload Student CSV File")
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
    return score

df["Risk_Score"] = df.apply(predict_risk, axis=1)
df["Dropout_Risk"] = df["Risk_Score"].apply(lambda x: "High" if x >= 3 else "Medium" if x == 2 else "Low")

# Sentiment Analysis
df["Sentiment_Score"] = df["Messages"].apply(lambda x: TextBlob(x).sentiment.polarity)
df["Sentiment"] = df["Sentiment_Score"].apply(lambda x: "Negative" if x < 0 else "Positive")

# Recommendations
def get_recommendation(row):
    recs = []
    if row["GPA"] < 2.5:
        recs.append("📚 Academic tutoring")
    if row["Attendance_%"] < 70:
        recs.append("🕒 Attendance counseling")
    if row["LMS_Logins"] < 10:
        recs.append("💻 LMS engagement support")
    if row["Financial_Risk"] == 1:
        recs.append("💰 Financial aid check-in")
    if row["Sentiment"] == "Negative":
        recs.append("🧠 Mental health referral")
    return ", ".join(recs)

df["Recommendations"] = df.apply(get_recommendation, axis=1)
df["Alert"] = df.apply(lambda x: "⚠️ Advisor Action" if x["Dropout_Risk"] == "High" or x["Sentiment"] == "Negative" else "✓ OK", axis=1)

# Filters
summary_cols = ["Student_ID", "GPA", "Attendance_%", "Dropout_Risk"]
high_risk = df[df["Dropout_Risk"] == "High"][summary_cols]
negative_sentiment = df[df["Sentiment"] == "Negative"][summary_cols + ["Sentiment"]]
alerts = df[df["Alert"] == "⚠️ Advisor Action"][summary_cols + ["Sentiment", "Alert", "Recommendations"]]

# Sexy Quadrant Layout
st.subheader("📈 Student Insights Overview")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown("### 👥 All Students (Summary)")
    st.dataframe(df[summary_cols])

with col2:
    st.markdown("### 🔥 High Risk")
    st.dataframe(high_risk)

with col3:
    st.markdown("### 😟 Negative Sentiment")
    st.dataframe(negative_sentiment)

with col4:
    st.markdown("### 🚨 Advisor Alerts & Suggestions")
    st.dataframe(alerts)

# Download button
st.download_button("📥 Download Alerts", alerts.to_csv(index=False), "advisor_alerts.csv", "text/csv")

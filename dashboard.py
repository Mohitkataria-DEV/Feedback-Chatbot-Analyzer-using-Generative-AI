import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
import string

FILE_NAME = "feedback_data.csv"

st.set_page_config(page_title="Feedback Dashboard", layout="wide")

st.title("📊 Customer Feedback Dashboard")

# Safety check
if not os.path.exists(FILE_NAME):
    st.warning("No feedback data found. Please run the chatbot first.")
    st.stop()

# Load data
df = pd.read_csv(FILE_NAME)

if df.empty:
    st.warning("Feedback file is empty.")
    st.stop()

# =====================
# KPIs
# =====================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Responses", len(df))

with col2:
    st.metric("Average Rating", round(df["rating"].mean(), 2))

with col3:
    negative_pct = round(
        (df["sentiment"] == "negative").mean() * 100, 1
    )
    st.metric("Negative Feedback (%)", f"{negative_pct}%")

st.divider()

# =====================
# Sentiment Distribution
# =====================
st.subheader("Sentiment Distribution")
sentiment_counts = df["sentiment"].value_counts()

fig1, ax1 = plt.subplots()
sentiment_counts.plot(kind="bar", ax=ax1)
st.pyplot(fig1)

# =====================
# Rating Distribution
# =====================
st.subheader("Rating Distribution")
fig2, ax2 = plt.subplots()
df["rating"].value_counts().sort_index().plot(kind="bar", ax=ax2)
st.pyplot(fig2)

# =====================
# Keyword Analysis
# =====================
STOPWORDS = {
    "the", "is", "was", "and", "to", "a", "of", "it", "very",
    "really", "for", "in", "on", "with", "this", "that"
}

def extract_keywords(df, sentiment_type):
    text = " ".join(
        df[df["sentiment"] == sentiment_type]["feedback"].dropna()
    ).lower()

    words = text.split()

    # Remove punctuation
    words = [w.strip(string.punctuation) for w in words]

    # Remove stopwords and empty words
    words = [w for w in words if w and w not in STOPWORDS]

    return Counter(words).most_common(5)

st.subheader("Top Issues & Strengths")

col4, col5 = st.columns(2)

with col4:
    st.write("❌ Top Complaints")
    complaints = extract_keywords(df, "negative")
    if complaints:
        for word, count in complaints:
            st.write(f"- **{word}** ({count})")
    else:
        st.write("No negative feedback yet.")

with col5:
    st.write("✅ Top Strengths")
    strengths = extract_keywords(df, "positive")
    if strengths:
        for word, count in strengths:
            st.write(f"- **{word}** ({count})")
    else:
        st.write("No positive feedback yet.")

st.divider()

st.caption("Generated from chatbot feedback data")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Page setup
st.set_page_config(
    page_title="AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# AI setup (FROM .env)
openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_ai(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# Load sample data
@st.cache_data
def load_data():
    months = ['Jan','Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec']

    return pd.DataFrame({
        'Month': months,
        'Sales': np.random.randint(50000, 200000, 12),
        'Profit': np.random.randint(10000, 80000, 12),
        'Leads': np.random.randint(100, 500, 12)
    })


df = load_data()

# Title
st.title("📊 AI-Powered Business Dashboard")
st.caption("Ask questions about your data in plain English")

# KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", "Rs." + str(df['Sales'].sum()), "+12%")
c2.metric("Total Profit", "Rs." + str(df['Profit'].sum()), "+8%")
c3.metric("Best Month", df.loc[df['Sales'].idxmax(), 'Month'])
c4.metric("Avg Leads", str(int(df['Leads'].mean())) + " / mo")

# Charts
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Sales Trend")

    fig1 = px.line(
        df,
        x='Month',
        y='Sales',
        markers=True,
        color_discrete_sequence=['#00d4ff']
    )

    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Profit vs Sales")

    fig2 = px.bar(
        df,
        x='Month',
        y=['Sales', 'Profit'],
        barmode='group'
    )

    st.plotly_chart(fig2, use_container_width=True)

# AI Q&A section
st.divider()

st.subheader("🤖 Ask AI About Your Data")

question = st.text_input(
    "Your question:",
    placeholder="Which month had highest profit?"
)

if st.button("Ask AI") and question:

    with st.spinner("Thinking..."):

        prompt = f"""
You are a business analyst.

Here is the business data:

{df.to_string(index=False)}

User Question:
{question}
"""

        answer = ask_ai(prompt)

        st.success(answer)
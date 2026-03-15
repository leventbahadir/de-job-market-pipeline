import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

st.set_page_config(page_title="DE Job Market", layout="wide")
st.title("Data Engineer Job Market Dashboard")

col1, col2, col3 = st.columns(3)

total = pd.read_sql("SELECT COUNT(*) as count FROM raw.job_postings", engine)
col1.metric("Total Jobs Tracked", total['count'][0])

top_skill = pd.read_sql("SELECT skill FROM marts.skill_demand ORDER BY job_count DESC LIMIT 1", engine)
col2.metric("Top Skill", top_skill['skill'][0])

last_updated = pd.read_sql("SELECT MAX(ingested_at) as ts FROM raw.job_postings", engine)
col3.metric("Last Updated", str(last_updated['ts'][0])[:16])

st.subheader("Top trending skills")
skills_df = pd.read_sql("SELECT skill, job_count, pct_of_total FROM marts.skill_demand ORDER BY job_count DESC LIMIT 15", engine)
fig1 = px.bar(skills_df, x='job_count', y='skill', orientation='h', color='job_count', color_continuous_scale='blues')
fig1.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Jobs by location")
location_df = pd.read_sql("""
    SELECT location, COUNT(*) as job_count 
    FROM raw.job_postings 
    WHERE location IS NOT NULL 
    GROUP BY location 
    ORDER BY job_count DESC 
    LIMIT 15
""", engine)
fig2 = px.bar(location_df, x='job_count', y='location', orientation='h', color='job_count', color_continuous_scale='teal')
fig2.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top hiring companies")
companies_df = pd.read_sql("""
    SELECT company, COUNT(*) as job_count 
    FROM raw.job_postings 
    WHERE company IS NOT NULL 
    GROUP BY company 
    ORDER BY job_count DESC 
    LIMIT 15
""", engine)
fig3 = px.bar(companies_df, x='job_count', y='company', orientation='h', color='job_count', color_continuous_scale='purples')
fig3.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

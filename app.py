import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{st.secrets['DB_USER_SUPABASE']}:{st.secrets['DB_PASSWORD_SUPABASE']}"
    f"@{st.secrets['DB_HOST_SUPABASE']}:{st.secrets['DB_PORT_SUPABASE']}"
    f"/{st.secrets['DB_NAME_SUPABASE']}"
)

st.set_page_config(page_title="DE Job Market", layout="wide")

st.markdown("""
    <style>
    iframe { pointer-events: none; }
    .stApp { background-color: #1a1a1a; }
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp div {
        color: #f0f0f0;
    }
    .stMetric { background-color: #2a2a2a; border-radius: 8px; padding: 12px; }
    </style>
    <div style="position:fixed; bottom:30px; right:20px; z-index:999; display:flex; flex-direction:column; gap:8px;">
        <button onclick="window.scrollTo({top:0, behavior:'smooth'})"
            style="padding:8px 14px; border-radius:6px; border:1px solid #555; cursor:pointer; background:#2a2a2a; color:white; font-size:16px;">↑</button>
        <button onclick="window.scrollTo({top:document.body.scrollHeight, behavior:'smooth'})"
            style="padding:8px 14px; border-radius:6px; border:1px solid #555; cursor:pointer; background:#2a2a2a; color:white; font-size:16px;">↓</button>
    </div>
""", unsafe_allow_html=True)

st.title("Data Engineer Job Market Stats")

# ── Load filter options ──────────────────────────────────────────────
locations_df = pd.read_sql("""
    SELECT DISTINCT location FROM raw.job_postings
    WHERE location IS NOT NULL ORDER BY location
""", engine)

titles_df = pd.read_sql("""
    SELECT DISTINCT title FROM raw.job_postings
    WHERE title IS NOT NULL ORDER BY title
""", engine)

# ── Sidebar filters ──────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")

    selected_locations = st.multiselect(
        "Location",
        options=locations_df['location'].tolist(),
        default=[]
    )

    selected_titles = st.multiselect(
        "Job Title",
        options=titles_df['title'].tolist(),
        default=[]
    )

# ── Build WHERE clause dynamically ──────────────────────────────────
def build_where(extra_conditions=None):
    conditions = []
    if selected_locations:
        locs = ", ".join([f"'{l}'" for l in selected_locations])
        conditions.append(f"location IN ({locs})")
    if selected_titles:
        titles = ", ".join([f"'{t}'" for t in selected_titles])
        conditions.append(f"title IN ({titles})")
    if extra_conditions:
        conditions.extend(extra_conditions)
    return "WHERE " + " AND ".join(conditions) if conditions else ""

# ── Metrics ──────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

where = build_where(["1=1"])
total = pd.read_sql(f"SELECT COUNT(*) as count FROM raw.job_postings {build_where()}", engine)
col1.metric("Total Jobs Tracked", total['count'][0])

top_skill = pd.read_sql("SELECT skill FROM marts.skill_demand ORDER BY job_count DESC LIMIT 1", engine)
col2.metric("Top Skill", top_skill['skill'][0])

last_updated = pd.read_sql("SELECT MAX(ingested_at) as ts FROM raw.job_postings", engine)
col3.metric("Last Updated", str(last_updated['ts'][0])[:16])

# ── Skills chart ─────────────────────────────────────────────────────
st.subheader("Top trending skills")
skills_df = pd.read_sql("""
    SELECT skill, job_count, pct_of_total 
    FROM marts.skill_demand 
    ORDER BY job_count DESC LIMIT 15
""", engine)
fig1 = px.bar(skills_df, x='job_count', y='skill', orientation='h', color='job_count',
              color_continuous_scale=[[0, '#ffffff'], [1, '#0066FF']])
fig1.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,
                   paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#f0f0f0')
st.plotly_chart(fig1, use_container_width=True)

# ── Location chart ───────────────────────────────────────────────────
st.subheader("Jobs by location")
location_df = pd.read_sql(f"""
    SELECT location, COUNT(*) as job_count 
    FROM raw.job_postings 
    {build_where(["location IS NOT NULL"])}
    GROUP BY location 
    ORDER BY job_count DESC 
    LIMIT 15
""", engine)
fig2 = px.bar(location_df, x='job_count', y='location', orientation='h', color='job_count',
              color_continuous_scale=[[0, '#ffffff'], [1, '#0066FF']])
fig2.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,
                   paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#f0f0f0')
st.plotly_chart(fig2, use_container_width=True)

# ── Companies chart ──────────────────────────────────────────────────
st.subheader("Top hiring companies")
companies_df = pd.read_sql(f"""
    SELECT company, COUNT(*) as job_count 
    FROM raw.job_postings 
    {build_where(["company IS NOT NULL"])}
    GROUP BY company 
    ORDER BY job_count DESC 
    LIMIT 15
""", engine)
fig3 = px.bar(companies_df, x='job_count', y='company', orientation='h', color='job_count',
              color_continuous_scale=[[0, '#ffffff'], [1, '#0066FF']])
fig3.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,
                   paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font_color='#f0f0f0')
st.plotly_chart(fig3, use_container_width=True)
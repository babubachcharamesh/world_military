import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.data_loader import load_data, filter_data

# Page Config
st.set_page_config(
    page_title="Global Sentinel | Military Power Intel",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Data Initialization
df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>COMMAND CENTRE</h1>", unsafe_allow_html=True)
    st.divider()
    
    selected_region = st.multiselect("Select Regions", options=["Global"] + sorted(df['Country'].unique().tolist()), default="Global")
    rank_range = st.slider("Military Rank Range", 1, 50, (1, 10))
    
    st.markdown("---")
    st.markdown("### 📊 Metrics Selection")
    show_funding = st.checkbox("Show Funding Data", value=True)
    show_manpower = st.checkbox("Show Manpower Analysis", value=True)
    
    st.divider()
    st.markdown("🛡️ **System Status:** Online")
    st.markdown("🕒 **Last Intel Sync:** 2024.Q4")

# --- MAIN CONTENT ---
st.markdown("<h1 class='main-title'>GLOBAL MILITARY SENTINEL</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-style: italic; color: #888;'>Comprehensive Intelligence on World Military Power & Economic Defense Funding</p>", unsafe_allow_html=True)

filtered_df = df[(df['Rank'] >= rank_range[0]) & (df['Rank'] <= rank_range[1])]

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("Top Superpower", filtered_df.iloc[0]['Country'])
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    total_budget = filtered_df['Budget_Billions'].sum()
    st.metric("Total Regional Budget", f"${total_budget:.1f}B")
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    avg_pi = filtered_df['PowerIndex'].mean()
    st.metric("Avg PowerIndex", f"{avg_pi:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    total_personnel = filtered_df['Total_Personnel'].sum() / 1e6
    st.metric("Total Manpower", f"{total_personnel:.1f}M")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# Main Visualizations
tab1, tab2, tab3 = st.tabs(["🌐 Strategic Map", "📉 Power vs Funding", "⚔️ Force Comparison"])

with tab1:
    st.subheader("Global Deployment Analysis")
    # Using bubble chart for map to show power vs budget
    fig_map = px.scatter_geo(
        filtered_df,
        locations="Country",
        locationmode="country names",
        size="Total_Personnel",
        color="Budget_Billions",
        hover_name="Country",
        hover_data={"Rank": True, "PowerIndex": True, "Budget_Billions": True},
        projection="natural earth",
        template="plotly_dark",
        color_continuous_scale="Viridis"
    )
    fig_map.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("Budget Allocation (Billions USD)")
        fig_budget = px.bar(
            filtered_df,
            x="Country",
            y="Budget_Billions",
            color="Budget_Billions",
            template="plotly_dark",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_budget, use_container_width=True)
        
    with col_right:
        st.subheader("Efficiency: PowerIndex vs Budget")
        fig_efficiency = px.scatter(
            filtered_df,
            x="Budget_Billions",
            y="PowerIndex",
            size="Aircraft_Total",
            color="Country",
            hover_name="Country",
            template="plotly_dark",
            log_x=True
        )
        # PowerIndex is better when lower, so we reverse y-axis
        fig_efficiency.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_efficiency, use_container_width=True)

with tab3:
    st.subheader("Dual Force Intel Comparison")
    compare_col1, compare_col2 = st.columns(2)
    
    country1 = compare_col1.selectbox("Primary Nation", df['Country'].unique(), index=0)
    country2 = compare_col2.selectbox("Opposing/Ally Nation", df['Country'].unique(), index=2)
    
    def get_radar_data(country):
        row = df[df['Country'] == country].iloc[0]
        return [row['norm_Budget_USD'], row['norm_Aircraft_Total'], 
                row['norm_Tanks'], row['norm_Navy_Total'], row['norm_Personnel_Active']]

    categories = ['Budget', 'Air Power', 'Tank Force', 'Naval Fleet', 'Active Personnel']
    
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=get_radar_data(country1),
        theta=categories,
        fill='toself',
        name=country1,
        line_color='#00f2ff'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=get_radar_data(country2),
        theta=categories,
        fill='toself',
        name=country2,
        line_color='#7000ff'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=True,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Footer
st.divider()
st.markdown("<p style='text-align: center; color: #555;'>Data Source: Global Firepower 2024 & SIPRI Intelligence Reviews | Built for Strategic Analysis</p>", unsafe_allow_html=True)

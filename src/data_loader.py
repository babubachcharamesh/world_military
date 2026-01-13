import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load and preprocess the military power dataset."""
    df = pd.read_csv("data/military_power_2024.csv")
    
    # Calculate additional metrics
    df['Budget_Billions'] = df['Budget_USD'] / 1e9
    df['Total_Personnel'] = df['Personnel_Active'] + df['Personnel_Reserve']
    
    # Normalized scores for Radar Charts (0 to 1)
    metrics_to_normalize = ['Budget_USD', 'Aircraft_Total', 'Tanks', 'Navy_Total', 'Personnel_Active']
    for metric in metrics_to_normalize:
        col_name = f'norm_{metric}'
        df[col_name] = (df[metric] - df[metric].min()) / (df[metric].max() - df[metric].min())
        
    return df

def filter_data(df, countries=None, min_rank=1, max_rank=50):
    """Filter data based on user selection."""
    filtered_df = df[(df['Rank'] >= min_rank) & (df['Rank'] <= max_rank)]
    if countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(countries)]
    return filtered_df

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Interact with Gapminder Data")

df = pd.read_csv("Data/gapminder_tidy.csv")



continent_list = list(df["continent"].unique())
metric_list = list(df["metric"].unique())

metric_labels = {
    "gdpPercap": "GDP Per Capita",
    "lifeExp": "Life Expectancy",
    "pop": "Population"
}

def format_metric(metric_raw):
    return metric_labels[metric_raw]

with st.sidebar:
    st.subheader("Configure the plot")
    continent = st.selectbox(label="Choose a continent", options=continent_list)
    metric = st.selectbox(label="Choose a metric", options=metric_list, format_func=format_metric)
    show_dataframe = st.checkbox(label="Show Table", value=False)

    query = f"continent=='{continent}' & metric=='{metric}'"
    df_filtered = df.query(query)

    country_list = list(df_filtered["country"].unique())
    
    selected_countries = st.multiselect(
        label="Select Countries to plot", 
        options=country_list, 
        default=country_list
    )

    df_filtered = df_filtered[df_filtered.country.isin(selected_countries)]

title = f"{metric_labels[metric]} in {continent}"
fig = px.line(
    df_filtered, 
    x="year", 
    y="value", 
    color="country", 
    title=title,
    labels={"value", metric_labels[metric]}
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("This plot shows the GDP Per Capita for all countries in the continent of Oceania")

if show_dataframe:
    st.dataframe(df_filtered)

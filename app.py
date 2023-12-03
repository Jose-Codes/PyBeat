import streamlit as st
import requests
import pandas as pd
from views import events_per_month

with st.sidebar:
    artist = st.text_input("Search an Artist")
    category = st.selectbox("Choose event details", options=["Map", "Table", "View available events by date", "View available artist events by country", "View artist events per month"])
if(artist):
    if category == "Map":
        # TODO: Make Map
        st.title("Map of events")
        st.markdown("This is a map of events in the world")
        st.map()
    elif category == "Table":
        # TODO: Make Table
        st.title("Table of events")
        st.markdown("This is a table of events in the world")
        st.table()
    elif category == "View available events by date":
        # TODO: Make available events by date Table
        st.title("View available events by date")
        st.markdown("This is a table of events in the world")
        st.table()
    elif category == "View available artist events by country":
        # TODO: Make available artist events by country Bar Chart
        st.title("View artist events by country")
        st.markdown("This is a table of events in the world")
        st.table()
    elif category == "View artist events per month":
        # TODO: Make artist events per month line chart
        events_per_month.get_artists_event_per_month(artist)
    else:
        # Default page view
        st.title("Map of events")
        st.markdown("This is a map of events in the world")
        st.map()
else:
        st.warning("Please enter an artist name.", icon="⚠️")

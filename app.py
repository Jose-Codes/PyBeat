import streamlit as st
import requests
import pandas as pd

#views
from views import events_by_country
from views import events_per_month
from views import table_view
from views import map_view

with st.sidebar:
    artist = st.text_input("Search an Artist")
    category = st.selectbox("Choose event details", options=["Map", "Table", "View available artist events by country", "View artist events per month"])
if(artist):
    if category == "Map":
        map_view.map_view(artist)
    elif category == "Table":
        table_view.display_table(artist)
    elif category == "View available artist events by country":
        events_by_country.get_artists_events_by_country(artist)
    elif category == "View artist events per month":
        events_per_month.get_artists_event_per_month(artist)
    else:
        # Default page view
        st.title("Map of events")
        st.markdown("This is a map of events in the world")
        st.map()
else:
        st.warning("Please enter an artist name.", icon="⚠️")
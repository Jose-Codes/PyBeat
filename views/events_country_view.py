import streamlit as st
import requests
import pandas as pd
import numpy as np

def get_artists_events_by_country(artist):
    artist_events_url = f"https://rest.bandsintown.com/artists/{artist}/events?app_id=foo&date=upcoming"
    
    events_result = requests.get(artist_events_url).json()

    if not events_result:
        st.title("No events found for this artist.")

    else:
        event_count = {} #country:count

        for event in events_result:
            country = event['venue']['country']
            event_count[country] = event_count.get(country, 0) + 1

        chart_data = pd.DataFrame(event_count.items(), columns=["Country", "# of Shows"])

        artist_name = events_result[0]["artist"]["name"]
        
        st.title(f"{artist_name}'s upcoming shows by country")
        st.bar_chart(chart_data, x="Country", y="# of Shows")

   


get_artists_events_by_country("playboi carti")





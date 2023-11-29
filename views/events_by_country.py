import streamlit as st
import requests
import pandas as pd

def get_artists_events_by_country(artist):
    
    #get time frame: upcoming, past, or specific range
    date = st.sidebar.selectbox("Choose event details", options=["Upcoming", "Past", "Specific range"])

    if date == "Specific range":
        start_date = st.sidebar.date_input("Start date:")
        end_date = st.sidebar.date_input("End date:")
        date = str(start_date) + ',' + str(end_date)

    
    artist_events_url = f"https://rest.bandsintown.com/artists/{artist}/events?app_id=foo&date={date.lower()}"
    events_result = requests.get(artist_events_url).json()

    if not events_result:
        st.title("No events found for this artist.")

    else:
        event_count = {} #country:count

        #iterate through response and get country count
        for event in events_result:
            country = event['venue']['country']
            event_count[country] = event_count.get(country, 0) + 1

        chart_data = pd.DataFrame(event_count.items(), columns=["Country", "# of Shows"])

        artist_name = events_result[0]["artist"]["name"]
        
        st.markdown(f"<h1 style='text-align: center'>{artist_name}'s shows by country</h1>", unsafe_allow_html=True)
        st.bar_chart(chart_data, x="Country", y="# of Shows")
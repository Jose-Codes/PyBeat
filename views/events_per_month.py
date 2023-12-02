import streamlit as st
import requests
import pandas as pd

def get_artists_event_per_month(artist):
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
        event_count = {} # month : count

        #iterate through response and get events per month
        for event in events_result:
            event_date = pd.to_datetime(event['datetime'])
            month = event_date.strftime('%B')  # '%B' gives full month name
            event_count[month] = event_count.get(month, 0) + 1

        chart_data = pd.DataFrame(event_count.items(), columns=["Month", "# of Shows"])

        artist_name = events_result[0]["artist"]["name"]

        st.markdown(f"<h1 style='text-align: center'>{artist_name}'s shows per month</h1>", unsafe_allow_html=True)
        st.line_chart(chart_data.set_index("Month"))

import streamlit as st
import requests
import pandas as pd

with st.sidebar:
    category = st.selectbox("Choose event details", options=["Map", "Table", "View available events by date", "View available artist events by country", "View artist events per month"])
    artist = st.text_input("Search an Artist")
if(artist):
    artist_information_url = f"https://rest.bandsintown.com/artists/{artist}?app_id=foo"
    artist_events_url = f"https://rest.bandsintown.com/artists/{artist}/events?app_id=foo"
    information_result = requests.get(artist_information_url).json()
    events_result = requests.get(artist_events_url).json()
    df = pd.DataFrame(events_result)
if category == "Map":
    # TODO: Make Map
    st.title("Map of events")
    st.markdown("This is a map of events in the world")
    st.map()

elif category == "Table":
    st.title("Table of events")
    st.markdown("This is a table of events in the world")
    table_data = df[['url', 'datetime', 'venue']]
    table_data = pd.concat([table_data.drop(['venue'], axis=1), table_data['venue'].apply(pd.Series)], axis=1)
    table_data = table_data[['url', 'datetime', 'location', 'name', 'street_address']]
    table_data.columns = ['Get Details', 'Event Date', 'Location', 'Venue Name', 'Address']
    table_data['Event Date'] = pd.to_datetime(table_data['Event Date'])

    st.dataframe(table_data, hide_index=True, column_config={
        "Get Details": st.column_config.LinkColumn("View Event Details")
    }, column_order=("Event Date", "Location", "Venue Name", "Address", "Get Details"))
elif category == "View available events by date":
    # TODO: Make available events by date Table
    st.title("View available events by date")
    st.markdown("This is a table of events in the world")
    st.table()
elif category == "View available artist events by country":
    # TODO: Make available artist events by country Bar Chart
    st.title("View available artist events by country")
    st.markdown("This is a table of events in the world")
    st.table()
elif category == "View artist events per month":
    # TODO: Make artist events per month line chart
    st.title("View artist events per month")
    st.markdown("This is a table of events in the world")
    st.table()
else:
    # Default page view
    st.title("Map of events")
    st.markdown("This is a map of events in the world")
    st.map()

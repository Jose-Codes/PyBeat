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
    # TODO: Make Table
    st.title("Table of events")
    st.markdown("This is a table of events in the world")
    # events(df)[
    #     url,
    #     datetime,
    #     venue{location, name},
    #     offers[]
    # ]
    table_data = df[['url', 'datetime', 'offers']]
    table_data['datetime'] = pd.to_datetime(table_data['datetime'])
    table_data['datetime_str'] = table_data['datetime'].dt.strftime(
    '%Y-%m-%d %H:%M:%S')
    table_data.drop('datetime_str', axis=1)
    st.data_editor(table_data,
                   column_config={
                    'url': st.column_config.LinkColumn(
                        "View More Details", 
                        disabled=True, 
                        width="medium"
                    ),
                   'datetime':st.column_config.DatetimeColumn(
                        "Event Date",
                        format="MMM Do, YYYY [at] h:mma z",
                    )},
                    hide_index=True)
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

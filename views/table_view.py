import streamlit as st
import requests
import pandas as pd


def display_table(artist):
    artist_events_url = f"https://rest.bandsintown.com/artists/{artist}/events?app_id=foo"
    events_result = requests.get(artist_events_url).json()

    if not events_result:
        st.warning("No events found for this artist.", icon="⚠️")
    elif 'errorMessage' in events_result:
        st.error("Please enter a valid artist name.", icon="⚠️")
    else:
        df = pd.DataFrame(events_result)
        if not df.empty:
            st.title(f"Table of {artist}'s events")
            table_data = df[['url', 'datetime', 'venue']]
            table_data = pd.concat([table_data.drop(
                ['venue'], axis=1), table_data['venue'].apply(pd.Series)], axis=1)
            table_data = table_data[['url', 'datetime',
                                     'location', 'name', 'street_address']]
            table_data.columns = [
                'Get Details', 'Event Date', 'Location', 'Venue Name', 'Address']
            table_data['Event Date'] = pd.to_datetime(table_data['Event Date'])
            if 'table_filter' not in st.session_state:
                st.session_state.table_filter = ''

            st.session_state.table_filter = st.multiselect(placeholder="Choose Locations to Filter By", label="Filter by Location",
                                                           options=table_data['Location'].drop_duplicates())
            if len(st.session_state.table_filter) == 0:
                st.dataframe(table_data, hide_index=True, column_config={"Get Details": st.column_config.LinkColumn("View Event Details")
                                                                         }, column_order=("Event Date", "Location", "Venue Name", "Address", "Get Details"))
            else:
                table_data = table_data[table_data['Location'].isin(
                    st.session_state.table_filter)]
                st.dataframe(table_data, hide_index=True, column_config={"Get Details": st.column_config.LinkColumn("View Event Details")
                                                                         }, column_order=("Event Date", "Location", "Venue Name", "Address", "Get Details"))

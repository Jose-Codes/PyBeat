import streamlit as st
import requests
from streamlit_folium import folium_static
import folium

# The st.cache decorator is used for caching, st.cache_data isn't a valid Streamlit function.
# Hence, using st.cache() instead.
@st.cache_data
def map_creator(locations, cities):
    # get average center of all locations
    center_latitude = sum([location[0] for location in locations]) / len(locations)
    center_longitude = sum([location[1] for location in locations]) / len(locations)
    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=2)

    # Add a marker for each location in the list
    for i, location in enumerate(locations):
        folium.Marker([location[0], location[1]], popup=cities[i], tooltip="Click for more info").add_to(m)

    return m

def get_event_coordinates(artist_name="Metallica"):
    events_url = f"https://rest.bandsintown.com/artists/{artist_name}/events?app_id=foo"
    events = requests.get(events_url).json()
    event_coordinates = [] # List of tuples
    event_cities = [] # List of strings
    if len(events) == 0:
        st.error("No events found for " + artist_name)
    else:
        # Use st.json to display the JSON response on the app screen
        for event in events:
            event_coordinates.append((float(event["venue"]["latitude"]), float(event["venue"]["longitude"])))
            country, city = event["venue"]["country"], event["venue"]["city"]
            event_cities.append(f"{country}, {city}")
        return event_coordinates, event_cities

def map_view():
    st.title("Map of Events")
    st.markdown("This is a map of events in the world.")
    artist_name = st.text_input("Enter artist name", value="Metallica")
    
    event_coordinates, event_cities = get_event_coordinates(artist_name)
    if event_coordinates is not None:
        folium_static(map_creator(event_coordinates, event_cities))
    else:
        st.error("No events found for " + artist_name)
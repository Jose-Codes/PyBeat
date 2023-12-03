import streamlit as st
import requests
from streamlit_folium import folium_static
import folium
import math

# The st.cache decorator is used for caching, st.cache_data isn't a valid Streamlit function.
# Hence, using st.cache() instead.
@st.cache_data
def map_creator(locations, cities):
    # get average center of all locations
    if len(locations) == 0:
        st.error("No events found")
        return None
    else:
        center_latitude = sum([location[0] for location in locations]) / len(locations)
        center_longitude = sum([location[1] for location in locations]) / len(locations)

    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=2)

    # Create a bounds list to fit the map to
    bounds = []

    # Add a marker for each location in the list
    for i, location in enumerate(locations):
        folium.Marker([location[0], location[1]], popup=cities[i], tooltip="Click for more info").add_to(m)
        bounds.append([location[0], location[1]])
    
    # Fit the map to the bounds if there are locations
    if bounds:
        m.fit_bounds(bounds)

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

def map_view(artist_name="Metallica"):
    st.title("Map of Events")
    st.markdown("This is a map of events in the world.")
    coords, cities = [], []
    
    # Checkbox to toggle area filter
    st.session_state.filter_by_area = st.checkbox("Filter by area", value=False)

    with st.form(key='event_form'):
        artist_name = st.text_input("Enter artist name", value=artist_name)
        
        if st.session_state.filter_by_area:
            # Number input for radius
            st.session_state.radius = st.number_input("Enter radius in miles", value=1000)

        submit_button = st.form_submit_button(label='Show Events')

    # When the user clicks the submit button, the code within this if block will run
    if submit_button:
        event_coordinates, event_cities = get_event_coordinates(artist_name)
        if event_coordinates is not None:
            if st.session_state.filter_by_area:
                user_location = get_user_location()  # You'll need to implement this function
                filtered_coordinates, filtered_cities = filter_events_by_area(event_coordinates, event_cities, 
                                                                              user_location, radius=st.session_state.radius)
                if len(filtered_coordinates) == 0:
                    st.error("No events found for " + artist_name + " within " + str(st.session_state.radius) + " miles of your location.")
                    m = folium.Map()
                    folium_static(m)
                else:
                    m = map_creator(filtered_coordinates, filtered_cities)
                    folium_static(m)
            else:            
                m = map_creator(event_coordinates, event_cities)
                folium_static(m)

        else:
            st.error("No events found for " + artist_name)

def haversine(coord1, coord2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    # Radius of the Earth in miles
    R = 3959.87433

    # Compute distances along lat and long dimensions
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula to calculate the distance
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def filter_events_by_area(event_coordinates, event_cities, user_location, radius=100): # make radius a slider
    filtered_coords = []
    filtered_cities = []

    for coord, city in zip(event_coordinates, event_cities):
        if haversine(user_location, coord) <= radius:
            filtered_coords.append(coord)
            filtered_cities.append(city)

    return filtered_coords, filtered_cities


def get_user_location():
    # Make a request to the geolocation API
    response = requests.get('http://ip-api.com/json/')
    if response.status_code == 200:
        data = response.json()
        # Extract latitude and longitude from the response
        return data['lat'], data['lon']
    else:
        # Handle the error or return a default location
        st.error('Could not determine your location.')
        return None, None

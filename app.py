import streamlit as st
import requests



category = st.sidebar.selectbox("Choose event details", options=["Map", 
"Table", "View available events by date", "View available artist events by country", "View artist events per month"])

if category == "Map":
    st.title("Map of events")
    st.markdown("This is a map of events in the world")
    st.map()
elif category == "Table":
    st.title("Table of events")
    st.markdown("This is a table of events in the world")
    st.table()
elif category == "View available events by date":
    st.title("View available events by date")
    st.markdown("This is a table of events in the world")
    st.table()
elif category == "View available artist events by country":
    st.title("View available artist events by country")
    st.markdown("This is a table of events in the world")
    st.table()
elif category == "View artist events per month":
    st.title("View artist events per month")
    st.markdown("This is a table of events in the world")
    st.table()
else:
    st.title("Map of events")
    st.markdown("This is a map of events in the world")
    st.map()

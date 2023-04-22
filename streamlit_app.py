from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

#Load the data

import numpy as np
import pandas as pd
import csv

airports =  pd.read_csv('airports.dat', header=None, na_values=['\\N'], dtype=str) #read airports data

#Naming column headers
airports.columns = ["id", "airport", "city", "country", "iata", "icao", "latitude", 
                    "longitude", "altitude", "offset", "dst", "timezone", "type", "source"]

#Cleaning data in the dataframe
airports.drop(['type', 'source'], axis=1, inplace=True) #removing type and source thereby dropping redundant columns 

#Print the airports data
#st.table(airports)  

# Create a world map to show distributions of users 
import folium
from folium.plugins import MarkerCluster

#empty map
world_map= folium.Map(location=(30, 10), zoom_start=1.99, tiles="cartodb positron")
marker_cluster = MarkerCluster().add_to(world_map)
#for each coordinate, create circlemarker of user percent
for i in range(len(airports)):
        lat = airports.iloc[i]['latitude']
        long = airports.iloc[i]['longitude']
        radius=6
        popup_text = """airport : {}<br>
                     country : {}<br>
                     city : {}<br>
                     altitude : {}<br>"""
        popup_text = popup_text.format(airports.iloc[i]['airport'],
                                       airports.iloc[i]['country'],
                                       airports.iloc[i]['city'],
                                       airports.iloc[i]['altitude'],
                                       )
        
        folium.CircleMarker(location = [lat, long], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
#show the map
world_map

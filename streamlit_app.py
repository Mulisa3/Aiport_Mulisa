from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit

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

m = folium.Map(location=[airports.latitude.mean(), airports.longitude.mean()], 
                 zoom_start=3, control_scale=True)

#Loop through each row in the dataframe
for i,row in airports.iterrows():
    #Setup the content of the popup
    iframe = folium.IFrame('altitude:' + str(row["altitude"]))
    
    #Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    
    #Add each row to the map
    folium.Marker(location=[row['latitude'],row['longitude']],
                  popup = popup, c=row['altitude']).add_to(m)

st_data = st_folium(m, width=700)

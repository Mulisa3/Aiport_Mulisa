from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

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



# Create a list of African countries
african_countries = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi',
                     'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros',
                     'Democratic Republic of the Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea',
                     'Eritrea', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau',
                     'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi',
                     'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger',
                     'Nigeria', 'Republic of the Congo', 'Rwanda', 'São Tomé and Príncipe', 'Senegal',
                     'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan',
                     'Swaziland', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']

# Drop rows with countries that are not in Africa
airports = airports[airports['country'].isin(african_countries)]


# Create a list of airports to drop
airports_to_drop = ['Newnan Hospital Heliport', 'Shuttle Landing Facility Airport', 'Burnet Municipal Kate Craddock Field', 'Los Alamitos Army Air Field', 'Nasa Shuttle Landing Facility Airport']

# Drop rows with airports to drop
airports = airports[~airports['airport'].isin(airports_to_drop)]

# Print the updated DataFrame
#airports

#Print the airports data
#airports  
airports1 = airports.groupby('country')['airport'].count().reset_index()


st.write('**Number Of Airports in African Countries**')
#st.table(airports1)

st.bar_chart(airports1, x='country', y= 'airport')


# Create a world map to show distributions of users 
import streamlit as st
import leafmap.foliumap as leafmap
import folium

st.dataframe(airports)

m = leafmap.Map(center=(8.7832, 34.5085), zoom=3)
for index, row in airports.iterrows():
    popup = folium.Popup(f"<strong>Airport:</strong> {row['airport']}<br><strong>Country:</strong> {row['country']}<br><strong>City:</strong> {row['city']}<br><strong>IATA:</strong> {row['iata']}<br><strong>ICAO:</strong> {row['icao']}<br><strong>Timezone:</strong> {row['timezone']}<br><strong>Altitude:</strong> {row['altitude']} m")
    folium.Marker([row['latitude'], row['longitude']], popup=popup).add_to(m)

m.to_streamlit()

import streamlit as st
import pandas as pd
import plotly.express as px

# create a sample dataframe with country names and airport counts

# create a choropleth map using plotly express
fig = px.choropleth(airports1, locations='country', locationmode='country names',
                    color='airport', range_color=[0, max(airports1['airport'])],
                    title='airport by Country')

# set the map projection and center it on Africa
fig.update_geos(projection_type='natural earth', center=dict(lon=8.7832, lat=34.5085), scope = 'comoros', 'madagascar', 'mauritius', 'mayotte', 'reunion', 'zimbabwe')


# display the map in Streamlit
st.plotly_chart(fig)



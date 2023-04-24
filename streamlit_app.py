from collections import namedtuple
import altair as alt
import math
import csv
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import streamlit as st
import folium
import plotly.graph_objs as go
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
import plotly.express as px

"""
# Welcome to Streamlit

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

#Load the airport data

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


# Create a list of airports(that are not in Frica) to drop,this are airports that have incorrect information,e.g.The frrom the airports datafile,it says these airports are in Africa which is not true.
airports_to_drop = ['Newnan Hospital Heliport', 'Shuttle Landing Facility Airport', 'Burnet Municipal Kate Craddock Field', 'Los Alamitos Army Air Field', 'Nasa Shuttle Landing Facility Airport']

# Drop rows with airports to drop
airports = airports[~airports['airport'].isin(airports_to_drop)]


# group the airports by country and count the number of airports in each country
airports1 = airports.groupby('country')['airport'].count().reset_index()



#Load routes data

routes =  pd.read_csv('routes.dat', header=None, na_values=['\\N'], dtype=str) #read routes data

#Naming column headers
routes.columns = ["airline", "airline_id", "source_airport", "source_airport_id", "destination_airport",
                  "destination_airport_id", "codeshare", "stops", "equipment"]
#routes

# Data manipulation and merge dataset(routes.dat and airport.dat) in order to create flight routes map

source_airports = airports[['airport', 'iata', 'icao', 'latitude', 'longitude']]
destination_airports = source_airports.copy()
source_airports.columns = [str(col) + '_source' for col in source_airports.columns]
destination_airports.columns = [str(col) + '_destination' for col in destination_airports.columns]
routes = routes[['source_airport', 'destination_airport']]
routes = pd.merge(routes, source_airports, left_on='source_airport', right_on='iata_source')
routes = pd.merge(routes, destination_airports, left_on='destination_airport', right_on='iata_destination')
#
geometry = [LineString([[routes.iloc[i]['longitude_source'], routes.iloc[i]['latitude_source']], [routes.iloc[i]['longitude_destination'], routes.iloc[i]['latitude_destination']]]) for i in range(routes.shape[0])]
routes = gpd.GeoDataFrame(routes, geometry=geometry, crs='EPSG:4326')

#Dispaly Charts
st.write('**Number Of Airports in African Countries**')
#st.table(airports1)

st.bar_chart(airports1, x='country', y='airport')



# Create a world map to show distributions of airports in Africa
st.write('**A world map that shows the distributions of airports in Africa**')
#st.dataframe(airports)

m = leafmap.Map(center=(8.7832, 34.5085), zoom=3)
for index, row in airports.iterrows():
    popup = folium.Popup(f"<strong>Airport:</strong> {row['airport']}<br><strong>Country:</strong> {row['country']}<br><strong>City:</strong> {row['city']}<br><strong>IATA:</strong> {row['iata']}<br><strong>ICAO:</strong> {row['icao']}<br><strong>Timezone:</strong> {row['timezone']}<br><strong>Altitude:</strong> {row['altitude']} m")
    folium.Marker([row['latitude'], row['longitude']], popup=popup).add_to(m)
    
#Display a map show distributions of airports in Africa
m.to_streamlit()


# Create a new figure
figure = go.Figure()

# Create a trace for each flight route
for i, row in routes.iterrows():
    figure.add_trace(
        go.Scattergeo(
            lat=[row['latitude_source'], row['latitude_destination']],
            lon=[row['longitude_source'], row['longitude_destination']],
            mode='lines',
            line=dict(width=1, color='red'),
            hoverinfo='text',
            text=f"{row['airport_source']} to {row['airport_destination']}",
            name='Flight Route'
        )
    )

# Update the layout of the figure
figure.update_layout(
    title='Flight Routes in Africa',
    geo=dict(
        scope='africa',
        projection_type='natural earth',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)

# Display the figure on Streamlit
st.plotly_chart(figure)


#load airlines data

airlines =  pd.read_csv('airlines.dat', header=None, na_values=['\\N'], dtype=str) #read airlines data

#Naming column headers
airlines.columns = ["id", "airline", "alias", "iata", "icao", "callsign", "country", "active"]

#Cleaning data in the dataframe
airlines.drop(0, axis=0, inplace=True)   # remove id = negative value,thereby dropping redundant rows 

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
airlines = airlines[airlines['country'].isin(african_countries)]


# Create a list of airports to drop,these airports are not in Africa.
airports_to_drop = ['Newnan Hospital Heliport', 'Shuttle Landing Facility Airport', 'Burnet Municipal Kate Craddock Field', 'Los Alamitos Army Air Field', 'Nasa Shuttle Landing Facility Airport']


# Create a filter for selecting the country
countries = airlines['country'].unique()
selected_country = st.sidebar.selectbox('Select a country', countries)

# Create a new dataframe for the selected country
selected_df = airlines[airlines['country'] == selected_country]

# Count the number of active and inactive airlines for the selected country
active_airlines = selected_df[selected_df['active'] == 'Y']['airline'].count()
inactive_airlines = selected_df[selected_df['active'] == 'N']['airline'].count()

# Create the pie chart
fig, ax = plt.subplots()
ax.pie([active_airlines, inactive_airlines], labels=['Active', 'Inactive'], autopct='%1.1f%%')
ax.set_title(f'Active Airlines in {selected_country}')

# Show the pie chart and the filter pop-up
st.pyplot(fig)
st.sidebar.markdown('---')
st.sidebar.markdown(f'Active airlines in **{selected_country}**: {active_airlines}')
st.sidebar.markdown(f'Inactive airlines in **{selected_country}**: {inactive_airlines}')

##############################


# Create a function to plot the pie chart
def plot_pie_chart(country):
    # Create a new dataframe for the selected country
    selected_df = airlines[airlines['country'] == country]

    # Count the number of active and inactive airlines for the selected country
    active_airlines = selected_df[selected_df['active'] == 'Y']['airline'].count()
    inactive_airlines = selected_df[selected_df['active'] == 'N']['airline'].count()

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie([active_airlines, inactive_airlines], labels=['Active', 'Inactive'], autopct='%1.1f%%')
    ax.set_title(f'Active Airlines in {country}')
    st.pyplot(fig)

# Get the unique countries in the data
countries = airlines['country'].unique()

# Display the pie chart and filter for each country
for country in countries:
    st.header(f"{country}")
    plot_pie_chart(country)
    st.sidebar.selectbox('Select a country', countries)


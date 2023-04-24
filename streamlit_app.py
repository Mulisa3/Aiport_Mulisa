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
# African Airports Explorer

Air travel infrastructure plays a critical role in driving economic development, facilitating international trade and travel, and connecting people and businesses across the world. In Africa, however, air travel infrastructure remains underdeveloped and inadequate, hindering the continent's ability to fully participate in the global economy and limiting opportunities for growth and development.

To better understand the state of air travel infrastructure in Africa, we have developed a dashboard that visualizes data on the distribution of airports and airline activity across the continent. Our dashboard includes a variety of charts and visualizations, including a bar graph of the total number of airports in each African country, a pie chart that shows the distribution of active and inactive airlines in each country, and an interactive map that displays the location of airports across Africa and the routes between them.
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



# Create a world map to show distributions of airports in Africa

#st.dataframe(airports)

m = leafmap.Map(center=(8.7832, 34.5085), zoom=3)
for index, row in airports.iterrows():
    popup = folium.Popup(f"<strong>Airport:</strong> {row['airport']}<br><strong>Country:</strong> {row['country']}<br><strong>City:</strong> {row['city']}<br><strong>IATA:</strong> {row['iata']}<br><strong>ICAO:</strong> {row['icao']}<br><strong>Timezone:</strong> {row['timezone']}<br><strong>Altitude:</strong> {row['altitude']} m")
    folium.Marker([row['latitude'], row['longitude']], popup=popup).add_to(m)
    
#Display a map show distributions of airports in Africa
st.markdown("<h1 style='font-size:18px;'>A world map that shows the distributions of airports in Africa</h1>", unsafe_allow_html=True)
"""The interactive map above provides a detailed view of the location of airports across the continent. The map highlights the fact that many of the major airports in Africa are in or near major cities, such as Johannesburg in South Africa, Lagos in Nigeria, and Cairo in Egypt. This map wallow users to zoom in and out and click on individual airports to see more detailed information about their location, activity, and time zone.A user can also be able to search and measure the distance between airports of interest. By visualizing the distribution of airports across the continent, this map will provide users with a sense of how air travel infrastructure is distributed across different regions of Africa."""
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
    title='Flight Routes In Africa',
    title_font_size=18,  # set the font size of the title to 24
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
"""This African map shows flight routes between different countries and cities. This map uses the users to explore the connectivity of different cities and regions across the continent. By visualizing the network of flight routes in Africa, this map will help users understand the importance of different cities and airports in the continent's air travel infrastructure. The map also shows that there are significant gaps in air travel infrastructure in some regions of the continent, particularly in central Africa."""

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

###################################################################!#################
#Dispaly Charts
#st.table(airports1)

st.write(
    f"<h1 style='font-size: 18px; font-weight: bold;'>Number of Airports by Country</h1>",
    unsafe_allow_html=True,
)
"""This bar chart shows the total number of airports in each African country. This chart will provide users with a broad overview of the distribution of airport infrastructure across the continent and will highlight countries that have relatively low numbers of airports and may benefit from investment and development."""
st.bar_chart(airports1, x='country', y='airport')
###############################################################!################################

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
"""A pie chart below shows the percentage of active and inactive airlines in each African country. This chart provides users with a sense of the level of competition and activity in different regions of the continent and will highlight countries where more investment and development may be needed to stimulate growth in the air travel sector. A user can use the filter on the top left corner to select the country and get its airline active status displayed on the pie chart."""
# Create the pie chart
fig, ax = plt.subplots()
ax.pie([active_airlines, inactive_airlines], labels=['Active', 'Inactive'], autopct='%1.1f%%')
ax.set_title(f'Active Airlines in {selected_country}', fontsize=8)

# Show the pie chart and the filter pop-up
st.pyplot(fig)
st.sidebar.markdown('---')
st.sidebar.markdown(f'Active airlines in **{selected_country}**: {active_airlines}')
st.sidebar.markdown(f'Inactive airlines in **{selected_country}**: {inactive_airlines}')


####################################!##############


# Count the number of airports for each country
country_counts = airports['city'].value_counts()

# Get the countries with at least 20 airports
at_least_20_airports = country_counts[country_counts >= 2]

# Get the top ten countries by number of airports
top_ten_countries = at_least_20_airports[:10]

# Create the vertical bar chart
fig, ax = plt.subplots()
ax.bar(top_ten_countries.index, top_ten_countries.values)
ax.set_xlabel('City')
ax.set_ylabel('Number of Airports')
ax.set_title('Top Ten Cities with At Least 2 Airports', fontweight='bold', fontsize=10)
plt.xticks(rotation=90)

"""A bar chart below shows the top ten cities with the highest number of airports in Africa. This chart will provide users with a sense of the importance of different cities in the continent's air travel infrastructure."""
# Display the chart on a Streamlit app
st.pyplot(fig)

""" """

"""Overall, our dashboard will provide users with a comprehensive overview of the state of air travel infrastructure in Africa and will highlight areas where investment and development could be particularly beneficial. By combining multiple visualizations and charts, the dashboard will enable users to explore different aspects of the air travel sector in Africa, and gain insights into the current state of the industry. Whether users are investors, policymakers, or researchers, this dashboard will provide a valuable resource for understanding the opportunities and challenges facing the air travel sector in Africa, and for identifying areas where intervention and support may be needed to drive growth and development."""



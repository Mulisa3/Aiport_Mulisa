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
#airports  
airports1 = airports.groupby('country')['airports'].count().reset_index()

st.write('My column')
st.table(airpots1)

st.bar_chart(airports1, x='country', y= 'airports')

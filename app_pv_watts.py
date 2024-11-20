import json, requests
from urllib.request import urlopen
import pandas as pd
import streamlit as st
import sys

# input parameters for terminal run Austin lat/long: 30.26/-97.74
#lat = float(sys.argv[1])
#long = float(sys.argv[2])
#size = float(sys.argv[3])


# input parameters for app run default is for Austin
lat = st.sidebar.slider(
    'Latitude:',
    -90.0, 90.0, (30.26)
) 
long = st.sidebar.slider(
    'Longitude',
    -180.0, 180.0, (-97.74)
) 
size = st.sidebar.slider(
    'Size of PV array:',
    0.0, 100.0, (50.0)
)


# url generator
nrel_api_key = 'kVTh5O88nbYohgldbB92JC17TL4UzxwauQo1x2Ha'
url = 'https://developer.nrel.gov/api/pvwatts/v6.json?api_key=%s&lat=%s&lon=%s&system_capacity=%s&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10' % (nrel_api_key, lat, long, size)


## add catch for bad locations and print output for app
if(requests.get(url).status_code == 200):
    response = urlopen(url)
    pv_out = json.loads(response.read())
    location = pv_out['station_info']['state']
    gen = round(pv_out['outputs']['ac_annual'])

    ## print statement for terminal run
    #print(f'A {size} kW solar PV array in {location} should output about {gen} kWh per year!')
    ## print statement for app run
    st.write('A %s kW solar PV array in %s should output about %s kWh per year!' % (size, location, gen))

else:
    ## print statement for terminal run
    #print('You appear to have chosen a location without data! Maybe try again?')
    ## print statement for app run
    st.write('You appear to have chosen a location without data! Maybe try again?')

# plot the location data on a map with streamlit!
map_data = pd.DataFrame(data={'lat': float(lat), 'lon': float(long)}, index=[0])
st.map(map_data)
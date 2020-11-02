#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#Reading the html
torontodf=pd.read_html("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
print("html is read")


# In[3]:


#Toronto df has list of all the tables present in the html. Extract the first one.
torontodf=torontodf[0]


# In[4]:


# remove the rows where Borough=='Not assigned' 
torontodf=torontodf[torontodf.Borough != 'Not assigned']


# In[5]:


#check if 'Not assigned' exists in Neighborhood column'
df=torontodf.Neighbourhood=='Not assigned'
if "True" in df:
    print('Element exists in Dataframe')
else:
     print('Element doesnt exist in Dataframe')


# In[6]:


#print the number of rows in the df
torontodf.shape[0]


# ### Adding the Latitudes and Longitudes for each Postal Code

# In[7]:


#!conda install -c conda-forge geocoder --yes
get_ipython().system('pip install geocoder')
#import geocoder # import geocoder

import geocoder
from geopy.geocoders import Nominatim
get_ipython().system('pip install pgeocode')
import pgeocode


# In[8]:


nomi = pgeocode.Nominatim('CA')
for index, row in torontodf.iterrows(): 
 location=nomi.query_postal_code(row['Postal Code'])
 torontodf.at[index,'Latitude'] = location.latitude
 torontodf.at[index,'Longitude']=location.longitude


# In[9]:


toronto_data = torontodf[torontodf['Borough'].str.contains('Toronto')].reset_index(drop=True)
toronto_data_clustering=toronto_data.drop('Borough',axis=1)
toronto_data_clustering=toronto_data_clustering.drop('Neighbourhood',axis=1)
toronto_data_clustering=toronto_data_clustering.drop('Postal Code',axis=1)


# In[10]:


from sklearn.cluster import KMeans

# set number of clusters
kclusters = 4

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(toronto_data_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 


# In[11]:


toronto_data["kmeans_label"]=kmeans.labels_
toronto_data


# In[12]:


#initialise the default latitude and longitude
location=nomi.query_postal_code("M5A")
latitude = location.latitude
longitude = location.longitude


# In[13]:


get_ipython().system('pip install folium')
import folium # map rendering library
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(toronto_data['Latitude'], toronto_data['Longitude'], toronto_data['Neighbourhood'], toronto_data['kmeans_label']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# In[ ]:





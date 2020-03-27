# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 10:41:03 2020

@author: Lenovo
"""
import pandas as pd
import geopandas as gpd
import folium
import json
import branca

import branca.colormap as cm
from folium.features import GeoJson, GeoJsonTooltip

# Import the GEOJson and csv file
with open("C:/Users/Lenovo/Documents/Datasets/Geospatial Data/indonesia_province.geojson") as json_file:
    idn = gpd.GeoDataFrame.from_features(json.load(json_file))
idn.crs = "epsg:4326"

province = pd.read_csv("C:/Users/Lenovo/Documents/Datasets/Geospatial Data/Indonesia_Province.csv")
province.rename(columns = {"Code" : "KODE", "Province" : "Provinsi"}, inplace = True)

test = province.set_index("KODE").iloc[:, 0:4]

# Merge the idn and province dataframe
IND = pd.merge(idn, province, how="inner", on="KODE")

# Create a colormap
linear = cm.linear.viridis.scale(
    province["area(Km2)"].min(),
    province["area(Km2)"].max())

# Create a white image of 4 pixels, and embed it in a url.
white_tile = branca.utilities.image_to_url([[1, 1], [1, 1]])

# Create a map object
map_file = folium.Map(location =[0.8, 113],
                      tiles = white_tile, attr='white tile',
                      zoom_start = 6)

# Make a tooltip
tooltip = GeoJsonTooltip(
    fields = ["NAME_1", "area(Km2)"],
    aliases = ["Province Name :", "Area(Km2) :"],
    localize = True,
    sticky = True,
    labels = True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """)

# Add to the map
geo = folium.GeoJson(IND,
                     style_function = lambda x: {
                         "fillColor": linear(x["properties"]["area(Km2)"]),
                         "color" : "black",
                         "fillOpacity" : 0.75},
                     tooltip = tooltip).add_to(map_file)

linear.add_to(map_file) # if you want show the color bar

# Save the map to HTML
map_file.save("choroplethMap_Indonesia.html")
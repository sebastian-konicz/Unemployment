from pathlib import Path
import pandas as pd
# import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import time
from folium import IFrame
import json
import requests
import altair as alt
from branca.utilities import _locations_mirror
from folium.features import *


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading map data
    geo_path = r'\data\geo\admin\Powiaty.shp'
    map = gpd.read_file(project_dir + geo_path)

    # restricting dataframe
    map = map[['JPT_KOD_JE', 'geometry']]
    map['JPT_KOD_JE'] = map['JPT_KOD_JE'].apply(lambda x: str(x))

    print(map.dtypes)
    # loading unemployment data
    data_path = r'\data\interim\unemployment.xlsx'
    data = pd.read_excel(project_dir + data_path)

    # restricting dataframe
    data = data[['teryt', 'pow_name', 'unempl_%']]

    # transforming teryt column
    data['teryt'] = data['teryt'].apply(lambda x: '0' + str(x) if len(str(x)) < 4 else str(x))

    # merging dataframes
    map = map.merge(data, left_on='JPT_KOD_JE', right_on='teryt')

    print(map.head(10))

    # simplifying geometry
    map.geometry = map.geometry.simplify(0.005)

    # changing data to GeoJSON
    map_geo = map.to_json()

    # parsing geoJSON
    geo_parsed = json.loads(map_geo)
    with open('geo_parsed.json', 'w') as json_file:
        json.dump(geo_parsed, json_file)
    # print(geo_parsed['type'])
    # print(json.dumps(geo_parsed, indent=4, sort_keys=True))

    # creating folium map
    map_graph = folium.Map([52, 19], zoom_start=7)

    # print(map_geo)

    choropleth = folium.Choropleth(geo_data=map_geo,
                      name='choropleth',
                      data=data,
                      columns=['teryt', 'unempl_%'],
                      key_on='feature.properties.JPT_KOD_JE',
                      bins=9,
                      fill_color='YlOrRd',
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      highlight=True,
                      legend_name="Stopa bezrobocia w procentach").add_to(map_graph)


    # # VINCENT

    url = ("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data")
    vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
    # print(vis1)
    # vincent = folium.Vega(vis1, width=450, height=250)
    # # add_child(vincent)
    #
    # html text in tooltip
    html = """
            <b>dupa</b><br>
            """


    # html style
    style = "background-color: white; " \
                 "color: #333333; " \
                 "font-family: arial; " \
                 "font-size: 16px; " \
                 "padding: 10px;"

    # load GEOJSON, but don't add it to anything
    temp_geojson = folium.GeoJson(map_geo)

    print((folium.Vega(vis1, width=450, height=250)))

    # TOOLTIP LAYER
    tooltip_layer = folium.FeatureGroup(name='tooltip', show=False)

    # iterate over GEOJSON, style individual features, and add them to FeatureGroup
    for feature in temp_geojson.data['features']:
        style_function = lambda x: {'fillColor': '#ffffff',
                                    'color': '#000000',
                                    'fillOpacity': 0.1,
                                    'weight': 0.1}

        # GEOJSON layer consisting of a single feature
        temp_layer = folium.GeoJson(feature, style_function=style_function)

        # lambda to add HTML
        foo = lambda name, source: f"""
         <p> Nazwa:               {name}</p><br>
         <p> Stopa berobocia (%): {source}</p>
            """

        folium.map.Tooltip(text=foo(feature["properties"]["pow_name"], feature["properties"]["unempl_%"]), style=style, sticky=True).add_to(temp_layer)
        # consolidate individual features back into the main layer
        temp_layer.add_to(tooltip_layer)

    # add main layer to folium.Map object
    tooltip_layer.add_to(choropleth)

    # saving map
    print('saving map')
    map_graph.save(project_dir + r'\data\final\unemployment_map_tooltip.html')
    map_graph.save(project_dir + r'\templates\unemployment_map_tooltip.html')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')



if __name__ == "__main__":
    main()
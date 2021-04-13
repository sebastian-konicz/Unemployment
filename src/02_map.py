from pathlib import Path
import pandas as pd
# import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import time

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

    # # prepare the customised text
    # tooltip_text = []
    # for idx in range(len(data)):
    #     tooltip_text.append(str(data['pow_name'][idx]) + ' ' + str(data['unempl_%'][idx]) + '%')
    # tooltip_text
    #
    # # append a tooltip column with customised text
    # for idx in range(len(tooltip_text)):
    #     print(map_geo)
    #     map_geo['features'][idx]['properties']['tooltip'] = tooltip_text[idx]

    # creating folium map
    map_graph = folium.Map([52, 19], zoom_start=7)

    choropleth = folium.Choropleth(geo_data=map_geo,
                      name='choropleth',
                      data=data,
                      columns=['teryt', 'unempl_%'],
                      key_on='feature.properties.JPT_KOD_JE',
                      fill_color='YlOrRd',
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      legend_name="Stopa bezrobocia w procentach"
                                   ).add_to(map_graph)

    # choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['pow_name'], labels=False))

    # adding labels to map
    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}

    tooltip = folium.features.GeoJson(
        map_geo,
        style_function=style_function,
        control=False,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['pow_name', 'unempl_%'],
            aliases=['nazwa', 'stopa bezrobocia (%)'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    map_graph.add_child(tooltip)
    map_graph.keep_in_front(tooltip)
    folium.LayerControl().add_to(map_graph)

    # saving map
    print('saving map')
    map_graph.save(project_dir + r'\data\final\density.html')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
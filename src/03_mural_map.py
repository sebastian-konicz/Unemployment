from pathlib import Path
import pandas as pd
import base64
from folium import IFrame
import folium
import time
from IPython.display import display

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading mural data
    data_path = r'\data\interim\murale_ursynow.xlsx'
    data = pd.read_excel(project_dir + data_path)

    print(data)

    lat = data['lat']
    lng = data['lng']
    name = data['name']
    photo = data['photo']


    # creating folium map
    map_graph = folium.Map([52.145259, 21.051619], zoom_start=13)

    # encoded = base64.b64encode(open('mypict.jpg', 'rb').read())




    # Plot Markers
    for lat, lng, name, photo in zip(lat, lng, name, photo):
        # photo path
        photo_path = project_dir + r'\data\murale_img\{photo_path}.jpg'.format(photo_path=photo)
        # marker setting
        encoded = base64.b64encode(open(photo_path, 'rb').read())
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode('UTF-8')), width=400, height=350)
        popup = folium.Popup(iframe, max_width=800)

        folium.Marker(location=[lat, lng],
                      tooltip=html, popup=popup,
                      # popup='<img src={path}>'.format(path=photo_path),
                      icon=folium.Icon(color='blue', icon='camera', prefix='fa')).add_to(map_graph)


    # choropleth = folium.Choropleth(geo_data=map_geo,
    #                   name='choropleth',
    #                   data=data,
    #                   columns=['teryt', 'unempl_%'],
    #                   key_on='feature.properties.JPT_KOD_JE',
    #                   fill_color='YlOrRd',
    #                   fill_opacity=0.7,
    #                   line_opacity=0.2,
    #                   legend_name="Stopa bezrobocia w procentach"
    #                                ).add_to(map_graph)

    # choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['pow_name'], labels=False))

    # # adding labels to map
    # style_function = lambda x: {'fillColor': '#ffffff',
    #                             'color': '#000000',
    #                             'fillOpacity': 0.1,
    #                             'weight': 0.1}
    #
    # tooltip = folium.features.GeoJson(
    #     map_geo,
    #     style_function=style_function,
    #     control=False,
    #     tooltip=folium.features.GeoJsonTooltip(
    #         fields=['pow_name', 'unempl_%'],
    #         aliases=['nazwa', 'stopa bezrobocia (%)'],
    #         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    #     )
    # )
    # map_graph.add_child(tooltip)
    # map_graph.keep_in_front(tooltip)
    # folium.LayerControl().add_to(map_graph)

    # saving map
    print('saving map')
    map_graph.save(project_dir + r'\data\final\mural_map.html')
    display(map_graph)
    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')


if __name__ == "__main__":
    main()
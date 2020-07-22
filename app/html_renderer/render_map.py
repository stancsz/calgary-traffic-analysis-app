import folium as folium
import dash_html_components as html
from folium import plugins, Popup
from database.geo_json import get_geo_df, get_geo_json_form_df, get_geo_json


def get_map(df, the_geom_col):
    # print(df.columns, the_geom_col)
    yyc_coordinates = (51.121191, -114.048240)
    yyc_map = folium.Map(location=yyc_coordinates, zoom_start=13)
    src_geo_df = get_geo_df(df, the_geom_col)
    # print(src_geo_df)
    for index, values in enumerate(src_geo_df):
        # print(index, values)
        geojson_polygon = get_geo_json_form_df(src_geo_df, index)
        lines = [geojson_polygon.coordinates]
        folium.PolyLine(lines, weight=12, color='red', popup=Popup('Max volume location')).add_to(yyc_map)
    return yyc_map


def generate_html(map_object):
    map_object.save('map.html')


def render_volume_map_html(df, the_geom_col):
    generate_html(get_map(df, the_geom_col))
    render = html.Div([
        html.H1('Traffic Analysis Map'),
        html.Iframe(id='map', srcDoc=open('map.html').read(), width='100%', height=600)
    ])
    return render


def render_incident_map(df):
    """
    takes a incident dataframe, which must have "Longitude", "Latitude" or else it will fail
    :return:
    """
    # df = db.get_dataframe_from_mongo('db_incident', 'traffic_incidents')
    yyc_coordinates = (51.049999, -114.066666)
    yyc_map = folium.Map(location=yyc_coordinates, zoom_start=10)
    src_geo_df = df[["longitude", "latitude"]]
    coordinates = []
    for index, value in src_geo_df.iterrows():
        coordinates.append([value[1], value[0]])
    # print(coordinates)
    # geo_json = get_geo_json(coordinates)
    yyc_map.add_child(plugins.HeatMap(coordinates, width=1, height=1, radius=13))
    yyc_map.save('map.html')

    render = html.Div([
        html.H1('Traffic Analysis Map'),
        html.Iframe(id='map', srcDoc=open('map.html').read(), width='100%', height=600)
    ])
    return render


def main():
    return


if __name__ == '__main__':
    main()

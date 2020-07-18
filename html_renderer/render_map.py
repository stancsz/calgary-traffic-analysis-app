import folium as folium
import dash_html_components as html

from database.geo_json import get_geo_df, get_geo_json_form_df


def get_map(df, the_geom_col):
    yyc_coordinates = (51.049999, -114.066666)
    yyc_map = folium.Map(location=yyc_coordinates, zoom_start=10)
    src_geo_df = get_geo_df(df, the_geom_col)
    for index, values in enumerate(src_geo_df):
        geojson_polygon = get_geo_json_form_df(src_geo_df, index)
        lines = [geojson_polygon.coordinates]
        folium.PolyLine(lines).add_to(yyc_map)
    return yyc_map


def generate_html(map_object):
    map_object.save('map.html')


def render_map_html(df, the_geom_col):
    generate_html(get_map(df, the_geom_col))
    render = html.Div([
        html.H1('Traffic Analysis Map'),
        html.Iframe(id='map', srcDoc=open('map.html').read(), width='100%', height=600)
    ])
    return render


def main():
    get_map()


if __name__ == '__main__':
    main()

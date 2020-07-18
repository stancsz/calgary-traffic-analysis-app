import folium as folium
import dash_html_components as html


def get_map():
    yyc_coordinates = (51.049999, -114.066666)
    yyc_map = folium.Map(location=yyc_coordinates, zoom_start=10)
    return yyc_map


def generate_html(map):
    map.save('map.html')


def render_map_html():
    generate_html(get_map())
    render = html.Div([
        html.H1('Traffic Analysis Map'),
        html.Iframe(id='map', srcDoc=open('map.html').read(), width='100%', height=600)
    ])
    return render


def main():
    get_map()


if __name__ == '__main__':
    main()

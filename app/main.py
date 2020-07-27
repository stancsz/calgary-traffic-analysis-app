"""
plot documentation: https://dash.plot.ly/urls
"""
import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from database import db
from database.db import get_dataframe_from_db_by_year, ingest_data, sort_dataframe_by
from database.db_index import get_index, get_status
from html_renderer.render_graph import render_graph
from html_renderer.render_html import get_project_demo_page
from html_renderer.render_map import render_volume_map_html, render_incident_map
from html_renderer.render_table import render_dataframe
from plot_data.compute_plot_data import compute_plot_data

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
csv_path = '../csv'
df1, df2 = ingest_data(csv_path)  # ingest all csv data into mongo database

"""
Quick Lookup for collection and db names
Collection:  '2017_traffic_volume_flow'  is imported in DB: 'db_volume'
Collection:  'traffic_incidents'  is imported in DB: 'db_incident'
Collection:  'trafficflow2016_opendata'  is imported in DB: 'db_volume'
Collection:  'traffic_incidents_archive_2017'  is imported in DB: 'db_incident'
Collection:  'traffic_incidents_archive_2016'  is imported in DB: 'db_incident'
Collection:  'traffic_volumes_for_2018'  is imported in DB: 'db_volume'
"""

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Traffic Analysis", className="display-4"),
        html.Hr(),
        html.P(
            "ENSF 592 Term Project \n " + str(datetime.date.today()), className="lead"
        ),
        dcc.Dropdown(
            id='db-type',
            options=[
                {'label': 'Traffic Volume', 'value': 'volume'},
                {'label': 'Incidents', 'value': 'incident'},
            ],
            # value='volume',
            placeholder="(Select a data type)",
            searchable=True,
        ),
        dcc.Dropdown(
            id='data-year',
            options=[
                {'label': '2016', 'value': '2016'},
                {'label': '2017', 'value': '2017'},
                {'label': '2018', 'value': '2018'},
            ],
            # value='2016',
            placeholder="(Select a year)",
            searchable=True,
        ),
        dbc.Nav(
            [
                # dbc.NavLink("Traffic Vol", href="/page-1", id="page-1-link"),
                # dbc.NavLink("Year", href="/page-2", id="page-2-link"),
                dbc.NavLink("Read", href="/page-3", id="page-3-link"),
                dbc.NavLink("Sort", href="/page-4", id="page-4-link"),
                dbc.NavLink("Analysis", href="/page-5", id="page-5-link"),
                dbc.NavLink("Map", href="/page-6", id="page-6-link"),
            ],
            vertical=True,
            pills=True,
        ),
        dbc.Alert(
            'Status',
            id='load-status-bar',
            color='success',
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(3, 7)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    """
    toggle active links toggles the active link as a callback to make the active link stay active
    :param pathname: the path for the http request
    :return: return a list of variables that contains the active states for the tabs.
    """
    if pathname == "/":
        # Treat page 1 as the homepage / index
        # return True, False, False, False, False, False
        return False, False, False, False
    return [pathname == f"/page-{i}" for i in range(3, 7)]


@app.callback([Output("page-content", "children"), Output("load-status-bar", "children")],
              [Input("url", "pathname"), Input("db-type", "value"), Input("data-year", "value")])
def render_page_content(pathname, type_input, year_input):
    """
    render page content renders page based on the http path. Using callback inputs and outputs,
    this function gets the data from db type or year type. which then is passed to corresponding functions for
    implementing further progrom logics.
    :param pathname: the path for the http request
    :param type_input:
    :param year_input:
    :return:
    """
    return_status = get_status(pathname)
    if pathname in ["/", "/page-1"]:
        return_html = get_project_demo_page()
        return return_html, return_status
    elif pathname == "/page-2":
        return html.P(""), return_status
    elif pathname == "/page-3":
        # if inputs are invalid, prompt a message
        inputs = get_index(type_input, year_input)
        if inputs == -1:
            return html.P("Please enter valid values"), [""]
        # process logics to get the right dataframe
        df = get_dataframe_from_db_by_year(type_input, int(year_input))
        return render_dataframe(df), return_status
    elif pathname == "/page-4":
        inputs = get_index(type_input, year_input)
        if inputs == -1:
            return html.P("Please enter valid values"), [""]
        df_in = get_dataframe_from_db_by_year(type_input, int(year_input))
        df = sort_dataframe_by(df_in, type_input)
        return render_dataframe(df), return_status
    elif pathname == "/page-5":
        return render_graph(df1, df2), return_status
    elif pathname == "/page-6":
        # if inputs are invalid, prompt a message
        # inputs = get_index(type_input, year_input)
        # if inputs == -1:
        #     return html.P("Please enter valid values"), [""]
        # process logics to get the right dataframe
        # print(type_input, int(year_input))
        df = get_dataframe_from_db_by_year(type_input, int(year_input))
        if type_input == 'volume':
            # to render a volume map
            item = df[df.volume == df.volume.max()]
            return_render = render_volume_map_html(item, 'the_geom')
        else:
            # to render a incident map
            # df = df.groupby('domain')['ID'].nunique()
            return_render = render_incident_map(df)
        return return_render, return_status
    # If the user tries to reach a different page, return a 404 message
    # else:
    #     return dbc.Jumbotron(
    #         [
    #             html.H1("404: Not found", className="text-danger"),
    #             html.Hr(),
    #             html.P(f"The pathname {pathname} was not recognised..."),
    #         ], return_status
    #     )


if __name__ == "__main__":
    app.run_server(port=8888)

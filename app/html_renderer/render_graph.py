from datetime import datetime

import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from plot_data.compute_plot_data import compute_plot_data


def render_graph(df1, df2):
    """
    render graphs based on two dataframe, df1 for volume and df2 for incidents.
    compute html rendered code to the function caller.
    :param df1:volume df
    :param df2: incidents df
    :return:
    """
    x1, y1, x2, y2 = compute_plot_data(df1, df2)

    x2=x2[:3]
    y2=y2[:3]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1,
                             mode='lines',
                             name='lines'))

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=x2, y=y2,
                              mode='lines+markers',
                              name='lines+markers'))

    # fig.show()
    render = \
        html.Div([
            html.Div([
                html.H1("Volume Plot"),
                dcc.Graph(
                    id='render-graph',
                    figure=fig
                )
             ]),
            html.Div([
                html.H1("Incidents Plot"),
                dcc.Graph(
                    id='render-graph',
                    figure=fig2
                )
            ])
        ])
    return render

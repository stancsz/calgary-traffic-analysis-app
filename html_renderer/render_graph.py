import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html


def generate_graph_dataframe_dummy():
    """
    generate a dummy dataframe to test graph render
    :return:
    """
    df = px.data.gapminder().query("country=='Canada'")
    # print(df)
    return df


def render_graph(df_input, x_axis, y_axis, graph_title):
    fig = px.line(df_input, x=x_axis, y=y_axis, title=graph_title)
    # fig.show()
    render = html.Div([
        dcc.Graph(
            id='render-graph',
            figure=fig
        )
    ])
    return render

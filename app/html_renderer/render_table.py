import dash_table
import dash_html_components as html


def render_dataframe(df):
    """
    renders tabular table from input dataframe
    :param df: dataframe to be rendered
    :return: the html code that contains the html code for the rendered table
    """
    render_html_table = dash_table.DataTable(
        id='table',
        columns=[{"name": i.replace("_", " ").title(), "id": i} for i in df.columns],
        data=df.to_dict('rows'),
        style_cell={'textAlign': 'left',
                    'width': '100%',
                    'max-width': '500px',
                    'overflow-x': 'wrap'
                    },
        page_size=22,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
    )
    render = html.Div([
        html.H3('Data'),
        render_html_table
    ])
    return render


def main():
    return


if __name__ == '__main__':
    main()

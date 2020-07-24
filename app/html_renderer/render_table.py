import dash_table
import dash_html_components as html


def render_dataframe(df):
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
    # database.ingest_data('../csv')  # Note that ingest data only need to run once
    # data = database.get_dataframe_from_mongo('db_volume', 'trafficflow2016_opendata')
    # """
    # A list of possible collections & dbs
    #     Collection:  '2017_traffic_volume_flow'  is imported in DB: 'db_volume'
    #     Collection:  'traffic_incidents'  is imported in DB: 'db_incident'
    #     Collection:  'trafficflow2016_opendata'  is imported in DB: 'db_volume'
    #     Collection:  'traffic_incidents_archive_2017'  is imported in DB: 'db_incident'
    #     Collection:  'traffic_incidents_archive_2016'  is imported in DB: 'db_incident'
    #     Collection:  'traffic_volumes_for_2018'  is imported in DB: 'db_volume'
    # """
    # print(data)


if __name__ == '__main__':
    main()

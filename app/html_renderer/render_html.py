import dash_html_components as html


def get_project_demo_page():
    """
    generate renders of the html content for the welcome page
    :return: rendered html code containing the welcome page info
    """
    render_html = html.Div([
        html.H1('Welcome to ENSF 592 Term Project Demo'),
        html.H2('Presentation Topics and Presenter'),
        html.P('Data - Burak Gulseren'),
        html.P('Plot - Sarang Kumar'),
        html.P('Others - Stan Chen'),
        html.H3('(Select a data type and year to continue)'),

    ])
    return render_html


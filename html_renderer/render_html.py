import dash_html_components as html


def get_project_demo_page():
    render_html = html.Div([
        html.H1('Welcome to ENSF 592 Term Project Demo'),
        html.H2('Presentation topics and presenter:'),
        html.P('Data - Burak Gulseren'),
        html.P('Plot - Sarang Kumar'),
        html.P('Others - Stan Chen')
    ])
    return render_html


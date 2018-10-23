# Import supporting lib
import dash
import dash_core_components as dcc
import dash_html_components as html


# Boostrap CSS.
#app.config['suppress_callback_exceptions']=True

app = dash.Dash()

app.css.append_css(
    {'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})


app.layout = html.Div(
    html.Div([
        html.Div([
            html.H1(children='Dash Test'),
            html.Img(
                src="http://goo.gl/images/Lb1hG7",
                className = 'three columns',
                style={'float':'right',
                'position':'relative'}),

            html.Div(children='''
                Dash: A web application framework for Python.
            ''')
        ],className="row"),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Data Visualization/bar',
                            'xaxis': dict(
                            title= 'x axis',
                            size = 25),
                            'yaxis': dict(
                            title= 'y axis',
                            size=25
                            )}

                        })
            ], className='six columns'),
            html.Div([
                dcc.Graph(
                    id='example-graph-2',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Data Visualization/line',
                            'xaxis': dict(
                            title= 'x axis',
                            size = 25),
                            'yaxis': dict(
                            title= 'y axis',
                            size=25
                            )}

                        })
                    ],className='six columns')
    ],className='row')
]))

if __name__ == '__main__':
    app.run_server(debug=True)

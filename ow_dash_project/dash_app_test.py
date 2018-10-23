# Import supporting lib
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

# Boostrap CSS.
#app.config['suppress_callback_exceptions']=True

app = dash.Dash()

image_filename = '/Users/omar/DB/om81/ow_dash_project/ow.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.css.append_css(
    {'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})


app.layout = html.Div(
    html.Div([
        html.Div([
            html.H1(children='Dash Test'),
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                className = 'three columns',
                style={
                    'height' : '25%',
                    'width' : '25%',
                    'float' : 'right',
                    'position' : 'relative',
                    'padding-top' : -50,
                    'padding-right' : 10
                }),

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

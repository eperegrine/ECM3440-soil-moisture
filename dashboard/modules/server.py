"""The web server for the dashboard"""

from typing import Callable
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

def prepare_app():
    """Start the app"""
    dashboard = Dash(__name__)

    fig = px.line(pd.DataFrame({'soil_moisture':[0],'time':[0]}), x='time', y='soil_moisture')

    dashboard.layout = html.Div(children=[
        html.H1(children='A simple chart'),
        dcc.Graph(id='soil-moisture-graph',figure=fig),
        dcc.Interval(
            id='interval-component',
            interval=2*1000, # in milliseconds
            n_intervals=0
        )
    ])
    return dashboard

def start_server(get_moisture: Callable[[], list[int]]):
    """Start the web app"""
    app = prepare_app()


    @app.callback(Output('soil-moisture-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
    def update_graph_live(_):
        data = get_moisture()
        time_values = [count for count, _ in enumerate(data)]
        data_frame = pd.DataFrame({ 'soil_moisture': data, 'time':time_values})
        fig = px.line(data_frame,  y='soil_moisture',  x='time')
        return fig

    app.run_server(debug=False,host='0.0.0.0',port=5001)

""" The main dashboard to view the sensor """

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

def prepare_app():
    """Start the app"""
    dashboard = Dash(__name__)

    data_frame = pd.DataFrame({'soil_moisture':[12.0, 14.6, 13.2, 14.4],'time':[0,1,2,3]})

    fig = px.bar(data_frame, x='time', y='soil_moisture')

    dashboard.layout = html.Div(children=[
        html.H1(children='A simple chart'),
        dcc.Graph(id='soil-moisture-graph',figure=fig)
    ])
    return dashboard

if __name__ == '__main__':
    app = prepare_app()

    app.run_server(debug=False,host='0.0.0.0',port=8080)

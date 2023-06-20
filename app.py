import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import requests
import json
import time
from flask import session

app = Dash(__name__, use_pages=True)
server = app.server

'''
    dcc.Interval(
         id='interval',
         interval=1 * 36000000,
         n_intervals=0),
    '''

app.layout = html.Div([
    dcc.Store(id='store'),
    dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Convenios", href='/convenios'),
                    dbc.DropdownMenuItem('Movilidad académica',
                                         href="/movilidad-estudiantil"),
                ],
                nav=True,
                in_navbar=True,
                label="Relaciones interinstitucionales",
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Proyectos de extensión", href='/presentacion-propuestas-y-cotizaciones-de-estudios'),
                    dbc.DropdownMenuItem(
                        "Alianzas, redes, convenios", href='/alianzas-redes-convenios-y-movilidad-de-investigacion'),
                ],
                nav=True,
                in_navbar=True,
                label="Extensión, Innovación y Propiedad Intelectual",
            ),

        ],
        brand="Prig Data App",
        brand_href="/convenios",
        color="light",
        dark=False,
    ),

    dash.page_container
])

'''
@callback(
    Output("store", "data"),
    Input('interval', 'n_intervals')
)
def login(interval):
    url = "http://localhost:8070/authenticate"
    data = {'username': 'jforerobo', 'password': 'T$Cc#s7%hPqk'}
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=data)
    jsonResponse = r.json()
    token = 'Bearer ' + jsonResponse['token']
    
    return {'token': token}
'''


if __name__ == '__main__':
    app.run_server(debug=True)

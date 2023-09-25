import dash
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import requests
import json
import time
from flask import session

url = "http://localhost:8070/authenticate"
data = {'username': 'jforerobo', 'password': 'T$Cc#s7%hPqk'}
headers = {'Content-type': 'application/json'}
r = requests.post(url, json=data)
jsonResponse = r.json()
token = 'Bearer ' + jsonResponse['token']
text_file = open("file.txt", "w")
n = text_file.write(token)
text_file.close()


app = Dash(__name__, use_pages=True)
server = app.server

'''
 dbc.NavItem(dbc.NavLink("capacitaciones, investigación y creación artística",
                        href='/mecanismo-comunicacion-informacion-oficial')),
'''

app.layout = html.Div([
    dcc.Interval(
        id='interval',
        interval=1 * 3600000,
        n_intervals=0),
    dcc.Store(id='store'),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Aseo, transporte, vigilancia y mantenimiento",
                                    href='/servicios-aseo-transporte-vigilancia-mantenimiento-gestion-administrativa-y-financiera')),
            dbc.NavItem(dbc.NavLink("Gestión Financiera",
                                    href='/presupuesto-proyectos-investigacion-gestion-administrativa-y-financiera')),
            dbc.NavItem(dbc.NavLink("Gestión Administrativa de Bienes y Servicios",
                                    href='/adquisicion-bienes-y-servicios-gestion-administrativa-y-financiera')),
            dbc.NavItem(dbc.NavLink("Gestión Documental",
                                    href='/actualizacion-TRD-y-TVD-gestion-documental')),
            dbc.NavItem(dbc.NavLink("Gestión de Ordenamiento y Desarrollo Físico",
                                    href='/elaboracion-y-diseno-proyectos-infraestructura')),

        ],
        brand="Prig Data App",
        color="light",
        dark=False,
        expand="xs"
    ),

    dash.page_container
])


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
    text_file = open("file.txt", "w")
    n = text_file.write(token)
    text_file.close()
    return {'token': token}


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/servicios-aseo-transporte-vigilancia-mantenimiento-gestion-administrativa-y-financiera')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Gestión Administrativa y Financiera&programa_param=Aseo, transporte, vigilancia y mantenimiento&actividad_param=Servicios de aseo, transporte, vigilancia, mantenimiento"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0

data = pd.DataFrame(list)

# logros alcanzados

layout = html.Div([
    html.H2('Gestión Administrativa y Financiera'),
    html.H3('Aseo, transporte, vigilancia y mantenimiento'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Servicios de aseo, transporte, vigilancia, mantenimiento", active=True,
                                    href="/servicios-aseo-transporte-vigilancia-mantenimiento-gestion-administrativa-y-financiera")),

        ],
        pills=True,),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_servicios_aseo_transporte_vigilancia_mantenimiento_gestion_administrativa",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_servicios_aseo_transporte_vigilancia_mantenimiento_gestion_administrativa",
                            options=data['Año'].unique(),
                            clearable=True,
                            placeholder="Seleccione el año",
                        ),
                    ]), lg=6),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div([
                            dash_table.DataTable(
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'fontFamily': 'Mulish',
                                    'fontSize': '18pts',
                                    'fontWeight': 400
                                },
                                style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold',
                                    'textAlign': 'center',
                                    'fontFamily': 'Mulish',
                                    'fontSize': '22pts',
                                    'fontWeight': 500
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(29, 105, 150, 0.1)',
                                    }
                                ],
                                id='logros_tabla_servicios_aseo_transporte_vigilancia_mantenimiento_gestion_administrativa',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_servicios_aseo_transporte_vigilancia_mantenimiento_gestion_administrativa", "data"),
    [Input("facultad_servicios_aseo_transporte_vigilancia_mantenimiento_gestion_administrativa", "value"), Input("anio_servicios_aseo_transporte_vigilancia_mantenimiento_gestion_administrativa", "value")])
def logros_alcanzados_servicios_aseo_transporte_vigilancia_mantenimiento_gestion_administrativa(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
    df = data
    table = df.to_dict('records')
    return table

import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
from flask import session
import requests

dash.register_page(
    __name__, path='/acompanamiento-programas-especiales')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Acompañamiento estudiantil&actividad_param=Acompañamiento a Programas Especiales: PAES, PEAMA, Ser Pilo Paga y Generación E"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': '',
                    'Grupos participantes': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logro'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Grupos participantes'] = a['cifra']
                    i += 1
            if i == 2:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)

data['Grupos participantes'] = data['Grupos participantes'].replace(['584'], 'PAES')
data['Grupos participantes'] = data['Grupos participantes'].replace(['585'], 'PEAMA')
data['Grupos participantes'] = data['Grupos participantes'].replace(['586'], 'Ser Pilo Paga')
data['Grupos participantes'] = data['Grupos participantes'].replace(['587'], 'Generación E')


layout = html.Div([
    html.H2('Formación'),
    html.H3('Acompañamiento estudiantil'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("PAES, PEAMA, Ser Pilo Paga y Generación E", active=True, href="/acompanamiento-programas-especiales")),
            dbc.NavItem(dbc.NavLink("Iniciativas de apoyo a estudiantes", href="/iniciativas-apoyos-estudiantes")),
        ],
        pills=True,),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_acompañamiento_programas_especiales",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_acompañamiento_programas_especiales",
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
                                id='logros_tabla_acompañamiento_programas_especiales',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_acompañamiento_programas_especiales", "data"),
    [Input("facultad_acompañamiento_programas_especiales", "value"), Input("anio_acompañamiento_programas_especiales", "value")])
def logros_alcanzados_acompañamiento_programas_especiales(facultad, anio):
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

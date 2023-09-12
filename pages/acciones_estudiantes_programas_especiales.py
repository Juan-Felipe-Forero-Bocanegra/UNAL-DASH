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
    __name__, path='/acciones-estudiantes-programas-especiales')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Bienestar Universitario&programa_param=Área de Acompañamiento Integral&actividad_param=Acciones con estudiantes de Programas Especiales"
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
                    'Grupo objetivo': '',
                }
            if a['actividadDatoLista']['nombre'] == 'Logro':
                if a['indice'] == j:
                    o['Logro'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['nombre'] == 'Grupo objetivo':
                if a['indice'] == j:
                    o['Grupo objetivo'] = a['cifra']
                    i += 1
            if i == 2:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)

data['Grupo objetivo'] = data['Grupo objetivo'].replace(['589'], 'PAES')
data['Grupo objetivo'] = data['Grupo objetivo'].replace(['590'], 'PEAMA')
data['Grupo objetivo'] = data['Grupo objetivo'].replace(
    ['591'], 'Ser Pilo Paga y Generación E')


layout = html.Div([
    html.H2('Bienestar Universitario'),
    html.H3('Área de Acompañamiento Integral'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Admisión e inducción",
                                    href='/admision-e-induccion-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Acciones con estudiantes de programas especiales", active=True,
                        href="/acciones-estudiantes-programas-especiales")),
            dbc.NavItem(dbc.NavLink("Inclusión, género y accesibilidad",
                                    href="/inclusion-genero-accesibilidad-bienestar-universitario")),
            dbc.NavItem(dbc.NavLink("Acciones con estudiantes en general",
                                    href="/acciones-estudiantes-general-bienestar-universitario")),
        ],
        pills=True,),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_acciones_estudiantes_programas_especiales",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_acciones_estudiantes_programas_especiales",
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
                                id='logros_tabla_acciones_estudiantes_programas_especiales',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_acciones_estudiantes_programas_especiales", "data"),
    [Input("facultad_acciones_estudiantes_programas_especiales", "value"), Input("anio_acciones_estudiantes_programas_especiales", "value")])
def logros_alcanzados_acciones_estudiantes_programas_especiales(facultad, anio):
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

import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/salidas-no-conformes-desarrollo-organizacional')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Desarrollo Organizacional&programa_param=Implementación del Sistema de Gestión de Calidad&actividad_param=Salidas no conformes"
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
                    'Gestión realizadas': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Gestión realizada'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0

data = pd.DataFrame(list)

# logros alcanzados

layout = html.Div([
    html.H2('Desarrollo Organizacional'),
    html.H3('Implementación del Sistema de Gestión de Calidad'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Procesos y procedimientos",
                                    href="/procesos-y-procedimientos-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Retroalimentación con partes interesadas",
                                    href="/retroalimentacion-partes-interesadas-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Trámites y servicios",
                                    href="/tramites-servicios-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Salidas no conformes", active=True,
                                    href="/salidas-no-conformes-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Mejoramiento contínuo del SGC",
                                    href="/mejoramiento-continuo-SGC-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Auditorias",
                                    href="/auditorias-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Planes de mejoramiento y acciones correctivas",  
                                    href="/planes-mejoramiento-acciones-correctivas-desarrollo-organizacional")),

        ],
        pills=True,),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_salidas_no_conformes_desarrollo_organizacional",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_salidas_no_conformes_desarrollo_organizacional",
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
                                id='logros_tabla_salidas_no_conformes_desarrollo_organizacional',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_salidas_no_conformes_desarrollo_organizacional", "data"),
    [Input("facultad_salidas_no_conformes_desarrollo_organizacional", "value"), Input("anio_salidas_no_conformes_desarrollo_organizacional", "value")])
def logros_alcanzados_salidas_no_conformes_desarrollo_organizacional(facultad, anio):
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

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
    __name__, path='/resultados-seguimientos-tutores-docentes')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Tutores docentes&actividad_param=Resultados de los seguimientos"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Periodo': '',
                    'Actividades': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Periodo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Actividades'] = a['cifra']
                    i += 1
            if i == 2:
                list.append(o)
                i = 0
                j += 1
    if c['informeActividadDetalle']['orden'] == 2:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Requerimiento': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Requerimiento'] = a['cifra']
                i += 1
            if i == 1:
                list2.append(o)
                i = 0
    if c['informeActividadDetalle']['orden'] == 3:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Dificultad': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Dificultad'] = a['cifra']
                i += 1
            if i == 1:
                list3.append(o)
                i = 0


data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)

data['Periodo'] = data['Periodo'].replace(['578'], 'Semestre I')
data['Periodo'] = data['Periodo'].replace(['579'], 'Semestre II')


layout = html.Div([
    html.H2('Formación'),
    html.H3('Tutores docentes'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Designación de tutores docentes",
                                    href="/designacion-tutores-docentes")),
            dbc.NavItem(dbc.NavLink("Seguimiento a docentes tutores",
                                    href="/seguimiento-docentes-tutores")),
            dbc.NavItem(dbc.NavLink("Resultados de los seguimientos", active=True,
                                    href="/resultados-seguimientos-tutores-docentes")),

        ],
        pills=True,),
    html.H5('Resultados de los seguimientos'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_resultados_seguimientos_tutores_docentes",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_resultados_seguimientos_tutores_docentes",
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
                                id='logros_tabla_resultados_seguimientos_tutores_docentes',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
    html.H5('Principales requerimientos de los estudiantes'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_resultados_principales_requerimientos_estudiantes",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_resultados_principales_requerimientos_estudiantes",
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
                                id='logros_tabla_resultados_principales_requerimientos_estudiantes',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
    html.H5('Dificultades presentadas'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_resultados_seguimiento_dificultades",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_resultados_seguimiento_dificultades",
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
                                id='logros_tabla_resultados_seguimiento_dificultades',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),



], className='layout')


@callback(
    Output("logros_tabla_resultados_seguimientos_tutores_docentes", "data"),
    [Input("facultad_resultados_seguimientos_tutores_docentes", "value"), Input("anio_resultados_seguimientos_tutores_docentes", "value")])
def logros_alcanzados_resultados_seguimientos_tutores_docentes(facultad, anio):
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


@callback(
    Output("logros_tabla_resultados_principales_requerimientos_estudiantes", "data"),
    [Input("facultad_resultados_principales_requerimientos_estudiantes", "value"), Input("anio_resultados_principales_requerimientos_estudiantes", "value")])
def logros_alcanzados_resultados_principales_requerimientos_estudiantes(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data_2
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table

@callback(
    Output("logros_tabla_resultados_seguimiento_dificultades", "data"),
    [Input("facultad_resultados_seguimiento_dificultades", "value"), Input("anio_resultados_seguimiento_dificultades", "value")])
def logros_alcanzados_resultados_seguimiento_dificultades(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_3
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data_3
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data_3
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
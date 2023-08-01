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
    __name__, path='/creacion-modicacion-programas-planes-estudio')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Gestión de programas curriculares&actividad_param=Creación y modificación de programas y planes de estudio"
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
                    'Programas nuevos': '',
                    'Nivel de formación': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logro'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Programas nuevos'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Nivel de formación'] = a['cifra']
                    i += 1
            if i == 3:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)

layout = html.Div([
    html.H2('Formación'),
    html.H3('Gestión de programas curriculares'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Creación y modificación de programas y planes de estudio", active=True, href="/creacion-modicacion-programas-planes-estudio")),
            dbc.NavItem(dbc.NavLink(
                "Autoevaluación de los programas académicos", href="/autoevaluacion-programas-academicos")),
            dbc.NavItem(dbc.NavLink(
                "Planes de mejoramiento de los programas académicos", href="/planes-mejoramiento-programas-academicos")),
            dbc.NavItem(dbc.NavLink(
                "Acreditación de programas académicos", href="/acreditacion-programas-academicos")),
            dbc.NavItem(dbc.NavLink(
                "Proyectos Educativos de los Programas (PEP)", href="/proyectos-educativos-programas")),
             dbc.NavItem(dbc.NavLink(
                "Recursos en Autoevaluación, Planes de Mejoramiento y Acreditación", href="/recursos-autoevaluacion-planes-mejoramiento-acreditacion")),
        ],
        pills=True,),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_creacion_modificacion_programas_planes_estudio",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_creacion_modificacion_programas_planes_estudio",
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
                                id='logros_tabla_creacion_modificacion_programas_planes_estudio',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_creacion_modificacion_programas_planes_estudio", "data"),
    [Input("facultad_creacion_modificacion_programas_planes_estudio", "value"), Input("anio_creacion_modificacion_programas_planes_estudio", "value")])
def logros_alcanzados_creacion_modificacion_programas_planes_estudio(facultad, anio):
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

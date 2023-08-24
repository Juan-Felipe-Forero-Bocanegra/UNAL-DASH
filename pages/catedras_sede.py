import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/catedras-sede')


f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Gestión de la actividad académica&actividad_param=Cátedras de sede"
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
                    'Logros': '',
                    'Docentes': '',
                    'Estudiantes': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logros'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Docentes'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Estudiantes'] = a['cifra']
                    i += 1
            if i == 3:
                list.append(o)
                i = 0
                j += 1


data = pd.DataFrame(list)

data.fillna(0, inplace=True)
data['Logros'] = data['Logros'].replace(0, 'N/A')
data = data[data['Logros'] != 'N/A']

docentes_tmp = data[['Facultad', 'Año', 'Docentes']]
docentes = docentes_tmp.rename(columns={'Docentes': 'cifra'})

estudiantes_tmp = data[['Facultad', 'Año', 'Estudiantes']]
estudiantes = estudiantes_tmp.rename(columns={'Estudiantes': 'cifra'})

def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total

# Docentes

docentes['Año'] = docentes['Año'].astype('str')
docentes.fillna(0, inplace=True)
docentes['cifra'] = docentes['cifra'].astype('int')

docentes = docentes.groupby(['Facultad', 'Año'])['cifra'].sum().reset_index()

docentes.apply(lambda x: total_function(
    x['Facultad'], x['Año'], docentes), axis=1)

total_docentes = docentes['cifra'].sum()


# Estudiantes

estudiantes['Año'] = estudiantes['Año'].astype('str')
estudiantes.fillna(0, inplace=True)
estudiantes['cifra'] = estudiantes['cifra'].astype('int')

estudiantes = estudiantes.groupby(['Facultad', 'Año'])[
    'cifra'].sum().reset_index()

estudiantes.apply(lambda x: total_function(
    x['Facultad'], x['Año'], estudiantes), axis=1)

total_estudiantes = estudiantes['cifra'].sum()

layout = html.Div([
    html.H2('Formación'),
    html.H3('Gestión de la actividad académica'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Cátedras de sede",
                        active=True, href="/catedras-sede")),
            dbc.NavItem(dbc.NavLink("Buenas prácticas de gestión académica",
                        href="/buenas-practicas-gestion-academica")),
            dbc.NavItem(dbc.NavLink("Evaluación estudiantil y examen Saber Pro",
                        href="/evaluacion-estudiantil-examen-saber-pro")),
            dbc.NavItem(dbc.NavLink("Actividades  para el aprendizaje de lenguas extranjeras",
                                    href="/actividades_aprendizaje_lenguas_extranjeras")),
        ],
        pills=True,),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_docentes,
                                        className="card-number",
                                    ),
                                    html.P("docentes participantes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_estudiantes,
                                        className="card-number",
                                    ),
                                    html.P("estudiantes beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Docentes participantes en cátedras de sede'),
    dcc.Graph(id="graph_catedras_sede_docentes",
              figure=px.bar(docentes,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Docentes participantes'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Estudiantes beneficiados en cátedras de sede'),
    dcc.Graph(id="graph_catedras_sede_estudiantes",
              figure=px.bar(estudiantes,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes beneficiados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_catedras_sede",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_catedras_sede",
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
                                id='logros_table_catedras_sede',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("logros_table_catedras_sede", "data"),
    [Input("facultad_catedras_sede", "value"), Input("anio_catedras_sede", "value")])
def logros_alcanzados_catedras_sede(facultad, anio):
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

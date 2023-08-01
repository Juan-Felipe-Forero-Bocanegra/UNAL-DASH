import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/cursos')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Cursos y Asignaturas&actividad_param=Cursos"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []
list4 = []
list5 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list.append(o)
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list2.append(o)
    if c['informeActividadDetalle']['orden'] == 3:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list3.append(o)
    if c['informeActividadDetalle']['orden'] == 4:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list4.append(o)
    if c['informeActividadDetalle']['orden'] == 5:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
    list5.append(o)

data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)
data_4 = pd.DataFrame(list4)
data_5 = pd.DataFrame(list5)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Número de Cursos Teóricos dictados en el semestre 1

data['Año'] = data['Año'].astype('str')
data.fillna(0, inplace=True)
data['cifra'] = data['cifra'].astype('int')

data.apply(lambda x: total_function(x['Facultad'], x['Año'], data), axis=1)
total_data = data['cifra'].sum()

# Recursos nacional

data_2['Año'] = data_2['Año'].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

# Recursos Sede

data_3['Año'] = data_3['Año'].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()

# Recursos funcionamiento

data_4['Año'] = data_4['Año'].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('int')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)
total_data_4 = data_4['cifra'].sum()

layout = html.Div([
    html.H2('Formación'),
    html.H3('Cursos y Asignaturas'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Cursos", active=True, href="/cursos")),
            dbc.NavItem(dbc.NavLink(
                "Asignaturas",  href="/asignaturas")),

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
                                        total_data,
                                        className="card-number",
                                    ),
                                    html.P("cursos teóricos semestre 1"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_2,
                                        className="card-number",
                                    ),
                                    html.P("cursos teóricos semestre 2"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_3,
                                        className="card-number",
                                    ),
                                    html.P("cursos prácticos semestre 1"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_4,
                                        className="card-number",
                                    ),
                                    html.P("cursos prácticos semestre 2"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Cursos teóricos semestre 1'),
    dcc.Graph(id="graph_cursos_teoricos_semestre_1",
              figure=px.bar(data,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Cursos teóricos semestre 1'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Cursos teóricos semestre 2'),
    dcc.Graph(id="graph_cursos_teoricos_semestre_2",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Cursos teóricos semestres 2'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Cursos prácticos semestre 1'),
    dcc.Graph(id="graph_cursos_practicos_semestre_1",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Cursos prácticos semestre 1'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Cursos prácticos semestre 2'),
    dcc.Graph(id="graph_cursos_practicos_semestre_2",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Cursos prácticos semestre 2'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
], className='layout')

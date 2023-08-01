import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/recursos-autoevaluacion-planes-mejoramiento-acreditacion')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Gestión de programas curriculares&actividad_param=Recursos en Autoevaluación, Planes de Mejoramiento y Acreditación"
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
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list.append(o)
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list2.append(o)
    if c['informeActividadDetalle']['orden'] == 3:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list3.append(o)
    if c['informeActividadDetalle']['orden'] == 4:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list4.append(o)

data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)
data_4 = pd.DataFrame(list4)

def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Presupuesto ejecutado*

data['Año'] = data['Año'].astype('str')
data.fillna(0, inplace=True)
data['cifra'] = data['cifra'].astype('float')

data.apply(lambda x: total_function(x['Facultad'], x['Año'], data), axis=1)
total_data = data['cifra'].sum()
total_data = f'{total_data:,}'.replace(',', ' ')
total_data = '$ ' + total_data

# Recursos nacional

data_2['Año'] = data_2['Año'].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('float')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')
total_data_2 = '$ ' + total_data_2

# Recursos Sede

data_3['Año'] = data_3['Año'].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('float')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()
total_data_3 = f'{total_data_3:,}'.replace(',', ' ')
total_data_3 = '$ ' + total_data_3

# Recursos funcionamiento

data_4['Año'] = data_4['Año'].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('float')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)
total_data_4 = data_4['cifra'].sum()
total_data_4 = f'{total_data_4:,}'.replace(',', ' ')
total_data_4 = '$ ' + total_data_4

layout = html.Div([
    html.H2('Formación'),
    html.H3('Gestión de programas curriculares'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Creación y modificación de programas y planes de estudio", href="/creacion-modicacion-programas-planes-estudio")),
            dbc.NavItem(dbc.NavLink(
                "Autoevaluación de los programas académicos", href="/autoevaluacion-programas-academicos")),
             dbc.NavItem(dbc.NavLink(
                "Planes de mejoramiento de los programas académicos", href="/planes-mejoramiento-programas-academicos")),
             dbc.NavItem(dbc.NavLink(
                "Acreditación de programas académicos", href="/acreditacion-programas-academicos")),
             dbc.NavItem(dbc.NavLink(
                "Proyectos Educativos de los Programas (PEP)", href="/proyectos-educativos-programas")),
            dbc.NavItem(dbc.NavLink(
                "Recursos en Autoevaluación, Planes de Mejoramiento y Acreditación", active=True, href="/recursos-autoevaluacion-planes-mejoramiento-acreditacion")),
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
                                    html.P("presupuesto ejecutado"),
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
                                    html.P("recurso nacional"),
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
                                    html.P("recurso sede"),
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
                                    html.P("recurso funcionamiento"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Presupuesto ejecutado'),
    dcc.Graph(id="graph_presupuesto_ejecutado",
              figure=px.bar(data,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presupuesto ejecutado'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Recurso nacional'),
    dcc.Graph(id="graph_recurso_nacional",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Recurso nacional'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Recurso sede'),
    dcc.Graph(id="graph_recurso_sede",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Recurso sede'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Recurso funcionamiento'),
    dcc.Graph(id="graph_recurso_funcionamiento",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Recurso funcionamiento'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
], className='layout')


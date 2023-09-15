import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/planes-mejoramiento-acciones-correctivas-desarrollo-organizacional')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Desarrollo Organizacional&programa_param=Implementación del Sistema de Gestión de Calidad&actividad_param=Planes de mejoramiento y acciones correctivas"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []


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

data_2 = pd.DataFrame(list)
data_3 = pd.DataFrame(list2)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total

# Planes de mejoramiento


data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

# Acciones correctivas

data_3["Año"] = data_3["Año"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()


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
            dbc.NavItem(dbc.NavLink("Salidas no conformes",
                                    href="/salidas-no-conformes-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Mejoramiento contínuo del SGC",
                                    href="/mejoramiento-continuo-SGC-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Auditorias", 
                                    href="/auditorias-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Planes de mejoramiento y acciones correctivas",  active=True,
                                    href="/planes-mejoramiento-acciones-correctivas-desarrollo-organizacional")),

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
                                        total_data_2,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "planes de mejoramiento"),
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
                                    html.P(
                                        "acciones correctivas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Planes de mejoramiento'),
    dcc.Graph(id="graph_planes_mejoramiento_desarrollo_organizacional",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Planes de mejoramiento'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Acciones correctivas'),
    dcc.Graph(id="graph_acciones_correctivas_desarrollo_organizacional",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Acciones correctivas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
   
], className='layout')



import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/reparaciones-locativas-laboratorios')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Gestión de Laboratorios&programa_param=Proyectos de laboratorios&actividad_param=Reparaciones locativas en laboratorios"
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

data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Número de directrices solicitadas con recursos de la facultad

data["Año"] = data["Año"].astype('str')
data.fillna(0, inplace=True)
data['cifra'] = data['cifra'].astype('int')

data.apply(lambda x: total_function(x['Facultad'], x['Año'], data), axis=1)
total_data = data['cifra'].sum()

# Valor de las reparaciones locativas en laboratorios

data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('float')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
data_2['total'] = data_2['total'].map("{:,.2f}".format)
total_data_2 = data_2['cifra'].sum()
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')
total_data_2 = '$ ' + total_data_2

layout = html.Div([
    html.H2('Gestión de Laboratorios'),
    html.H3('Proyectos de laboratorios'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Proyectos y convenios",
                                    href="/formulacion-ejecucion-proyectos-y-convenios-laboratorios")),
            dbc.NavItem(dbc.NavLink("Adquisición de equipos de laboratorio",
                                    href="/adquisicion-equipos-laboratorios")),
            dbc.NavItem(dbc.NavLink("Compra de mobiliario en laboratorio",
                                    href="/compra-mobiliario-laboratorios")),
            dbc.NavItem(dbc.NavLink("Contratación externa de mantenimiento preventivo",
                                    href="/contratacion-externa-mantenimietno-preventivo-laboratorios")),
            dbc.NavItem(dbc.NavLink("Contratación externa de mantenimiento correctivo",
                                    href="/contratacion-externa-mantenimietno-correctivo-laboratorios")),
            dbc.NavItem(dbc.NavLink("Reparaciones locativas en laboratorios", active=True,
                                    href="/reparaciones-locativas-laboratorios")),
            dbc.NavItem(dbc.NavLink("Adquisición de suministros y materiales", 
                                    href="/adquisicion-suministros-materiales")),
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
                                    html.P("directrices solicitadas"),
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
                                    html.P(
                                        "valor de las reparaciones locativas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Directrices solicitadas'),
    dcc.Graph(id="graph_directrices_solicitadas_reparaciones_locativas_laboratorio",
              figure=px.bar(data,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Directrices solicitadas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Valor de las reparaciones locativas en laboratorios'),
    dcc.Graph(id="graph_valor_total_reparaciones_locativas_laboratorio",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Valor de las reparaciones locativas en laboratorios'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')

import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/energia')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Gestión ambiental&programa_param=Línea base antrópica&actividad_param=Energía"
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


# Consumo de energía en el último año

data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('float')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
data_2['total'] = data_2['total'].map("{:,.2f}".format)
total_data_2 = data_2['cifra'].sum()
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')

# Costo de energía en el último año

data_3["Año"] = data_3["Año"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('float')


data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
data_3['total'] = data_3['total'].map("{:,.2f}".format)
total_data_3 = data_3['cifra'].sum()
total_data_3 = f'{total_data_3:,}'.replace(',', ' ')
total_data_3 = '$ ' + total_data_3

layout = html.Div([
    html.H2('Gestión ambiental'),
    html.H3('Línea base antrópica'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Agua",
                                    href="/agua")),
            dbc.NavItem(dbc.NavLink("Energía", active=True,
                                    href="/energia")),
            dbc.NavItem(dbc.NavLink("Resíduos",
                                    href="/residuos")),
            dbc.NavItem(dbc.NavLink("Plagas y vectores",
                                    href="/plagas-y-vectores")),
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
                                    html.P("consumo de energía en (?)"),
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
                                    html.P("costo de la energía"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Consumo de energía'),
    dcc.Graph(id="graph_consumo_energia",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Consumo de energía'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Costo de la energía'),
    dcc.Graph(id="graph_costo_energia",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Costo de la energía'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')

import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/presupuesto-proyectos-investigacion-gestion-administrativa-y-financiera')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Gestión Administrativa y Financiera&programa_param=Gestión Financiera&actividad_param=Presupuesto en proyectos de investigación"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []

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
    if c['informeActividadDetalle']['orden'] == 6:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list6.append(o)

data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)
data_4 = pd.DataFrame(list4)
data_5 = pd.DataFrame(list5)
data_6 = pd.DataFrame(list6)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Presupuesto apropiado fondo especial

data["Año"] = data["Año"].astype('str')
data.fillna(0, inplace=True)
data['cifra'] = data['cifra'].astype('float')

data.apply(lambda x: total_function(x['Facultad'], x['Año'], data), axis=1)

data['total'] = data['total'].map("{:,.2f}".format)

total_data = data['cifra'].sum()
total_data = f'{total_data:,}'.replace(',', ' ')
total_data = '$ ' + total_data

# Presupuesto ejecutado fondo especial

data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('float')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)

data_2['total'] = data_2['total'].map("{:,.2f}".format)

total_data_2 = data_2['cifra'].sum()
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')
total_data_2 = '$ ' + total_data_2

# Presupuesto apropiado fondo UGI

data_3["Año"] = data_3["Año"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('float')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)

data_3['total'] = data_3['total'].map("{:,.2f}".format)

total_data_3 = data_3['cifra'].sum()
total_data_3 = f'{total_data_3:,}'.replace(',', ' ')
total_data_3 = '$ ' + total_data_3

# Presupuesto ejecutado fondo UGI

data_4["Año"] = data_4["Año"].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('float')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)

data_4['total'] = data_4['total'].map("{:,.2f}".format)

total_data_4 = data_4['cifra'].sum()
total_data_4 = f'{total_data_4:,}'.replace(',', ' ')
total_data_4 = '$ ' + total_data_4

# Valor de la Apropiación en Proyectos de Investigación

data_5["Año"] = data_5["Año"].astype('str')
data_5.fillna(0, inplace=True)
data_5['cifra'] = data_5['cifra'].astype('float')

data_5.apply(lambda x: total_function(x['Facultad'], x['Año'], data_5), axis=1)

data_5['total'] = data_5['total'].map("{:,.2f}".format)

total_data_5 = data_5['cifra'].sum()
total_data_5 = f'{total_data_5:,}'.replace(',', ' ')
total_data_5 = '$ ' + total_data_5

# Valor de Compromisos en Proyectos de Investigación

data_6["Año"] = data_6["Año"].astype('str')
data_6.fillna(0, inplace=True)
data_6['cifra'] = data_6['cifra'].astype('float')

data_6.apply(lambda x: total_function(x['Facultad'], x['Año'], data_6), axis=1)

data_6['total'] = data_6['total'].map("{:,.2f}".format)

total_data_6 = data_6['cifra'].sum()
total_data_6 = f'{total_data_6:,}'.replace(',', ' ')
total_data_6 = '$ ' + total_data_6


layout = html.Div([
    html.H2('Gestión Administrativa y Financiera'),
    html.H3('Gestión Financiera'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Presupuesto en proyectos de investigación", active=True,
                                    href="/presupuesto-proyectos-investigacion-gestion-administrativa-y-financiera")),
            dbc.NavItem(dbc.NavLink("Presupuesto en proyectos de extensión", 
                                    href="/presupuesto-proyectos-extension-gestion-administrativa-y-financiera")),


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
                                    html.P(
                                        "presupuesto apropiado fondo especial"),
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
                                        "presupuesto ejecutado fondo especial"),
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
                                        "presupuesto apropiado fondo UGI"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.Div(
        [
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
                                    html.P(
                                        "presupuesto ejecutado fondo UGI"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_5,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "valor de la Apropiación en Proyectos de Investigación"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_6,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "valor de Compromisos en Proyectos de Investigación"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Presupuesto apropiado fondo especial'),
    dcc.Graph(id="graph_presupuesto_apropiado_fondo_especial_gestion_administrativa_y_financiera",
              figure=px.bar(data,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presupuesto apropiado fondo especial'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Presupuesto ejecutado fondo especial'),
    dcc.Graph(id="graph_presupuesto_ejecutado_fondo_especial_gestion_administrativa_y_financiera",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presupuesto ejecutado fondo especial'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Presupuesto apropiado fondo UGI'),
    dcc.Graph(id="graph_presupuesto_apropiado_fondo_ugi_gestion_administrativa_y_financiera",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presupuesto apropiado fondo UGI'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Presupuesto ejecutado fondo UGI'),
    dcc.Graph(id="graph_presupuesto_ejecutado_fondo_ugi_gestion_administrativa_y_financiera",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presupuesto ejecutado fondo UGI'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Valor de la Apropiación en Proyectos de Investigación'),
    dcc.Graph(id="graph_valor_apropiacion_proyectos_investigacion_gestion_administrativa_y_financiera",
              figure=px.bar(data_5,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Valor de la Apropiación en Proyectos de Investigación'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Valor de Compromisos en Proyectos de Investigación'),
    dcc.Graph(id="graph_valor_compromisos_proyectos_investigacion_gestion_administrativa_y_financiera",
              figure=px.bar(data_6,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Valor de Compromisos en Proyectos de Investigación'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')

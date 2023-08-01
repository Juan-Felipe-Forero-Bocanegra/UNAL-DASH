import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/residuos')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Gestión ambiental&programa_param=Línea base antrópica&actividad_param=Residuos"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []

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
    if c['informeActividadDetalle']['orden'] == 7:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list7.append(o)

data_2 = pd.DataFrame(list)
data_3 = pd.DataFrame(list2)
data_4 = pd.DataFrame(list3)
data_5 = pd.DataFrame(list4)
data_6 = pd.DataFrame(list5)
data_7 = pd.DataFrame(list6)
data_8 = pd.DataFrame(list7)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total

# Cantidad de residuos biodegradables


data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('float')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')
total_data_2 = total_data_2 + ' kg'

# Cantidad de residuos reciclables

data_3["Año"] = data_3["Año"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('float')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()
total_data_3 = round(total_data_3, 2)
total_data_3 = f'{total_data_3:,}'.replace(',', ' ')
total_data_3 = total_data_3 + ' kg'

# Cantidad de residuos ordinarios

data_4["Año"] = data_4["Año"].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('float')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)
total_data_4 = data_4['cifra'].sum()
total_data_4 = f'{total_data_4:,}'.replace(',', ' ')
total_data_4 = total_data_4 + ' kg'

# Cantidad de RCD

data_5["Año"] = data_5["Año"].astype('str')
data_5.fillna(0, inplace=True)
data_5['cifra'] = data_5['cifra'].astype('float')

data_5.apply(lambda x: total_function(x['Facultad'], x['Año'], data_5), axis=1)
total_data_5 = data_5['cifra'].sum()
total_data_5 = f'{total_data_5:,}'.replace(',', ' ')
total_data_5 = total_data_5 + ' kg'

# Cantidad de residuos químicos

data_6["Año"] = data_6["Año"].astype('str')
data_6.fillna(0, inplace=True)
data_6['cifra'] = data_6['cifra'].astype('float')

data_6.apply(lambda x: total_function(x['Facultad'], x['Año'], data_6), axis=1)
total_data_6 = data_6['cifra'].sum()
total_data_6 = f'{total_data_6:,}'.replace(',', ' ')
total_data_6 = total_data_6 + ' kg'

# Cantidad de residuos infecciosos

data_7["Año"] = data_7["Año"].astype('str')
data_7.fillna(0, inplace=True)
data_7['cifra'] = data_7['cifra'].astype('float')

data_7.apply(lambda x: total_function(x['Facultad'], x['Año'], data_7), axis=1)
total_data_7 = data_7['cifra'].sum()
total_data_7 = f'{total_data_7:,}'.replace(',', ' ')
total_data_7 = total_data_7 + ' kg'

# Cantidad de residuos posconsumo

data_8["Año"] = data_8["Año"].astype('str')
data_8.fillna(0, inplace=True)
data_8['cifra'] = data_8['cifra'].astype('float')

data_8.apply(lambda x: total_function(x['Facultad'], x['Año'], data_8), axis=1)
total_data_8 = data_8['cifra'].sum()
total_data_8 = f'{total_data_8:,}'.replace(',', ' ')
total_data_8 = total_data_8 + ' kg'

layout = html.Div([
    html.H2('Gestión ambiental'),
    html.H3('Línea base antrópica'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Agua",
                                    href="/agua")),
            dbc.NavItem(dbc.NavLink("Energía",
                                    href="/energia")),
            dbc.NavItem(dbc.NavLink("Resíduos", active=True,
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
                                    html.P("biodegradables"),
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
                                    html.P("reciclables"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_4,
                                        className="card-number",
                                    ),
                                    html.P("ordinarios"),
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
                                        total_data_5,
                                        className="card-number",
                                    ),
                                    html.P("RCD generados"),
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
                                    html.P("químicos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_7,
                                        className="card-number",
                                    ),
                                    html.P("infecciosos"),
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
                                        total_data_8,
                                        className="card-number",
                                    ),
                                    html.P("posconsumo"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Residuos biodegradables'),
    dcc.Graph(id="graph_residuos_biodegradables",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Residuos biodegradables'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Residuos reciclables'),
    dcc.Graph(id="graph_residuos_reciclabes",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Residuos reciclables'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Residuos ordinarios'),
    dcc.Graph(id="graph_residuos_ordinarios",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Residuos ordinarios'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('RCD generado'),
    dcc.Graph(id="graph_RCD_generado",
              figure=px.bar(data_5,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'RDC generados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Residuos químicos'),
    dcc.Graph(id="graph_residuos_químicos",
              figure=px.bar(data_6,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Resíduos químicos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Residuos infecciosos'),
    dcc.Graph(id="graph_residuos_infecciosos",
              figure=px.bar(data_7,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Residuos infeccsiosos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Residuos posconsumo'),
    dcc.Graph(id="graph_residuos_posconsumo",
              figure=px.bar(data_8,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Residuos posconsumo'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')

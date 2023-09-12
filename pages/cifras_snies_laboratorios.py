import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/cifras-snies-laboratorios')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Gestión de Laboratorios&programa_param=Cifras SNIES&actividad_param=Cifras SNIES"
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
list8 = []

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
    if c['informeActividadDetalle']['orden'] == 8:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list8.append(o)

data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)
data_4 = pd.DataFrame(list4)
data_5 = pd.DataFrame(list5)
data_6 = pd.DataFrame(list6)
data_7 = pd.DataFrame(list7)
data_8 = pd.DataFrame(list8)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Número de laboratorios

data['Año'] = data['Año'].astype('str')
data.fillna(0, inplace=True)
data['cifra'] = data['cifra'].astype('int')

data.apply(lambda x: total_function(x['Facultad'], x['Año'], data), axis=1)
total_data = data['cifra'].sum()

# Número de talleres especializados*

data_2['Año'] = data_2['Año'].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

# Número de clínicas

data_3['Año'] = data_3['Año'].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()

# Metros cuadrados de área de laboratorios

data_4['Año'] = data_4['Año'].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('float')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)
total_data_4 = data_4['cifra'].sum()

# Metros cuadrados de talleres especializados

data_5['Año'] = data_5['Año'].astype('str')
data_5.fillna(0, inplace=True)
data_5['cifra'] = data_5['cifra'].astype('float')

data_5.apply(lambda x: total_function(x['Facultad'], x['Año'], data_5), axis=1)
total_data_5 = data_5['cifra'].sum()

# Metros cuadrados de clínicas

data_6['Año'] = data_6['Año'].astype('str')
data_6.fillna(0, inplace=True)
data_6['cifra'] = data_6['cifra'].astype('float')

data_6.apply(lambda x: total_function(x['Facultad'], x['Año'], data_6), axis=1)
total_data_6 = data_6['cifra'].sum()

# Número de puestos disponibles en laboratorios

data_7['Año'] = data_7['Año'].astype('str')
data_7.fillna(0, inplace=True)
data_7['cifra'] = data_7['cifra'].astype('int')

data_7.apply(lambda x: total_function(x['Facultad'], x['Año'], data_7), axis=1)
total_data_7 = data_7['cifra'].sum()

# Número de puestos disponibles en talleres especializados

data_8['Año'] = data_8['Año'].astype('str')
data_8.fillna(0, inplace=True)
data_8['cifra'] = data_8['cifra'].astype('int')

data_8.apply(lambda x: total_function(x['Facultad'], x['Año'], data_8), axis=1)
total_data_8 = data_8['cifra'].sum()

layout = html.Div([
    html.H2('Gestión de laboratorios'),
    html.H3('Cifras SNIES'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Cifras SNIES", active=True, href="/cifras-snies-laboratorios")),

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
                                    html.P("laboratorios"),
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
                                    html.P("talleres especializados"),
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
                                    html.P("clínicas"),
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
                                    html.P(
                                        "metros cuadrados de área de laboratorios"),
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
                                        "metros cuadrados de talleres especializados"),
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
                                        "metros cuadrados de clínicas"),
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
                                        total_data_7,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "puestos disponibles en laboratorios"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_8,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "puestos disponibles en talleres especializados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Laboratorios'),
    dcc.Graph(id="graph_numero_laboratorios_cifras_snies",
              figure=px.bar(data,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Laboratorios'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Talleres especializados'),
    dcc.Graph(id="graph_talleres_especializados_cifras_snies",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Talleres especializados'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Clíncas'),
    dcc.Graph(id="graph_clinicas_cifras_snies",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Clíncas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Metros cuadrados de área de laboratorios'),
    dcc.Graph(id="graph_metros_cuadrados_areas_laboratorios_cifras_snies",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Metros cuadrados de área de laboratorios'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Metros cuadrados de talleres especializados'),
    dcc.Graph(id="graph_metros_cuadrados_areas_talleres_especializados_cifras_snies",
              figure=px.bar(data_5,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Metros cuadrados de talleres especializados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Metros cuadrados de clínicas'),
    dcc.Graph(id="graph_metros_cuadrados_clínicas_cifras_snies",
              figure=px.bar(data_6,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Metros cuadrados de clínicas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Puestos disponibles en laboratorios'),
    dcc.Graph(id="graph_puestos_disponibles_laboratorios_cifras_snies",
              figure=px.bar(data_7,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': ' Puestos disponibles en laboratorios'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Puestos disponibles en talleres especializados'),
    dcc.Graph(id="graph_puestos_disponibles_talleres_especializados_cifras_snies",
              figure=px.bar(data_8,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': ' Puestos disponibles en talleres especializados'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
], className='layout')

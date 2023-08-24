import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/productos-por-modalidad')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Proyectos de investigación&actividad_param=Productos por modalidad"
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

# Ponencias


data_2["Año"] = data_2["Año"].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

# Pasantías

data_3["Año"] = data_3["Año"].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()

# Tesis

data_4["Año"] = data_4["Año"].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('int')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)
total_data_4 = data_4['cifra'].sum()

# Conferencias

data_5["Año"] = data_5["Año"].astype('str')
data_5.fillna(0, inplace=True)
data_5['cifra'] = data_5['cifra'].astype('int')

data_5.apply(lambda x: total_function(x['Facultad'], x['Año'], data_5), axis=1)
total_data_5 = data_5['cifra'].sum()

# Foros

data_6["Año"] = data_6["Año"].astype('str')
data_6.fillna(0, inplace=True)
data_6['cifra'] = data_6['cifra'].astype('int')

data_6.apply(lambda x: total_function(x['Facultad'], x['Año'], data_6), axis=1)
total_data_6 = data_6['cifra'].sum()

# Presentaciones

data_7["Año"] = data_7["Año"].astype('str')
data_7.fillna(0, inplace=True)
data_7['cifra'] = data_7['cifra'].astype('int')

data_7.apply(lambda x: total_function(x['Facultad'], x['Año'], data_7), axis=1)
total_data_7 = data_7['cifra'].sum()

# Conciertos

data_8["Año"] = data_8["Año"].astype('str')
data_8.fillna(0, inplace=True)
data_8['cifra'] = data_8['cifra'].astype('int')

data_8.apply(lambda x: total_function(x['Facultad'], x['Año'], data_8), axis=1)
total_data_8 = data_8['cifra'].sum()

layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Proyectos de investigación'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Cifras de proyectos en el periodo",
                                    href="/cifras-proyectos-periodo")),
            dbc.NavItem(dbc.NavLink("Productos por modalidad", active=True,
                                    href="/productos-por-modalidad")),
            dbc.NavItem(dbc.NavLink("Proyectos con financiación interna",
                                    href="/proyectos-financiacion-interna-investigacion-creacion-artistica")),
            dbc.NavItem(dbc.NavLink("Proyectos con financiación externa",
                                    href="/proyectos-financiacion-externa-investigacion-creacion-artistica")),
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
                                        "ponencias"),
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
                                        "pasantías"),
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
                                    html.P(
                                        "tesis"),
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
                                    html.P(
                                        "conferencias"),
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
                                        "foros"),
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
                                    html.P(
                                        "presentaciones"),
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
                                    html.P(
                                        "conciertos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Ponencias'),
    dcc.Graph(id="graph_ponencias_productos_por_modalidad",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Ponencias'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Pasantías'),
    dcc.Graph(id="graph_pasantias_ponencias_productos_por_modalidad",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Pasantías'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Tesis'),
    dcc.Graph(id="graph_tesis_productos_por_modalidad",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Tesis'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Conferencias'),
    dcc.Graph(id="graph_conferencias_productos_por_modalidad",
              figure=px.bar(data_5,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Conferencias'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Foros'),
    dcc.Graph(id="graph_foros_productos_por_modalidad",
              figure=px.bar(data_6,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Foros'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Presentaciones'),
    dcc.Graph(id="graph_presentaciones_productos_por_modalidad",
              figure=px.bar(data_7,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presentaciones'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Conciertos'),
    dcc.Graph(id="graph_conciertos_productos_por_modalidad",
              figure=px.bar(data_8,
                            x="cifra",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Conciertos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                "Año": True},
                            barmode="group"
                            )),
], className='layout')

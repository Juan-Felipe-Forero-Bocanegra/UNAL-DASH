import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
from flask import session
import requests

dash.register_page(
    __name__, path='/convocatorias-internas-institucionales')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Convocatorias&actividad_param=Convocatorias internas (Presentación a convocatorias institucionales)"
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
                    'Objeto de la convocatoria (abreviado)': '',
                    'Logros alcanzados': '',
                    'Propuestas presentadas': '',
                    'Propuestas adjudicadas': '',
                    'Monto financiado interno': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Objeto de la convocatoria (abreviado)'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Logros alcanzados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Propuestas presentadas'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '4':
                if a['indice'] == j:
                    o['Propuestas adjudicadas'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '5':
                if a['indice'] == j:
                    o['Monto financiado interno'] = a['cifra']
                    i += 1
            if i == 5:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# propuestas presentadas
propuestas_presentadas_tmp = data[[
    'Facultad', 'Año', 'Propuestas presentadas']]
propuestas_presentadas = propuestas_presentadas_tmp.rename(
    columns={'Propuestas presentadas': 'cifra'})

propuestas_presentadas['Año'] = propuestas_presentadas['Año'].astype('str')
propuestas_presentadas.fillna(0, inplace=True)
propuestas_presentadas['cifra'] = propuestas_presentadas['cifra'].astype('int')

propuestas_presentadas = propuestas_presentadas.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

propuestas_presentadas.apply(lambda x: total_function(
    x['Facultad'], x['Año'], propuestas_presentadas), axis=1)

total_propuestas_presentadas = propuestas_presentadas['cifra'].sum()

# propuestas adjudicadas
propuestas_adjudicadas_tmp = data[[
    'Facultad', 'Año', 'Propuestas adjudicadas']]
propuestas_adjudicadas = propuestas_adjudicadas_tmp.rename(
    columns={'Propuestas adjudicadas': 'cifra'})

propuestas_adjudicadas['Año'] = propuestas_adjudicadas['Año'].astype('str')
propuestas_adjudicadas.fillna(0, inplace=True)
propuestas_adjudicadas['cifra'] = propuestas_adjudicadas['cifra'].astype('int')

propuestas_adjudicadas = propuestas_adjudicadas.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

propuestas_adjudicadas.apply(lambda x: total_function(
    x['Facultad'], x['Año'], propuestas_adjudicadas), axis=1)

total_propuestas_adjudicadas = propuestas_adjudicadas['cifra'].sum()

# Monto financiero interno

monto_financiado_interno_tmp = data[[
    'Facultad', 'Año', 'Monto financiado interno']]
monto_financiado_interno = monto_financiado_interno_tmp.rename(
    columns={'Monto financiado interno': 'cifra'})

monto_financiado_interno['Año'] = monto_financiado_interno['Año'].astype('str')
monto_financiado_interno.fillna(0, inplace=True)
monto_financiado_interno['cifra'] = monto_financiado_interno['cifra'].astype(
    'float')

monto_financiado_interno = monto_financiado_interno.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_financiado_interno.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_financiado_interno), axis=1)
monto_financiado_interno['total'] = monto_financiado_interno['total'].map(
    "{:,.2f}".format)

total_monto_financiado_interno = monto_financiado_interno['cifra'].sum()

total_monto_financiado_interno = f'{total_monto_financiado_interno:,}'.replace(
    ',', ' ')
total_monto_financiado_interno = '$ ' + total_monto_financiado_interno


data['Monto financiado interno'] = data['Monto financiado interno'].astype(
    'float')
data['Monto financiado interno'] = '$ ' + \
    data['Monto financiado interno'].map("{:,.2f}".format)

layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Convocatorias'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Convocatorias internas", active=True,
                        href="/convocatorias-internas-institucionales")),
            dbc.NavItem(dbc.NavLink("Convocatorias externas", 
                        href="/convocatorias-externas-otras-entidades")),
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
                                        total_propuestas_presentadas,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "propuestas presentadas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_propuestas_adjudicadas,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "propuestas adjudicadas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_monto_financiado_interno,
                                        className="card-number",
                                    ),
                                    html.P("monto financiado interno"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Propuestas presentadas'),
    dcc.Graph(id="graph_propuestas_presentadas_convocatorias_internas_institucionales",
              figure=px.bar(propuestas_presentadas,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Propuestas presentadas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Propuestas adjudicadas'),
    dcc.Graph(id="graph_propuestas_adjudicadas_convocatorias_internas_institucionales",
              figure=px.bar(propuestas_adjudicadas,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Propuestas adjudicadas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Monto financiado interno'),
    dcc.Graph(id="graph_monto_financiado_interno_convocatorias_internas_institucionales",
              figure=px.bar(monto_financiado_interno,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto financiado interno'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Descripción de las convocatorias'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_convocatorias_internas_investigacion_creacion_artistica",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_convocatorias_internas_investigacion_creacion_artistica",
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
                                id='logros_tabla_convocatorias_internas_investigacion_creacion_artistica',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_convocatorias_internas_investigacion_creacion_artistica", "data"),
    [Input("facultad_convocatorias_internas_investigacion_creacion_artistica", "value"), Input("anio_convocatorias_internas_investigacion_creacion_artistica", "value")])
def logros_alcanzados_convocatorias_internas_investigacion_creacion_artistica(facultad, anio):
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

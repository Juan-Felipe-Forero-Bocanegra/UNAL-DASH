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
    __name__, path='/capacitaciones-investigacion-creacion-artistica')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Actividades de fomento y fortalecimiento de la Investigación y creación artística.&actividad_param=Capacitaciones"
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
                    'Nombre de la capacitación': '',
                    'Número de asistentes': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Nombre de la capacitación'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Número de asistentes'] = a['cifra']
                    i += 1
            if i == 2:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# descripción de las capacitaciones

capacitaciones_tmp = data[['Facultad', 'Año', 'Número de asistentes']]
capacitaciones = capacitaciones_tmp.rename(
    columns={'Número de asistentes': 'cifra'})

capacitaciones['Año'] = capacitaciones['Año'].astype('str')
capacitaciones.fillna(0, inplace=True)
capacitaciones['cifra'] = capacitaciones['cifra'].astype('float')

capacitaciones = capacitaciones.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

capacitaciones.apply(lambda x: total_function(
    x['Facultad'], x['Año'], capacitaciones), axis=1)

total_capacitaciones = capacitaciones['cifra'].sum()

layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Actividades de fomento y fortalecimiento'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Capacitaciones", active=True,
                        href="/capacitaciones-investigacion-creacion-artistica")),
            dbc.NavItem(dbc.NavLink("Eventos, congresos, foros, entre otros",
                                    href="/eventos-congresos-foros-entre-otros")),
            dbc.NavItem(dbc.NavLink("Revistas indexadas",
                                    href="/revistas-indexadas-investigacion-creacion-artisticas")),
            dbc.NavItem(dbc.NavLink("Otras actividades", 
                                    href="/otras-actividades-investigacion-creacion-artistica")),
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
                                        total_capacitaciones,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "asistentes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Asistentes'),
    dcc.Graph(id="graph_asistentes_capacitaciones_investigacion_creacion_artistica",
              figure=px.bar(capacitaciones,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'asistentes'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_capacitaciones_investigacion_creacion_artistica",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_capacitaciones_investigacion_creacion_artistica",
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
                                id='logros_tabla_capacitaciones_investigacion_creacion_artistica',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_capacitaciones_investigacion_creacion_artistica", "data"),
    [Input("facultad_capacitaciones_investigacion_creacion_artistica", "value"), Input("anio_capacitaciones_investigacion_creacion_artistica", "value")])
def logros_alcanzados_capacitaciones_investigacion_creacion_artistica(facultad, anio):
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

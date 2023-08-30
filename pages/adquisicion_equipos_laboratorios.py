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
    __name__, path='/adquisicion-equipos-laboratorios')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Gestión de Laboratorios&programa_param=Proyectos de laboratorios&actividad_param=Adquisición de equipos de laboratorio con recursos de Facultad"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Equipo': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Equipo'] = a['cifra']
                    i += 1
            if i == 1:
                list.append(o)
                i = 0
                j += 1
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


# Valor ejecutado con recursos de la facultad

data_2['Año'] = data_2['Año'].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('float')

data_2.apply(lambda x: total_function(
    x['Facultad'], x['Año'], data_2), axis=1)

total_data_2 = data_2['cifra'].sum()
data_2['total'] = data_2['total'].map("{:,.2f}".format)
total_data_2 = f'{total_data_2:,}'.replace(',', ' ')
total_data_2 = '$ ' + total_data_2


layout = html.Div([
    html.H2('Gestión de Laboratorios'),
    html.H3('Proyectos de laboratorios'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Proyectos y convenios",
                        href="/formulacion-ejecucion-proyectos-y-convenios-laboratorios")),
            dbc.NavItem(dbc.NavLink("Adquisición de equipos de laboratorio", active=True,
                                    href="/adquisicion-equipos-laboratorios")),
            dbc.NavItem(dbc.NavLink("Compra de mobiliario en laboratorio",
                                    href="/compra-mobiliario-laboratorios")),
            dbc.NavItem(dbc.NavLink("Contratación externa de mantenimiento preventivo",
                                    href="/contratacion-externa-mantenimietno-preventivo-laboratorios")),
            dbc.NavItem(dbc.NavLink("Contratación externa de mantenimiento correctivo",
                                    href="/contratacion-externa-mantenimietno-correctivo-laboratorios")),
            dbc.NavItem(dbc.NavLink("Reparaciones locativas en laboratorios",
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
                                        total_data_2,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "valor ejecutado con recursos de facultad"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Valor ejecutado con recursos de facultad'),
    dcc.Graph(id="graph_valor_ejecutado_recursos_facultad_adquisicion_equipos_laboratorios",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Valor ejecutado con recursos de facultad'
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
                            id="facultad_adquisicion_equipos_laboratorios",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_adquisicion_equipos_laboratorios",
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
                                id='logros_tabla_adquisicion_equipos_laboratorios',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_adquisicion_equipos_laboratorios", "data"),
    [Input("facultad_adquisicion_equipos_laboratorios", "value"), Input("anio_adquisicion_equipos_laboratorios", "value")])
def logros_alcanzados_adquisicion_equipos_laboratorios(facultad, anio):
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

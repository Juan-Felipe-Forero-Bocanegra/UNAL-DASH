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
    __name__, path='/apoyos-socioeconomicos-estudiantes-bienestar-universitario')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Bienestar Universitario&programa_param=Área de Gestión y Fomento Socioeconómico&actividad_param=Apoyos socioeconómicos a estudiantes de la facultad"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0
    if c['informeActividadDetalle']['orden'] == 2:
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Tipo de apoyo': '',
                    'Estudiantes beneficiados': '',
                }
            if a['actividadDatoLista']['nombre'] == 'Tipo de apoyo':
                if a['indice'] == j:
                    o['Tipo de apoyo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['nombre'] == 'Estudiantes beneficiados':
                if a['indice'] == j:
                    o['Estudiantes beneficiados'] = a['cifra']
                    i += 1
            if i == 2:
                list2.append(o)
                i = 0
                j += 1


data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# estudiantes beneficiados

estudiantes_beneficiados_tmp = data_2[['Facultad', 'Año',
                                       'Estudiantes beneficiados']]
estudiantes_beneficiados = estudiantes_beneficiados_tmp.rename(
    columns={'Estudiantes beneficiados': 'cifra'})

estudiantes_beneficiados['Año'] = estudiantes_beneficiados['Año'].astype('str')
estudiantes_beneficiados.fillna(0, inplace=True)
estudiantes_beneficiados['cifra'] = estudiantes_beneficiados['cifra'].astype(
    'int')

estudiantes_beneficiados = estudiantes_beneficiados.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

estudiantes_beneficiados.apply(lambda x: total_function(
    x['Facultad'], x['Año'], estudiantes_beneficiados), axis=1)

total_estudiantes_beneficiados = estudiantes_beneficiados['cifra'].sum()


layout = html.Div([
    html.H2('Bienestar Universitario'),
    html.H3('Área de Gestión y Fomento Socioeconómico'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Apoyos socioeconómicos a estudiantes", active=True, href="/apoyos-socioeconomicos-estudiantes-bienestar-universitario")),
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
                                        total_estudiantes_beneficiados,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiante beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Estudiantes beneficiados'),
    dcc.Graph(id="graph_estudiantes_beneficiados_apoyos_socieconomicos_bienesatar_universitario",
              figure=px.bar(estudiantes_beneficiados,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes beneficiados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Apoyos'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_apoyos_socieconomicos_estudiantes_bienestar_universitario",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_apoyos_socieconomicos_estudiantes_bienestar_universitario",
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
                                id='logros_tabla_apoyos_socieconomicos_estudiantes_bienestar_universitario',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
    html.H5('Logros alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_logros_apoyos_socieconomicos_estudiantes_bienestar_universitario",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_logros_apoyos_socieconomicos_estudiantes_bienestar_universitario",
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
                                id='logros_tabla_logros_apoyos_socieconomicos_estudiantes_bienestar_universitario',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_apoyos_socieconomicos_estudiantes_bienestar_universitario", "data"),
    [Input("facultad_apoyos_socieconomicos_estudiantes_bienestar_universitario", "value"), Input("anio_apoyos_socieconomicos_estudiantes_bienestar_universitario", "value")])
def logros_alcanzados_apoyos_socieconomicos_estudiantes_bienestar_universitario(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data_2
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table


@callback(
    Output("logros_tabla_logros_apoyos_socieconomicos_estudiantes_bienestar_universitario", "data"),
    [Input("facultad_logros_apoyos_socieconomicos_estudiantes_bienestar_universitario", "value"), Input("anio_logros_apoyos_socieconomicos_estudiantes_bienestar_universitario", "value")])
def logros_alcanzados_logros_apoyos_socieconomicos_estudiantes_bienestar_universitario(facultad, anio):
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
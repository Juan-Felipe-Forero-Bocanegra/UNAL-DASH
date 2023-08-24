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
    __name__, path='/iniciativas-apoyos-estudiantes')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Acompañamiento estudiantil&actividad_param=Iniciativas de apoyo a estudiantes "
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
                    'Logro': '',
                    'Estudiantes beneficiados': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logro'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Estudiantes beneficiados'] = a['cifra']
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


# iniciativas de apoyo a estudiantes

iniciativas_tmp = data[['Facultad', 'Año', 'Estudiantes beneficiados']]
iniciativas = iniciativas_tmp.rename(
    columns={'Estudiantes beneficiados': 'cifra'})

iniciativas['Año'] = iniciativas['Año'].astype('str')
iniciativas.fillna(0, inplace=True)
iniciativas['cifra'] = iniciativas['cifra'].astype('int')

iniciativas = iniciativas.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

iniciativas.apply(lambda x: total_function(
    x['Facultad'], x['Año'], iniciativas), axis=1)

total_iniciativas = iniciativas['cifra'].sum()

layout = html.Div([
    html.H2('Formación'),
    html.H3('Acompañamiento estudiantil'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("PAES, PEAMA, Ser Pilo Paga y Generación E",
                        href="/acompanamiento-programas-especiales")),
            dbc.NavItem(dbc.NavLink("Iniciativas de apoyo a estudiantes",
                        active=True, href="/iniciativas-apoyos-estudiantes")),
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
                                        total_iniciativas,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiantes beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Estudiantes beneficiados de iniciativas de apoyos a estudiantes'),
    dcc.Graph(id="graph_estudiantes_beneficiados_iniciativas_apoyos_estudiantes",
              figure=px.bar(iniciativas,
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
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_iniciativas_apoyos_estudiantes",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_iniciativas_apoyos_estudiantes",
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
                                id='logros_tabla_iniciativas_apoyos_estudiantes',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_iniciativas_apoyos_estudiantes", "data"),
    [Input("facultad_iniciativas_apoyos_estudiantes", "value"), Input("anio_iniciativas_apoyos_estudiantes", "value")])
def logros_alcanzados_iniciativas_apoyos_estudiantes(facultad, anio):
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

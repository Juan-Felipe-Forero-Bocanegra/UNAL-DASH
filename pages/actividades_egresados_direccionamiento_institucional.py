import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/actividades-egresados-direccionamiento-institucional')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Direccionamiento Institucional&programa_param=Programa de egresados&actividad_param=Actividades con egresados"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': '',
                    'Participantes': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if a['actividadDatoLista']['orden'] == '2':
                o['Participantes'] = a['cifra']
                i += 1
            if i == 2:
                list.append(o)
                i = 0


data = pd.DataFrame(list)


participantes_tmp = data[['Facultad', 'Año', 'Participantes']]
participantes = participantes_tmp.rename(
    columns={'Participantes': 'cifra'})


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# egresados participantes

participantes['Año'] = participantes['Año'].astype('str')
participantes.fillna(0, inplace=True)
participantes['cifra'] = participantes['cifra'].astype('int')


participantes = participantes.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

participantes.apply(lambda x: total_function(
    x['Facultad'], x['Año'], participantes), axis=1)

total_participantes = participantes['cifra'].sum()


layout = html.Div([
    html.H2('Direccionamiento Institucional'),
    html.H3('Programa de egresados'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Actividades con egresados", active=True,
                                    href="/actividades-egresados-direccionamiento-institucional")),



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
                                        total_participantes,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "egresados participantes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Egresados participantes'),
    dcc.Graph(id="graph_egresados_participantes_direccionamiento_institucional",
              figure=px.bar(participantes,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Egresados participantes'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Logros alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_actividades_egresados_direccionamiento_institucional",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_actividades_egresados_direccionamiento_institucional",
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
                                id='logros_tabla_actividades_egresados_direccionamiento_institucional',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_actividades_egresados_direccionamiento_institucional", "data"),
    [Input("facultad_actividades_egresados_direccionamiento_institucional", "value"), Input("anio_actividades_egresados_direccionamiento_institucional", "value")])
def logros_alcanzados_actividades_egresados_direccionamiento_institucional(facultad, anio):
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

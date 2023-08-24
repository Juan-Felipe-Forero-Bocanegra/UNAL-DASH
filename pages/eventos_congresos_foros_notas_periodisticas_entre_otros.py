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
    __name__, path='/eventos-congresos-foros-entre-otros')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Actividades de fomento y fortalecimiento de la Investigación y creación artística.&actividad_param=Eventos, congreso, foros, notas periodísticas, entre otros"
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
                    'Nombre de la actividad': '',
                    'Número de asistentes': '',
                    'Tipo de evento': '',
                    'Presupuesto ejecutado': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Nombre de la actividad'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Número de asistentes'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Tipo de evento'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '4':
                if a['indice'] == j:
                    o['Presupuesto ejecutado'] = a['cifra']
                    i += 1
            if i == 4:
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

presupuesto_tmp = data[['Facultad', 'Año', 'Presupuesto ejecutado']]
presupuesto = presupuesto_tmp.rename(
    columns={'Presupuesto ejecutado': 'cifra'})

presupuesto['Año'] = presupuesto['Año'].astype('str')
presupuesto.fillna(0, inplace=True)
presupuesto['cifra'] = presupuesto['cifra'].astype('float')


presupuesto = presupuesto.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

presupuesto.apply(lambda x: total_function(
    x['Facultad'], x['Año'], presupuesto), axis=1)

presupuesto['total'] = presupuesto['total'].map("{:,.2f}".format)

total_presupuesto = presupuesto['cifra'].sum()
total_presupuesto = f'{total_presupuesto:,}'.replace(',', ' ')
total_presupuesto = '$ ' + total_presupuesto


data['Presupuesto ejecutado'] = data['Presupuesto ejecutado'].astype(
    'float')
data['Presupuesto ejecutado'] = '$ ' + \
    data['Presupuesto ejecutado'].map("{:,.2f}".format)


layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Actividades de fomento y fortalecimiento'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Capacitaciones",
                        href="/capacitaciones-investigacion-creacion-artistica")),
            dbc.NavItem(dbc.NavLink("Eventos, congresos, foros, entre otros", active=True,
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
                                        total_presupuesto,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "presupuesto"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Presupuesto ejecutado'),
    dcc.Graph(id="graph_presupuesto_ejecutado_eventos_congresos_foros_entre_otros",
              figure=px.bar(presupuesto,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presupuesto ejecutado'
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
                            id="facultad_eventos_congresos_foros_entre_otros",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_eventos_congresos_foros_entre_otros",
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
                                id='logros_tabla_eventos_congresos_foros_entre_otros',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_eventos_congresos_foros_entre_otros", "data"),
    [Input("facultad_eventos_congresos_foros_entre_otros", "value"), Input("anio_eventos_congresos_foros_entre_otros", "value")])
def logros_alcanzados_eventos_congresos_foros_entre_otros(facultad, anio):
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

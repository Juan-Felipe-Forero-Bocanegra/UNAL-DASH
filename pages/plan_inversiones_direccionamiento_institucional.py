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
    __name__, path='/plan-inversiones-direccionamiento-institucional')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Direccionamiento Institucional&programa_param=Plan de Acción de Facultad&actividad_param=Plan de inversiones"
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
                    'Acciones programadas': '',
                    'Acciones realizadas': '',
                    'Presupuesto asignado': '',
                    'Presupuesto ejecutado': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Acciones programadas'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Acciones realizadas'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Presupuesto asignado'] = a['cifra']
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


presupuesto_asignado_tmp = data[['Facultad', 'Año', 'Presupuesto asignado']]
presupuesto_asignado = presupuesto_asignado_tmp.rename(
    columns={'Presupuesto asignado': 'cifra'})

presupuesto_ejecutado_tmp = data[['Facultad', 'Año', 'Presupuesto ejecutado']]
presupuesto_ejecutado = presupuesto_ejecutado_tmp.rename(
    columns={'Presupuesto ejecutado': 'cifra'})


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Presupuesto asignado

presupuesto_asignado['Año'] = presupuesto_asignado['Año'].astype('str')
presupuesto_asignado.fillna(0, inplace=True)
presupuesto_asignado['cifra'] = presupuesto_asignado['cifra'].astype('float')

presupuesto_asignado = presupuesto_asignado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

presupuesto_asignado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], presupuesto_asignado), axis=1)
presupuesto_asignado['total'] = presupuesto_asignado['total'].map(
    "{:,.2f}".format)

total_presupuesto_asignado = presupuesto_asignado['cifra'].sum()
total_presupuesto_asignado = f'{total_presupuesto_asignado:,}'.replace(
    ',', ' ')
total_presupuesto_asignado = '$ ' + total_presupuesto_asignado

# Presupuesto ejecutado

presupuesto_ejecutado['Año'] = presupuesto_ejecutado['Año'].astype('str')
presupuesto_ejecutado.fillna(0, inplace=True)
presupuesto_ejecutado['cifra'] = presupuesto_ejecutado['cifra'].astype('float')

presupuesto_ejecutado = presupuesto_ejecutado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

presupuesto_ejecutado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], presupuesto_ejecutado), axis=1)
presupuesto_ejecutado['total'] = presupuesto_ejecutado['total'].map(
    "{:,.2f}".format)

total_presupuesto_ejecutado = presupuesto_ejecutado['cifra'].sum()
total_presupuesto_ejecutado = f'{total_presupuesto_ejecutado:,}'.replace(
    ',', ' ')
total_presupuesto_ejecutado = '$ ' + total_presupuesto_ejecutado


data['Presupuesto asignado'] = data['Presupuesto asignado'].astype(
    'float')
data['Presupuesto asignado'] = '$ ' + \
    data['Presupuesto asignado'].map("{:,.2f}".format)

data['Presupuesto ejecutado'] = data['Presupuesto ejecutado'].astype(
    'float')
data['Presupuesto ejecutado'] = '$ ' + \
    data['Presupuesto ejecutado'].map("{:,.2f}".format)

layout = html.Div([
    html.H2('Direccionamiento Institucional'),
    html.H3('Plan de Acción de Facultad'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Formulación del Plan de Acción", 
                                    href='/formulacion-plan-accion-direccionamiento-institucional')),
            dbc.NavItem(dbc.NavLink("Cumplimiento de metas",
                                    href='/cumplimiento-metas-plan-accion-direccionamiento-institucional')),
            dbc.NavItem(dbc.NavLink("Plan de inversiones",active=True,
                                    href='/plan-inversiones-direccionamiento-institucional')),

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
                                        total_presupuesto_asignado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiantes de pregrado beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_presupuesto_ejecutado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiantes de posgrado beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Presupuesto asignado'),
    dcc.Graph(id="graph_presupuesto_asignado_plan_inversiones_direccionamiento_institucional",
              figure=px.bar(presupuesto_asignado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presupuesto asignado'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Presupuseto ejecutado'),
    dcc.Graph(id="graph_presupuesto_ejecutado_plan_inversiones_direccionamiento_institucional",
              figure=px.bar(presupuesto_ejecutado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Presuuesto ejecutado'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Iversiones'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_plan_inversiones_direccionamiento_institucional",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_plan_inversiones_direccionamiento_institucional",
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
                                id='logros_tabla_plan_inversiones_direccionamiento_institucional',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_plan_inversiones_direccionamiento_institucional", "data"),
    [Input("facultad_plan_inversiones_direccionamiento_institucional", "value"), Input("anio_plan_inversiones_direccionamiento_institucional", "value")])
def logros_alcanzados_plan_inversiones_direccionamiento_institucional(facultad, anio):
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

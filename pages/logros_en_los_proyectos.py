import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/logros-en-los-proyectos')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Extensión, Innovación y Propiedad Intelectual&programa_param=Proyectos de extensión&actividad_param=Logros en los proyectos"
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
    if c['informeActividadDetalle']['nombre'] == 'Descripción de principales logros alcanzados':
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': ''
                }
            if a['actividadDatoLista']['nombre'] == 'Logro' and a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list2.append(o)
    if c['informeActividadDetalle']['orden'] == 3:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list3.append(o)
    if c['informeActividadDetalle']['orden'] == 4:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list4.append(o)
    if c['informeActividadDetalle']['orden'] == 5:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list5.append(o)
    if c['informeActividadDetalle']['orden'] == 6:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list6.append(o)
    if c['informeActividadDetalle']['orden'] == 7:
        o = {
                'Facultad':c['facultad'],
                'Año':c['anio'],
                'cifra': c['informeActividadDetalle']['cifra']
                }
        list7.append(o)


data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)
data_4 = pd.DataFrame(list4)
data_5 = pd.DataFrame(list5)
data_6 = pd.DataFrame(list6)
data_7 = pd.DataFrame(list7)

def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total

# Inscritos en actividades de educación continua pertenecientes a la UNAL

data_2['Año'] = data_2['Año'].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')


data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

# Inscritos en actividades de educación continua externos a la UNAL

data_3['Año'] = data_3['Año'].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()
total_data_3 = f'{total_data_3:,}'.replace(',', ' ')

# Inscritos a nivel internacional en actividades de educación continua

data_4['Año'] = data_4['Año'].astype('str')
data_4.fillna(0, inplace=True)
data_4['cifra'] = data_4['cifra'].astype('int')

data_4.apply(lambda x: total_function(x['Facultad'], x['Año'], data_4), axis=1)
total_data_4 = data_4['cifra'].sum()

# Docentes participantes en actividades de educación continua externos a la UNAL*

data_5['Año'] = data_5['Año'].astype('str')
data_5.fillna(0, inplace=True)
data_5['cifra'] = data_5['cifra'].astype('int')

data_5.apply(lambda x: total_function(x['Facultad'], x['Año'], data_5), axis=1)
total_data_5 = data_5['cifra'].sum()

# Docentes participantes en actividades de educación continua pertenecientes a la UNAL

data_6['Año'] = data_6['Año'].astype('str')
data_6.fillna(0, inplace=True)
data_6['cifra'] = data_6['cifra'].astype('int')

data_6.apply(lambda x: total_function(x['Facultad'], x['Año'], data_6), axis=1)
total_data_6 = data_6['cifra'].sum()

# Número de diplomados que se dictan en temas ambientales

data_7['Año'] = data_7['Año'].astype('str')
data_7.fillna(0, inplace=True)
data_7['cifra'] = data_7['cifra'].astype('int')

data_7.apply(lambda x: total_function(x['Facultad'], x['Año'], data_7), axis=1)
total_data_7 = data_7['cifra'].sum()

layout = html.Div([])

layout = html.Div([
    html.H2('Extensión, Innovación y Propiedad Intelectual'),
    html.H3('Proyectos de extensión'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Presentación de propuestas y cotizaciones de estudios",
                                    href="/presentacion-propuestas-y-cotizaciones-de-estudios")),
            dbc.NavItem(dbc.NavLink('Participación en procesos de contratación y convocatorias',
                                    href="/participacion-en-procesos-de-contratacion-y-convocatorias")),
            dbc.NavItem(dbc.NavLink('Participación en procesos de invitación directa',
                                    href="/participacion-en-procesos-de-invitacion-directa")),
            dbc.NavItem(dbc.NavLink('Proyectos iniciados en el año',
                                    href="/proyectos-iniciados-en-el-anio")),
            dbc.NavItem(dbc.NavLink('Logros en los proyectos',  active=True,
                                    href="/logros-en-los-proyectos")),
            dbc.NavItem(dbc.NavLink('Liquidación de proyectos',
                                    href="/liquidacion-de-proyectos")),
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
                                    html.P("inscritos en actividades de educación continua - UNAL"),
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
                                    html.P("inscritos en actividades de educación continua externos"),
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
                                    html.P("inscritos a nivel internacional en actividades de educación continua"),
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
                                        total_data_6,
                                        className="card-number",
                                    ),
                                    html.P("docentes en actividades de educación continua - UNAL"),
                                ]
                            ),
                        ),
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data_5,
                                        className="card-number",
                                    ),
                                    html.P("docentes en actividades de educación continua externos"),
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
                                    html.P("diplomados en temas ambientales"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            )
        ]),
    html.H5('Inscritos en actividades de educación continua pertenecientes a la UNAL'),
    dcc.Graph(id="graph_inscritos_educacion_continua_UNAL",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Inscritos en educación contínua de la UNAL'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Inscritos en actividades de educación continua externos a la UNAL'),
    dcc.Graph(id="graph_inscritos_educacion_continua_externos_UNAL",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Inscritos en educación contínua externos'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Inscritos a nivel internacional en actividades de educación contínua'),
    dcc.Graph(id="graph_inscritos_nivel_internacional_educacion_continua",
              figure=px.bar(data_4,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Inscritos a nivel internacional'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Docentes participantes en actividades de educación continua pertenecientes a la UNAL'),
    dcc.Graph(id="graph_docentes_educacion_continua_unal",
              figure=px.bar(data_6,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Docentes pertenicientes a la UNAL'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5(
        'Docentes participantes en actividades de educación continua externos a la UNAL'),
    dcc.Graph(id="graph_docentes_educacion_continua_externos_unal",
              figure=px.bar(data_5,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Docentes externos'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Número de diplomados que se dictan en temas ambientales'),
    dcc.Graph(id="graph_diplomados_temas_ambientales",
              figure=px.bar(data_7,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Diplomados de temas ambientales'
                            },
                            color_discrete_sequence=px.colors.qualitative.Plotly,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_logros_proyectos",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_logros_proyectos",
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
                                id='logros_table_logros_proyectos',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),

], className='layout')


@callback(
    Output("logros_table_logros_proyectos", "data"),
    [Input("facultad_logros_proyectos", "value"), Input("anio_logros_proyectos", "value")])
def logros_alcanzados_logros_proyectos(facultad, anio):
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

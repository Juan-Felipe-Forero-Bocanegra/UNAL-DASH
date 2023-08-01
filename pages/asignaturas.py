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
    __name__, path='/asignaturas')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Cursos y Asignaturas&actividad_param=Asignaturas"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []
list4 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Actividad': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Actividad'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0
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
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Temas con mayor repitencia': '',
                    'Formato': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Temas con mayor repitencia'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Formato'] = a['cifra']
                    i += 1
            if i == 2:
                list4.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)
data_3 = pd.DataFrame(list3)
data_4 = pd.DataFrame(list4)

data_4['Formato'] = data_4['Formato'].replace(['575'], 'Teórico')
data_4['Formato'] = data_4['Formato'].replace(['576'], 'Práctico')

def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total

# Número de asignaturas/módulos que se imparten sobre el medio ambiente y sostenibilidad


data_2['Año'] = data_2['Año'].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')

data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()

# Número de asignaturas/módulos que se imparten sobre paz y sociedad

data_3['Año'] = data_3['Año'].astype('str')
data_3.fillna(0, inplace=True)
data_3['cifra'] = data_3['cifra'].astype('int')

data_3.apply(lambda x: total_function(x['Facultad'], x['Año'], data_3), axis=1)
total_data_3 = data_3['cifra'].sum()


layout = html.Div([
    html.H2('Formación'),
    html.H3('Cursos y Asignaturas'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Cursos", href="/cursos")),
            dbc.NavItem(dbc.NavLink(
                "Asignaturas", active=True, href="/asignaturas")),

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
                                    html.P("asignaturas sobre medio ambiente y sostenibilidad"),
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
                                    html.P("asignaturas sobre paz y sociedad"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Asignaturas sobre medio ambiente y sostenibilidad'),
    dcc.Graph(id="graph_asignaturas_medio_ambiente_sostenibilidad",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Asignaturas sobre medio ambiente y sostenibilidad'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Asignaturas sobre paz y sociedad'),
    dcc.Graph(id="graph_asignaturas_paz_sociedad",
              figure=px.bar(data_3,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Asignaturas sobre paz y sociedad'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            barmode="group",
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            )),
    html.H5('Temas o asignaturas con mayor repitencia'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_temas_asignaturas_mayor_repitencia",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_temas_asignaturas_mayor_repitencia",
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
                                id='logros_tabla_temas_asignaturas_mayor_repitencia',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
    html.H5('Actividades realizadas para tratar las asignaturas con alta repitencia'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_actividades_tratar_asignaturas_alta_repitencia",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_actividades_tratar_asignaturas_alta_repitencia",
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
                                id='logros_tabla_actividades_tratar_asignaturas_alta_repitencia',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_temas_asignaturas_mayor_repitencia", "data"),
    [Input("facultad_temas_asignaturas_mayor_repitencia", "value"), Input("anio_temas_asignaturas_mayor_repitencia", "value")])
def logros_alcanzados_temas_asignaturas_mayor_repitencia(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_4
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data_4
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data_4
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
    

@callback(
    Output("logros_tabla_actividades_tratar_asignaturas_alta_repitencia", "data"),
    [Input("facultad_actividades_tratar_asignaturas_alta_repitencia", "value"), Input("anio_actividades_tratar_asignaturas_alta_repitencia", "value")])
def logros_alcanzados_actividades_tratar_asignaturas_alta_repitencia(facultad, anio):
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
  
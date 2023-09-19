import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/examenes-ocupacionales-docentes-ocasionales-direccionamiento-institucional')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Direccionamiento Institucional&programa_param=División de seguridad y salud en el trabajo&actividad_param=Exámenes ocupacionales de ingreso para docentes ocasionales"
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
                    'Descripción del estado': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Descripción del estado'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0
    if c['informeActividadDetalle']['orden'] == 2:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Descripción del estado': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Descripción del estado'] = a['cifra']
                i += 1
            if i == 1:
                list2.append(o)
                i = 0


data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)


layout = html.Div([
    html.H2('Direccionamiento Institucional'),
    html.H3('División de seguridad y salud en el trabajo'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Exámenes ocupacionales de ingreso para docentes ocasionales", active=True,
                                    href="/examenes-ocupacionales-docentes-ocasionales-direccionamiento-institucional")),
            dbc.NavItem(dbc.NavLink("Actividades laborales con clase de riesgo",
                                    href="/actividades-laborales-clase-riesgo-direccionamiento-institucional")),
            dbc.NavItem(dbc.NavLink("Actividades de alto riesgo de personal directo o contratistas",
                                    href="/actividades-alto-riesgo-personal-directo-o-contratista-direccionamiento-institucional")),
            dbc.NavItem(dbc.NavLink("Actos y condiciones inseguras", 
                                    href="/actos-y-condiciones-inseguras")),


        ],
        pills=True,),
    html.H5('Estado del primer semestre'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_estado_primer_semestre_examen_ocupacional_direccionamiento_institucional",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_estado_primer_semestre_examen_ocupacional_direccionamiento_institucional",
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
                                id='logros_tabla_estado_primer_semestre_examen_ocupacional_direccionamiento_institucional',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
    html.H5('Estado del segundo semestre'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_estado_segundo_semestre_examen_ocupacional_direccionamiento_institucional",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_estado_segundo_semestre_examen_ocupacional_direccionamiento_institucional",
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
                                id='logros_tabla_estado_segundo_semestre_examen_ocupacional_direccionamiento_institucional',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_estado_primer_semestre_examen_ocupacional_direccionamiento_institucional", "data"),
    [Input("facultad_estado_primer_semestre_examen_ocupacional_direccionamiento_institucional", "value"), Input("anio_estado_primer_semestre_examen_ocupacional_direccionamiento_institucional", "value")])
def logros_alcanzados_estado_primer_semestre_examen_ocupacional_direccionamiento_institucional(facultad, anio):
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


@callback(
    Output("logros_tabla_estado_segundo_semestre_examen_ocupacional_direccionamiento_institucional", "data"),
    [Input("facultad_estado_segundo_semestre_examen_ocupacional_direccionamiento_institucional", "value"), Input("anio_estado_segundo_semestre_examen_ocupacional_direccionamiento_institucional", "value")])
def logros_alcanzados_estado_segundo_semestre_examen_ocupacional_direccionamiento_institucional(facultad, anio):
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

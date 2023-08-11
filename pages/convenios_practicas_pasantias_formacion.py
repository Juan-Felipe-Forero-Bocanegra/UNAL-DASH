import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/convenios-practicas-pasantias-formacion')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Reconocimientos económicos a estudiantes&actividad_param=Convenios para prácticas y pasantías realizados en el año"
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
                    'Logro': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0

data = pd.DataFrame(list)

layout = html.Div([
    html.H2('Formación'),
    html.H3('Reconocimientos económicos a estudiantes'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Beca auxiliar docente",
                        href="/beca-auxiliar-docente")),
            dbc.NavItem(dbc.NavLink("Beca asistente docente",
                                    href="/beca-asistente-docente")),
            dbc.NavItem(dbc.NavLink("Estudiantes auxiliares",
                        href="/estudiantes-auxiliares")),
            dbc.NavItem(dbc.NavLink("Beca Exención de Derechos Académicos",
                        href="/beca-exencion-derechos-economicos")),
            dbc.NavItem(dbc.NavLink("Prácticas y pasantías",
                        href="/practicas-y-pasantias-formacion")),
            dbc.NavItem(dbc.NavLink("Convenios para prácticas y pasantías en el año",
                        active=True, href="/convenios-practicas-pasantias-formacion")),
            dbc.NavItem(dbc.NavLink("Otras becas o reconocimientos económicos",
                        href="/otras-becas-o-reconocimientos-economicos")),
        ],
        pills=True,),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_convenios_practicas_pasantias_anio_formacion",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_convenios_practicas_pasantias_anio_formacion",
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
                                id='logros_tabla_convenios_practicas_pasantias_anio_formacion',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_convenios_practicas_pasantias_anio_formacion", "data"),
    [Input("facultad_convenios_practicas_pasantias_anio_formacion", "value"), Input('anio_convenios_practicas_pasantias_anio_formacion', "value")])
def logros_alcanzados_convenios_practicas_pasantias_anio_formacion(facultad, anio):
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

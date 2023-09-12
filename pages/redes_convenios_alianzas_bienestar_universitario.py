import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/redes-convenios-alianzas-bienestar-universitario')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Bienestar Universitario&programa_param=Programa de egresados&actividad_param=Redes, Convenios y Alianzas"
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
                    'Logros alcanzados': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Logros alcanzados'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0

data = pd.DataFrame(list)

# logros alcanzados

layout = html.Div([
    html.H2('Bienestar Universitario'),
    html.H3('Programa de egresados'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Actividades con egresados",
                                    href='/actividades-egresados-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Consejería a estudiantes",
                                    href='/consejeria-estudiantes-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Dialogos con egresados",
                                    href='/dialogos-egresados-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Cátedras con egresados",
                                    href='/catedras-egresados-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink(
                "Boletines y redes sociales", href="/boletines-y-redes-sociales-bienestar-universitario")),
            dbc.NavItem(dbc.NavLink(
                "Actividades deportivas, artísticas y culturales", href="/actividades-deportivas-artisticas-culturales-egresados-bienestar-universitario")),
            dbc.NavItem(dbc.NavLink(
                "Redes, Convenios y Alianzas", active=True, href="/redes-convenios-alianzas-bienestar-universitario")),
        ],
        pills=True,),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_redes_convenios_alianzas_bienestar_universitario",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_redes_convenios_alianzas_bienestar_universitario",
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
                                id='logros_tabla_redes_convenios_alianzas_bienestar_universitario',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_redes_convenios_alianzas_bienestar_universitario", "data"),
    [Input("facultad_redes_convenios_alianzas_bienestar_universitario", "value"), Input("anio_redes_convenios_alianzas_bienestar_universitario", "value")])
def logros_alcanzados_redes_convenios_alianzas_bienestar_universitario(facultad, anio):
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

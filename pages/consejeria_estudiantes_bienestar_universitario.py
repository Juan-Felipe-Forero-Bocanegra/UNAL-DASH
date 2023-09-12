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
    __name__, path='/consejeria-estudiantes-bienestar-universitario')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Bienestar Universitario&programa_param=Programa de egresados&actividad_param=Consejerías a estudiantes"
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
                    'Estudiantes participantes': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logro'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Estudiantes participantes'] = a['cifra']
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

estudiantes_participantes_tmp = data[[
    'Facultad', 'Año', 'Estudiantes participantes']]
estudiantes_participantes = estudiantes_participantes_tmp.rename(
    columns={'Estudiantes participantes': 'cifra'})

estudiantes_participantes['Año'] = estudiantes_participantes['Año'].astype(
    'str')
estudiantes_participantes.fillna(0, inplace=True)
estudiantes_participantes['cifra'] = estudiantes_participantes['cifra'].astype(
    'int')

estudiantes_participantes = estudiantes_participantes.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

estudiantes_participantes.apply(lambda x: total_function(
    x['Facultad'], x['Año'], estudiantes_participantes), axis=1)

total_estudiantes_participantes = estudiantes_participantes['cifra'].sum()

layout = html.Div([
    html.H2('Bienestar Universitario'),
    html.H3('Programa de egresados'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Actividades con egresados",
                                    href='/actividades-egresados-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Consejería a estudiantes", active=True,
                                    href='/consejeria-estudiantes-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Dialogos con egresados",
                                    href='/dialogos-egresados-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Cátedras con egresados",
                                    href='/catedras-egresados-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink(
                "Boletines y redes sociales",  href="/boletines-y-redes-sociales-bienestar-universitario")),
            dbc.NavItem(dbc.NavLink(
                "Actividades deportivas, artísticas y culturales", href="/actividades-deportivas-artisticas-culturales-egresados-bienestar-universitario")),
            dbc.NavItem(dbc.NavLink(
                "Redes, Convenios y Alianzas",  href="/redes-convenios-alianzas-bienestar-universitario")),
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
                                        total_estudiantes_participantes,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiantes participantes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Estudiantes participantes'),
    dcc.Graph(id="graph_estudiantes_participantes_consejería_bienestar_universitario",
              figure=px.bar(estudiantes_participantes,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes participantes'
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
                            id="facultad_consejeria_estudiantes_bienestar_universitario",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_consejeria_estudiantes_bienestar_universitario",
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
                                id='logros_tabla_consejeria_estudiantes_bienestar_universitario',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_consejeria_estudiantes_bienestar_universitario", "data"),
    [Input("facultad_consejeria_estudiantes_bienestar_universitario", "value"), Input("anio_consejeria_estudiantes_bienestar_universitario", "value")])
def logros_alcanzados_consejeria_estudiantes_bienestar_universitario(facultad, anio):
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

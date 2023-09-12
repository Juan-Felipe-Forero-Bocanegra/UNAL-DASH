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
    __name__, path='/actividades-deportivas-artisticas-culturales-egresados-bienestar-universitario')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Bienestar Universitario&programa_param=Programa de egresados&actividad_param=Actividades deportivas, artísticas y culturales con egresados"
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
                    'Logros alcanzados': '',
                    'Egresados participantes': '',
                    'Tipo de actividad': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logros alcanzados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Egresados participantes'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Tipo de actividad'] = a['cifra']
                    i += 1
            if i == 3:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)

data['Tipo de actividad'] = data['Tipo de actividad'].replace(
    ['600'], 'Deportiva')
data['Tipo de actividad'] = data['Tipo de actividad'].replace(
    ['601'], 'Artistica')
data['Tipo de actividad'] = data['Tipo de actividad'].replace(
    ['602'], 'Cultural')


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Egresados participantes
egresados_participantes_tmp = data[[
    'Facultad', 'Año', 'Egresados participantes']]
egresados_participantes = egresados_participantes_tmp.rename(
    columns={'Egresados participantes': 'cifra'})

egresados_participantes['Año'] = egresados_participantes['Año'].astype('str')
egresados_participantes.fillna(0, inplace=True)
egresados_participantes['cifra'] = egresados_participantes['cifra'].astype(
    'int')

egresados_participantes = egresados_participantes.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

egresados_participantes.apply(lambda x: total_function(
    x['Facultad'], x['Año'], egresados_participantes), axis=1)

total_egresados_participantes = egresados_participantes['cifra'].sum()

# egresados por tipo de actividad

egresados_tipo_actividad_tmp = data[[
    'Facultad', 'Año', 'Egresados participantes', 'Tipo de actividad']]
egresados_tipo_actividad = egresados_tipo_actividad_tmp.rename(
    columns={'Egresados participantes': 'cifra'})

# egresados por actividad deportiva

egresados_actividad_deportiva_tmp = egresados_tipo_actividad[
    egresados_tipo_actividad['Tipo de actividad'] == 'Deportiva']
egresados_actividad_deportiva = egresados_actividad_deportiva_tmp.rename(
    columns={'Egresados participantes': 'cifra'})

egresados_actividad_deportiva['Año'] = egresados_actividad_deportiva['Año'].astype(
    'str')
egresados_actividad_deportiva.fillna(0, inplace=True)
egresados_actividad_deportiva['cifra'] = egresados_actividad_deportiva['cifra'].astype(
    'int')

egresados_actividad_deportiva = egresados_actividad_deportiva.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

egresados_actividad_deportiva.apply(lambda x: total_function(
    x['Facultad'], x['Año'], egresados_actividad_deportiva), axis=1)

total_egresados_actividad_deportiva = egresados_actividad_deportiva['cifra'].sum(
)

# egresados por actividad artistica

egresados_actividad_artistica_tmp = egresados_tipo_actividad[
    egresados_tipo_actividad['Tipo de actividad'] == 'Artistica']
egresados_actividad_artistica = egresados_actividad_artistica_tmp.rename(
    columns={'Egresados participantes': 'cifra'})

if egresados_actividad_artistica.empty:
    egresados_actividad_artistica['total'] = 0
    total_egresados_actividad_artistica = 0
else:
    egresados_actividad_artistica['Año'] = egresados_actividad_artistica['Año'].astype(
        'str')
    egresados_actividad_artistica.fillna(0, inplace=True)
    egresados_actividad_artistica['cifra'] = egresados_actividad_artistica['cifra'].astype(
        'int')

    egresados_actividad_artistica = egresados_actividad_artistica.groupby(
        ['Facultad', 'Año'])['cifra'].sum().reset_index()

    egresados_actividad_artistica.apply(lambda x: total_function(
        x['Facultad'], x['Año'], egresados_actividad_artistica), axis=1)

    total_egresados_actividad_artistica = egresados_actividad_artistica['cifra'].sum(
    )

# egresados por actividad cultural

egresados_actividad_cultural_tmp = egresados_tipo_actividad[
    egresados_tipo_actividad['Tipo de actividad'] == 'Cultural']
egresados_actividad_cultural = egresados_actividad_cultural_tmp.rename(
    columns={'Egresados participantes': 'cifra'})

egresados_actividad_cultural['Año'] = egresados_actividad_cultural['Año'].astype(
    'str')
egresados_actividad_cultural.fillna(0, inplace=True)
egresados_actividad_cultural['cifra'] = egresados_actividad_cultural['cifra'].astype(
    'int')

egresados_actividad_cultural = egresados_actividad_cultural.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

egresados_actividad_cultural.apply(lambda x: total_function(
    x['Facultad'], x['Año'], egresados_actividad_cultural), axis=1)

total_egresados_actividad_cultural = egresados_actividad_cultural['cifra'].sum(
)


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
                "Actividades deportivas, artísticas y culturales", active=True, href="/actividades-deportivas-artisticas-culturales-egresados-bienestar-universitario")),
            dbc.NavItem(dbc.NavLink(
                "Redes, Convenios y Alianzas", href="/redes-convenios-alianzas-bienestar-universitario")),
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
                                        total_egresados_participantes,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "egresados participantes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_egresados_actividad_deportiva,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "egresados en actividades deportivas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_egresados_actividad_cultural,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "egresados en actividades culturales"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_egresados_actividad_artistica,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "egresados en actividades artísticas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Egresados participantes'),
    dcc.Graph(id="graph_egresados_participantes_actividades_bienestar_universitario",
              figure=px.bar(egresados_participantes,
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
    html.H5('Egresados participantes en actividades deportivas'),
    dcc.Graph(id="graph_egresados_participantes_actividades_deportivas_bienestar_universitario",
              figure=px.bar(egresados_actividad_deportiva,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Egresados en actividades deportivas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Egresados participantes en actividades culturales'),
    dcc.Graph(id="graph_egresados_participantes_actividades_culturales_bienestar_universitario",
              figure=px.bar(egresados_actividad_cultural,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Egresados en actividades culturales'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Egresados participantes en actividades artisticas'),
    dcc.Graph(id="graph_egresados_participantes_actividades_artisticas_bienestar_universitario",
              figure=px.bar(egresados_actividad_artistica,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Egresados en actividades artisticas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
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
                            id="facultad_actividades_deportivas_artisticas_culturales_bienestar_universitario",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_actividades_deportivas_artisticas_culturales_bienestar_universitario",
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
                                id='logros_tabla_actividades_deportivas_artisticas_culturales_bienestar_universitario',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_actividades_deportivas_artisticas_culturales_bienestar_universitario", "data"),
    [Input("facultad_actividades_deportivas_artisticas_culturales_bienestar_universitario", "value"), Input("anio_actividades_deportivas_artisticas_culturales_bienestar_universitario", "value")])
def logros_alcanzados_actividades_deportivas_artisticas_culturales_bienestar_universitario(facultad, anio):
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

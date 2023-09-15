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
    __name__, path='/auditorias-desarrollo-organizacional')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Desarrollo Organizacional&programa_param=Implementación del Sistema de Gestión de Calidad&actividad_param=Auditorias"
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
                    'Entidad': '',
                    'Tipo': '',
                    'Objetivo': '',
                    'Resultados': '',
                    'Oportunidades': '',
                    'No conformidades': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Entidad'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Tipo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Objetivo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '4':
                if a['indice'] == j:
                    o['Resultados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '5':
                if a['indice'] == j:
                    o['Oportunidades'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '6':
                if a['indice'] == j:
                    o['No conformidades'] = a['cifra']
                    i += 1
            if i == 6:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)


data['Tipo'] = data['Tipo'].replace(
    ['525'], 'Interna')
data['Tipo'] = data['Tipo'].replace(
    ['526'], 'Externa')


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# oportunidades de mejora

oportunidades_tmp = data[['Facultad', 'Año', 'Oportunidades']]
oportunidades = oportunidades_tmp.rename(
    columns={'Oportunidades': 'cifra'})

oportunidades['Año'] = oportunidades['Año'].astype('str')
oportunidades.fillna(0, inplace=True)
oportunidades['cifra'] = oportunidades['cifra'].astype(
    'int')

oportunidades = oportunidades.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

oportunidades.apply(lambda x: total_function(
    x['Facultad'], x['Año'], oportunidades), axis=1)

total_oportunidades = oportunidades['cifra'].sum()


# No conformidades detectadas

no_conformidades_tmp = data[['Facultad', 'Año', 'No conformidades']]
no_conformidades = no_conformidades_tmp.rename(
    columns={'No conformidades': 'cifra'})

no_conformidades['Año'] = no_conformidades['Año'].astype('str')
no_conformidades.fillna(0, inplace=True)
no_conformidades['cifra'] = no_conformidades['cifra'].astype(
    'int')

no_conformidades = no_conformidades.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

no_conformidades.apply(lambda x: total_function(
    x['Facultad'], x['Año'], no_conformidades), axis=1)

total_no_conformidades = no_conformidades['cifra'].sum()


# oportinudades de mejora por tipo

oportunidades_tipo_tmp = data[[
    'Facultad', 'Año', 'Oportunidades', 'Tipo']]
oportunidades_tipo = oportunidades_tipo_tmp.rename(
    columns={'Oportunidades': 'cifra'})


# Oportunidades de mejora detectadas por auditorias internas

oportunidades_auditoria_interna_tmp = oportunidades_tipo[oportunidades_tipo['Tipo']
                                                         == 'Interna']
oportunidades_auditoria_interna = oportunidades_auditoria_interna_tmp.rename(
    columns={'Oportunidades': 'cifra'})


oportunidades_auditoria_interna['Año'] = oportunidades_auditoria_interna['Año'].astype(
    'str')
oportunidades_auditoria_interna.fillna(0, inplace=True)
oportunidades_auditoria_interna['cifra'] = oportunidades_auditoria_interna['cifra'].astype(
    'int')

oportunidades_auditoria_interna = oportunidades_auditoria_interna.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

oportunidades_auditoria_interna.apply(lambda x: total_function(
    x['Facultad'], x['Año'], oportunidades_auditoria_interna), axis=1)

total_oportunidades_auditoria_interna = oportunidades_auditoria_interna['cifra'].sum(
)

# Oportunidades de mejora detectadas por auditorias externas

oportunidades_auditoria_externa_tmp = oportunidades_tipo[oportunidades_tipo['Tipo']
                                                         == 'Externa']
oportunidades_auditoria_externa = oportunidades_auditoria_externa_tmp.rename(
    columns={'Oportunidades': 'cifra'})


oportunidades_auditoria_externa['Año'] = oportunidades_auditoria_externa['Año'].astype(
    'str')
oportunidades_auditoria_externa.fillna(0, inplace=True)
oportunidades_auditoria_externa['cifra'] = oportunidades_auditoria_externa['cifra'].astype(
    'int')

oportunidades_auditoria_externa = oportunidades_auditoria_externa.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

oportunidades_auditoria_externa.apply(lambda x: total_function(
    x['Facultad'], x['Año'], oportunidades_auditoria_externa), axis=1)

total_oportunidades_auditoria_externa = oportunidades_auditoria_externa['cifra'].sum(
)


# No conformidades por tipo

no_conformidades_tipo_tmp = data[[
    'Facultad', 'Año', 'No conformidades', 'Tipo']]
no_conformidades_tipo = no_conformidades_tipo_tmp.rename(
    columns={'No conformidades': 'cifra'})


# No conformidades detectadas por auditorias internas

no_conformidades_auditoria_interna_tmp = no_conformidades_tipo[no_conformidades_tipo['Tipo']
                                                               == 'Interna']
no_conformidades_auditoria_interna = no_conformidades_auditoria_interna_tmp.rename(
    columns={'No conformidades': 'cifra'})


no_conformidades_auditoria_interna['Año'] = no_conformidades_auditoria_interna['Año'].astype(
    'str')
no_conformidades_auditoria_interna.fillna(0, inplace=True)
no_conformidades_auditoria_interna['cifra'] = no_conformidades_auditoria_interna['cifra'].astype(
    'int')

no_conformidades_auditoria_interna = no_conformidades_auditoria_interna.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

no_conformidades_auditoria_interna.apply(lambda x: total_function(
    x['Facultad'], x['Año'], no_conformidades_auditoria_interna), axis=1)

total_no_conformidades_auditoria_interna = no_conformidades_auditoria_interna['cifra'].sum(
)

# No conformidades detectadas por auditorias externas

no_conformidades_auditoria_externa_tmp = no_conformidades_tipo[no_conformidades_tipo['Tipo']
                                                               == 'Externa']
no_conformidades_auditoria_externa = no_conformidades_auditoria_externa_tmp.rename(
    columns={'No conformidades': 'cifra'})

no_conformidades_auditoria_externa['Año'] = no_conformidades_auditoria_externa['Año'].astype(
    'str')
no_conformidades_auditoria_externa.fillna(0, inplace=True)
no_conformidades_auditoria_externa['cifra'] = no_conformidades_auditoria_externa['cifra'].astype(
    'int')

no_conformidades_auditoria_externa = no_conformidades_auditoria_externa.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

no_conformidades_auditoria_externa.apply(lambda x: total_function(
    x['Facultad'], x['Año'], no_conformidades_auditoria_externa), axis=1)

total_no_conformidades_auditoria_externa = no_conformidades_auditoria_externa['cifra'].sum(
)


layout = html.Div([
    html.H2('Desarrollo Organizacional'),
    html.H3('Implementación del Sistema de Gestión de Calidad'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Procesos y procedimientos",
                                    href="/procesos-y-procedimientos-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Retroalimentación con partes interesadas",
                                    href="/retroalimentacion-partes-interesadas-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Trámites y servicios",
                                    href="/tramites-servicios-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Salidas no conformes",
                                    href="/salidas-no-conformes-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Mejoramiento contínuo del SGC",
                                    href="/mejoramiento-continuo-SGC-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Auditorias",  active=True,
                                    href="/auditorias-desarrollo-organizacional")),
            dbc.NavItem(dbc.NavLink("Planes de mejoramiento y acciones correctivas",  
                                    href="/planes-mejoramiento-acciones-correctivas-desarrollo-organizacional")),

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
                                        total_oportunidades,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "oportunidades de mejora detectadas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_no_conformidades,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "No conformidades detectadas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_oportunidades_auditoria_interna,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "Oportunidades de mejora detectadas por auditoria interna"),
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
                                        total_oportunidades_auditoria_externa,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "Oportunidades de mejora detectadas por auditoria externa"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_no_conformidades_auditoria_interna,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "No conformidades detectadas por auditoria interna"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_no_conformidades_auditoria_externa,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "No conformidades detectadas por auditoria externa"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Oportunidades de mejora detectadas'),
    dcc.Graph(id="graph_oportunidades_de_mejora_auditorias_desarrollo organizacional",
              figure=px.bar(oportunidades,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Oportunidades de mejora detectadas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('No conformidades detectadas'),
    dcc.Graph(id="graph_no_conformidades_auditorias_desarrollo organizacional",
              figure=px.bar(no_conformidades,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'No conformidades detectadas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Oportunidades de mejora detectadas por auditorías internas'),
    dcc.Graph(id="graph_oportunidades_de_mejora_auditorias_internas_desarrollo organizacional",
              figure=px.bar(oportunidades_auditoria_interna,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Oportunidades de mejora detectadas por auditorías internas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Oportunidades de mejora detectadas por auditorías externas'),
    dcc.Graph(id="graph_oportunidades_de_mejora_auditorias_externas_desarrollo organizacional",
              figure=px.bar(oportunidades_auditoria_externa,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Oportunidades de mejora detectadas por auditorías externas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('No conformidades detectadas por auditorías internas'),
    dcc.Graph(id="graph_no_conformidades_auditorias_internas_desarrollo organizacional",
              figure=px.bar(no_conformidades_auditoria_interna,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'No conformidades detectadas por auditorías internas'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('No conformidades detectadas por auditorías externas'),
    dcc.Graph(id="graph_no_conformidades_auditorias_externas_desarrollo organizacional",
              figure=px.bar(no_conformidades_auditoria_externa,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'No conformidades detectadas por auditorías externas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Descripción de las auditorias'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_auditorias_desarrollo_organizacional",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_auditorias_desarrollo_organizacional",
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
                                id='logros_tabla_auditorias_desarrollo_organizacional',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_auditorias_desarrollo_organizacional", "data"),
    [Input("facultad_auditorias_desarrollo_organizacional", "value"), Input("anio_auditorias_desarrollo_organizacional", "value")])
def logros_alcanzados_auditorias_desarrollo_organizacional(facultad, anio):
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

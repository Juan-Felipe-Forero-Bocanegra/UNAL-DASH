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
    __name__, path='/movilidad-docente-investigativa-ICA')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Movilidad investigativa&actividad_param=Movilidad docente"
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
                    'Logro': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if i == 1:
                list.append(o)
                i = 0
    if c['informeActividadDetalle']['orden'] == 2:
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Docentes beneficiados': '',
                    'Tipo': '',
                    'Nivel': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Docentes beneficiados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Tipo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Nivel'] = a['cifra']
                    i += 1
            if i == 3:
                list2.append(o)
                i = 0
                j += 1

data_logros = pd.DataFrame(list)
data = pd.DataFrame(list2)

data['Tipo'] = data['Tipo'].replace(
    ['553'], 'Movilidad entrante')
data['Tipo'] = data['Tipo'].replace(
    ['554'], 'Movilidad saliente')

data['Nivel'] = data['Nivel'].replace(
    ['556'], 'Nacional')
data['Nivel'] = data['Nivel'].replace(
    ['557'], 'Internacional')


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# Total de docentes beneficiados

movilidad_docente_tmp = data[['Facultad', 'Año', 'Docentes beneficiados']]
movilidad_docente = movilidad_docente_tmp.rename(
    columns={'Docentes beneficiados': 'cifra'})

movilidad_docente['Año'] = movilidad_docente['Año'].astype('str')
movilidad_docente.fillna(0, inplace=True)
movilidad_docente['cifra'] = movilidad_docente['cifra'].astype('int')

movilidad_docente = movilidad_docente.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_docente.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_docente), axis=1)

total_movilidad_docente = movilidad_docente['cifra'].sum()


# movilidad docente por tipo

movilidad_tipo_tmp = data[[
    'Facultad', 'Año', 'Docentes beneficiados', 'Tipo']]
movilidad_tipo = movilidad_tipo_tmp.rename(
    columns={'Docentes beneficiados': 'cifra'})


# movilidad estudiantil entrante

movilidad_entrante_tmp = movilidad_tipo[movilidad_tipo['Tipo']
                                        == 'Movilidad entrante']
movilidad_entrante = movilidad_entrante_tmp.rename(
    columns={'Docentes beneficiados': 'cifra'})

movilidad_entrante['Año'] = movilidad_entrante['Año'].astype('str')
movilidad_entrante.fillna(0, inplace=True)
movilidad_entrante['cifra'] = movilidad_entrante['cifra'].astype('int')

movilidad_entrante = movilidad_entrante.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_entrante.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_entrante), axis=1)

total_movilidad_entrante = movilidad_entrante['cifra'].sum()

# movilidad estudiantil saliente

movilidad_saliente_tmp = movilidad_tipo[movilidad_tipo['Tipo']
                                        == 'Movilidad saliente']
movilidad_saliente = movilidad_saliente_tmp.rename(
    columns={'Docentes beneficiados': 'cifra'})

movilidad_saliente['Año'] = movilidad_saliente['Año'].astype('str')
movilidad_saliente.fillna(0, inplace=True)
movilidad_saliente['cifra'] = movilidad_saliente['cifra'].astype('int')

movilidad_saliente = movilidad_saliente.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_saliente.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_saliente), axis=1)

total_movilidad_saliente = movilidad_saliente['cifra'].sum()

# movilidad estudiantil por nivel

movilidad_nivel_tmp = data[[
    'Facultad', 'Año', 'Docentes beneficiados', 'Nivel']]
movilidad_nivel = movilidad_nivel_tmp.rename(
    columns={'Docentes beneficiados': 'cifra'})


# movilidad estudiantil nacional

movilidad_nacional_tmp = movilidad_nivel[movilidad_nivel['Nivel'] == 'Nacional']
movilidad_nacional = movilidad_nacional_tmp.rename(
    columns={'Docentes beneficiados': 'cifra'})

movilidad_nacional['Año'] = movilidad_nacional['Año'].astype('str')
movilidad_nacional.fillna(0, inplace=True)
movilidad_nacional['cifra'] = movilidad_nacional['cifra'].astype('int')

movilidad_nacional = movilidad_nacional.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_nacional.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_nacional), axis=1)

total_movilidad_nacional = movilidad_nacional['cifra'].sum()

# movilidad estudiantil internacional

movilidad_internacional_tmp = movilidad_nivel[movilidad_nivel['Nivel']
                                              == 'Internacional']
movilidad_internacional = movilidad_internacional_tmp.rename(
    columns={'Docentes beneficiados': 'cifra'})

movilidad_internacional['Año'] = movilidad_internacional['Año'].astype('str')
movilidad_internacional.fillna(0, inplace=True)
movilidad_internacional['cifra'] = movilidad_internacional['cifra'].astype(
    'int')

movilidad_internacional = movilidad_internacional.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_internacional.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_internacional), axis=1)

total_movilidad_internacional = movilidad_internacional['cifra'].sum()


layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Movilidad investigativa'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Movilidad estudiantil investigativa", 
                                    href='/movilidad-estudiantil-investigativa-ICA')),
            dbc.NavItem(dbc.NavLink("Movilidad docente investigativa", active=True,
                                    href='/movilidad-docente-investigativa-ICA')),

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
                                        total_movilidad_docente,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "total movilidad docente investigativa"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_entrante,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "movilidad docente investigativa entrante"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_saliente,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "movilidad docente investigativa saliente"),
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
                                        total_movilidad_nacional,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "movilidad docente investigativa nacional"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_internacional,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "movilidad docente investigativa internacional"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Total de movilidad docente investigativa'),
    dcc.Graph(id="graph_total_movilidad_docente_investigativa",
              figure=px.bar(movilidad_docente,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad docente investigativa'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad docente investigativa entrante'),
    dcc.Graph(id="graph_movilidad_docente_investigativa_entrante",
              figure=px.bar(movilidad_entrante,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad docente investigativa entrante'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad docente investigativa saliente'),
    dcc.Graph(id="graph_movilidad_docente_investigativa_saliente",
              figure=px.bar(movilidad_saliente,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad docente investigativa saliente'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad docente investigativa nacional'),
    dcc.Graph(id="graph_movilidad_docente_investigativa_nacional",
              figure=px.bar(movilidad_nacional,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad docente investigativa nacional'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad docente investigativa internacional'),
    dcc.Graph(id="graph_movilidad_docente_investigativa_internacional",
              figure=px.bar(movilidad_internacional,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad docente investigativa internacional'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Docentes beneficiados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_movilidad_docente_investigativa",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_docente_investigativa",
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
                                id='logros_tabla_movilidad_docente_investigativa',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_movilidad_docente_investigativa_logros",
                            options=data_logros['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_docente_investigativa_logros",
                            options=data_logros['Año'].unique(),
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
                                id='logros_tabla_movilidad_docente_investigativa_logros',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_movilidad_docente_investigativa", "data"),
    [Input("facultad_movilidad_docente_investigativa", "value"), Input("anio_movilidad_docente_investigativa", "value")])
def logros_alcanzados_movilidad_docente_investigativa(facultad, anio):
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
    Output("logros_tabla_movilidad_docente_investigativa_logros", "data"),
    [Input("facultad_movilidad_docente_investigativa_logros", "value"), Input("anio_movilidad_docente_investigativa_logros", "value")])
def logros_alcanzados_movilidad_docente_investigativa_logros(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_logros
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if not facultad:
            df = data_logros
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and anio:
            df = data_logros
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table

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
    __name__, path='/movilidad-tipo-ICA')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Alianzas, redes, convenios y movilidades&actividad_param=Movilidades"
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
                    'Descripción general de las movilidades realizadas': '',
                    'Modalidad de las movilidades': '',
                    'Tipo de movilidad': '',
                    'Número de movilidades realizadas por tipo': '',
                    'Monto total por tipo de movilidad': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Descripción general de las movilidades realizadas'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Modalidad de las movilidades'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Tipo de movilidad'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '4':
                if a['indice'] == j:
                    o['Número de movilidades realizadas por tipo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '5':
                if a['indice'] == j:
                    o['Monto total por tipo de movilidad'] = a['cifra']
                    i += 1
            if i == 5:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)


data['Modalidad de las movilidades'] = data['Modalidad de las movilidades'].replace(
    ['559'], 'Investigadores y artistas extranjeros')
data['Modalidad de las movilidades'] = data['Modalidad de las movilidades'].replace(
    ['560'], 'Docentes investigadores o creadores UNAL')
data['Modalidad de las movilidades'] = data['Modalidad de las movilidades'].replace(
    ['561'], 'Estudiantes de pregrado y posgrado')
data['Modalidad de las movilidades'] = data['Modalidad de las movilidades'].replace(
    ['562'], 'Pasantías de investigación o residencias artísticas de estudiantes de posgrado')

data['Tipo de movilidad'] = data['Tipo de movilidad'].replace(
    ['564'], 'Entrante')
data['Tipo de movilidad'] = data['Tipo de movilidad'].replace(
    ['565'], 'Saliente')


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# número de movilidades

numero_movilidades_tmp = data[['Facultad', 'Año',
                               'Número de movilidades realizadas por tipo']]
numero_movilidades = numero_movilidades_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})

numero_movilidades['Año'] = numero_movilidades['Año'].astype('str')
numero_movilidades.fillna(0, inplace=True)
numero_movilidades['cifra'] = numero_movilidades['cifra'].astype('int')

numero_movilidades = numero_movilidades.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

numero_movilidades.apply(lambda x: total_function(
    x['Facultad'], x['Año'], numero_movilidades), axis=1)

total_numero_movilidades = numero_movilidades['cifra'].sum()


# numero de movilidades por tipo

movilidad_tipo_tmp = data[[
    'Facultad', 'Año', 'Número de movilidades realizadas por tipo', 'Tipo de movilidad']]
movilidad_tipo = movilidad_tipo_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})


# movilidades entrante

movilidad_entrante_tmp = movilidad_tipo[movilidad_tipo['Tipo de movilidad'] == 'Entrante']
movilidad_entrante = movilidad_entrante_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})

movilidad_entrante['Año'] = movilidad_entrante['Año'].astype('str')
movilidad_entrante.fillna(0, inplace=True)
movilidad_entrante['cifra'] = movilidad_entrante['cifra'].astype('int')

movilidad_entrante = movilidad_entrante.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_entrante.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_entrante), axis=1)

total_movilidad_entrante = movilidad_entrante['cifra'].sum()

# movilidad saliente

movilidad_saliente_tmp = movilidad_tipo[movilidad_tipo['Tipo de movilidad'] == 'Saliente']
movilidad_saliente = movilidad_saliente_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})

movilidad_saliente['Año'] = movilidad_saliente['Año'].astype('str')
movilidad_saliente.fillna(0, inplace=True)
movilidad_saliente['cifra'] = movilidad_saliente['cifra'].astype('int')

movilidad_saliente = movilidad_saliente.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_saliente.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_saliente), axis=1)

total_movilidad_saliente = movilidad_saliente['cifra'].sum()

# movilidad por modalidad

movilidad_modalidad_tmp = data[[
    'Facultad', 'Año', 'Número de movilidades realizadas por tipo', 'Modalidad de las movilidades']]
movilidad_modalidad = movilidad_modalidad_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})


# movilidad por modalidad Investigadores y artistas extranjeros

movilidad_investigadores_artistas_extranjeros_tmp = movilidad_modalidad[movilidad_modalidad[
    'Modalidad de las movilidades'] == 'Investigadores y artistas extranjeros']
movilidad_investigadores_artistas_extranjeros = movilidad_investigadores_artistas_extranjeros_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})

movilidad_investigadores_artistas_extranjeros['Año'] = movilidad_investigadores_artistas_extranjeros['Año'].astype(
    'str')
movilidad_investigadores_artistas_extranjeros.fillna(0, inplace=True)
movilidad_investigadores_artistas_extranjeros['cifra'] = movilidad_investigadores_artistas_extranjeros['cifra'].astype(
    'int')

movilidad_investigadores_artistas_extranjeros = movilidad_investigadores_artistas_extranjeros.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_investigadores_artistas_extranjeros.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_investigadores_artistas_extranjeros), axis=1)

total_movilidad_investigadores_artistas_extranjeros = movilidad_investigadores_artistas_extranjeros['cifra'].sum(
)

# Docentes investigadores o creadores UNAL

movilidad_investigadores_creadores_unal_tmp = movilidad_modalidad[movilidad_modalidad[
    'Modalidad de las movilidades'] == 'Docentes investigadores o creadores UNAL']
movilidad_investigadores_creadores_unal = movilidad_investigadores_creadores_unal_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})

movilidad_investigadores_creadores_unal['Año'] = movilidad_investigadores_creadores_unal['Año'].astype(
    'str')
movilidad_investigadores_creadores_unal.fillna(0, inplace=True)
movilidad_investigadores_creadores_unal['cifra'] = movilidad_investigadores_creadores_unal['cifra'].astype(
    'int')

movilidad_investigadores_creadores_unal = movilidad_investigadores_creadores_unal.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_investigadores_creadores_unal.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_investigadores_creadores_unal), axis=1)

total_movilidad_investigadores_creadores_unal = movilidad_investigadores_creadores_unal['cifra'].sum(
)

# Estudiantes de pregrado y posgrado

movilidad_estudiantes_tmp = movilidad_modalidad[movilidad_modalidad[
    'Modalidad de las movilidades'] == 'Estudiantes de pregrado y posgrado']
movilidad_estudiantes = movilidad_estudiantes_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})

movilidad_estudiantes['Año'] = movilidad_estudiantes['Año'].astype('str')
movilidad_estudiantes.fillna(0, inplace=True)
movilidad_estudiantes['cifra'] = movilidad_estudiantes['cifra'].astype('int')

movilidad_estudiantes = movilidad_estudiantes.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_estudiantes.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_estudiantes), axis=1)

total_movilidad_estudiantes = movilidad_estudiantes['cifra'].sum()


# Pasantías de investigación o residencias artísticas de estudiantes de posgrado

pasantias_residencias_posgrado_tmp = movilidad_modalidad[movilidad_modalidad['Modalidad de las movilidades']
                                                         == 'Pasantías de investigación o residencias artísticas de estudiantes de posgrado']
pasantias_residencias_posgrado = pasantias_residencias_posgrado_tmp.rename(
    columns={'Número de movilidades realizadas por tipo': 'cifra'})

pasantias_residencias_posgrado['Año'] = pasantias_residencias_posgrado['Año'].astype(
    'str')
pasantias_residencias_posgrado.fillna(0, inplace=True)
pasantias_residencias_posgrado['cifra'] = pasantias_residencias_posgrado['cifra'].astype(
    'int')

pasantias_residencias_posgrado = pasantias_residencias_posgrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

pasantias_residencias_posgrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], pasantias_residencias_posgrado), axis=1)

total_pasantias_residencias_posgrado = pasantias_residencias_posgrado['cifra'].sum(
)


data['Monto total por tipo de movilidad'] = data['Monto total por tipo de movilidad'].astype(
    'float')
data['Monto total por tipo de movilidad'] = '$ ' + \
    data['Monto total por tipo de movilidad'].map("{:,.2f}".format)

layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Alianzas, redes, convenios y movilidades'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Alianzas, redes y convenios",
                                    href='/alianzas-redes-convenios-ICA')),
            dbc.NavItem(dbc.NavLink("Movilidades por tipo", active=True,
                                    href='/movilidad-tipo-ICA')),
            dbc.NavItem(dbc.NavLink("Monto de las movilidades ",
                                    href='/movilidad-monto-ICA')),

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
                                        total_numero_movilidades,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "número de movilidades"),
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
                                        "movilidad entrante"),
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
                                    html.P("movilidad saliente"),
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
                                        total_movilidad_investigadores_artistas_extranjeros,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "movilidad de investigadores y artistas extranjeros"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_investigadores_creadores_unal,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "movilidad docentes investigadores o cradores UNAL"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_estudiantes,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "movilidad de estudiantes pregrado y posgrado"),
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
                                        total_pasantias_residencias_posgrado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "Pasantías de investigación o residencias artísticas de estudiantes de posgrado"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Total de movilidades'),
    dcc.Graph(id="graph_total_movilidades_movilidades_tipo",
              figure=px.bar(numero_movilidades,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidades'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad entrante'),
    dcc.Graph(id="graph_movilidad_entrante_movilidades_tipo",
              figure=px.bar(movilidad_entrante,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad entrante'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad saliente'),
    dcc.Graph(id="graph_movilidad_saliente_movilidades_tipo",
              figure=px.bar(movilidad_saliente,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad saliente'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad de investigadores y artistas extranjeros'),
    dcc.Graph(id="graph_movilidad_investigadores_artistas_extranjeros",
              figure=px.bar(movilidad_investigadores_artistas_extranjeros,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad de investigadores y artistas extranjeros'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Docentes investigadores o creadores UNAL'),
    dcc.Graph(id="graph_movilidad_docentes_investigadores_creadore_unal",
              figure=px.bar(movilidad_investigadores_creadores_unal,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Docentes investigadores o creadores UNAL'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Estudiantes de pregrado y posgrado'),
    dcc.Graph(id="graph_movilidad_tipo_estudiantes_pregrado_posgrado",
              figure=px.bar(movilidad_estudiantes,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes de pregrado y posgrado'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5(
        'Pasantías de investigación o residencias artísticas de estudiantes de posgrado'),
    dcc.Graph(id="graph_movilidad_tipo_pasantias_residencias_posgrado",
              figure=px.bar(pasantias_residencias_posgrado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Pasantías de investigación o residencias artísticas de estudiantes de posgrado'
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
                            id="facultad_movilidad_tipo_ICA",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_tipo_ICA",
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
                                id='logros_tabla_movilidad_tipo_ICA',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_movilidad_tipo_ICA", "data"),
    [Input("facultad_movilidad_tipo_ICA", "value"), Input("anio_movilidad_tipo_ICA", "value")])
def logros_alcanzados_movilidad_tipo_ICA(facultad, anio):
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

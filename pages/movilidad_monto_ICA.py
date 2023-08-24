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
    __name__, path='/movilidad-monto-ICA')

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

monto_movilidades_tmp = data[['Facultad',
                              'Año', 'Monto total por tipo de movilidad']]
monto_movilidades = monto_movilidades_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

monto_movilidades['Año'] = monto_movilidades['Año'].astype('str')
monto_movilidades.fillna(0, inplace=True)
monto_movilidades['cifra'] = monto_movilidades['cifra'].astype('float')

monto_movilidades = monto_movilidades.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_movilidades.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_movilidades), axis=1)

total_monto_movilidades = monto_movilidades['cifra'].sum()
total_monto_movilidades = f'{total_monto_movilidades:,}'.replace(
    ',', ' ')
total_monto_movilidades = '$ ' + total_monto_movilidades

# monto de movilidades por tipo

monto_movilidad_tipo_tmp = data[[
    'Facultad', 'Año', 'Monto total por tipo de movilidad', 'Tipo de movilidad']]
monto_movilidad_tipo = monto_movilidad_tipo_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})


# movilidades entrante

monto_movilidad_entrante_tmp = monto_movilidad_tipo[
    monto_movilidad_tipo['Tipo de movilidad'] == 'Entrante']
monto_movilidad_entrante = monto_movilidad_entrante_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

monto_movilidad_entrante['Año'] = monto_movilidad_entrante['Año'].astype('str')
monto_movilidad_entrante.fillna(0, inplace=True)
monto_movilidad_entrante['cifra'] = monto_movilidad_entrante['cifra'].astype(
    'float')

monto_movilidad_entrante = monto_movilidad_entrante.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_movilidad_entrante.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_movilidad_entrante), axis=1)

total_monto_movilidad_entrante = monto_movilidad_entrante['cifra'].sum()
total_monto_movilidad_entrante = f'{total_monto_movilidad_entrante:,}'.replace(
    ',', ' ')
total_monto_movilidad_entrante = '$ ' + total_monto_movilidad_entrante

# movilidad saliente

monto_movilidad_saliente_tmp = monto_movilidad_tipo[
    monto_movilidad_tipo['Tipo de movilidad'] == 'Saliente']
monto_movilidad_saliente = monto_movilidad_saliente_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

monto_movilidad_saliente['Año'] = monto_movilidad_saliente['Año'].astype('str')
monto_movilidad_saliente.fillna(0, inplace=True)
monto_movilidad_saliente['cifra'] = monto_movilidad_saliente['cifra'].astype(
    'float')

monto_movilidad_saliente = monto_movilidad_saliente.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_movilidad_saliente.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_movilidad_saliente), axis=1)

total_monto_movilidad_saliente = monto_movilidad_saliente['cifra'].sum()
total_monto_movilidad_saliente = f'{total_monto_movilidad_saliente:,}'.replace(
    ',', ' ')
total_monto_movilidad_saliente = '$ ' + total_monto_movilidad_saliente

# monto movilidad por modalidad

monto_movilidad_modalidad_tmp = data[[
    'Facultad', 'Año', 'Monto total por tipo de movilidad', 'Modalidad de las movilidades']]
monto_movilidad_modalidad = monto_movilidad_modalidad_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

# movilidad por modalidad Investigadores y artistas extranjeros

monto_movilidad_investigadores_artistas_extranjeros_tmp = monto_movilidad_modalidad[monto_movilidad_modalidad[
    'Modalidad de las movilidades'] == 'Investigadores y artistas extranjeros']
monto_movilidad_investigadores_artistas_extranjeros = monto_movilidad_investigadores_artistas_extranjeros_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

monto_movilidad_investigadores_artistas_extranjeros['Año'] = monto_movilidad_investigadores_artistas_extranjeros['Año'].astype(
    'str')
monto_movilidad_investigadores_artistas_extranjeros.fillna(0, inplace=True)
monto_movilidad_investigadores_artistas_extranjeros['cifra'] = monto_movilidad_investigadores_artistas_extranjeros['cifra'].astype(
    'float')

monto_movilidad_investigadores_artistas_extranjeros = monto_movilidad_investigadores_artistas_extranjeros.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_movilidad_investigadores_artistas_extranjeros.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_movilidad_investigadores_artistas_extranjeros), axis=1)

total_monto_movilidad_investigadores_artistas_extranjeros = monto_movilidad_investigadores_artistas_extranjeros['cifra'].sum(
)
total_monto_movilidad_investigadores_artistas_extranjeros = f'{total_monto_movilidad_investigadores_artistas_extranjeros:,}'.replace(
    ',', ' ')
total_monto_movilidad_investigadores_artistas_extranjeros = '$ ' + \
    total_monto_movilidad_investigadores_artistas_extranjeros

# Docentes investigadores o creadores UNAL

monto_movilidad_investigadores_creadores_unal_tmp = monto_movilidad_modalidad[monto_movilidad_modalidad[
    'Modalidad de las movilidades'] == 'Docentes investigadores o creadores UNAL']
monto_movilidad_investigadores_creadores_unal = monto_movilidad_investigadores_creadores_unal_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

monto_movilidad_investigadores_creadores_unal['Año'] = monto_movilidad_investigadores_creadores_unal['Año'].astype(
    'str')
monto_movilidad_investigadores_creadores_unal.fillna(0, inplace=True)
monto_movilidad_investigadores_creadores_unal['cifra'] = monto_movilidad_investigadores_creadores_unal['cifra'].astype(
    'float')

monto_movilidad_investigadores_creadores_unal = monto_movilidad_investigadores_creadores_unal.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_movilidad_investigadores_creadores_unal.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_movilidad_investigadores_creadores_unal), axis=1)

total_monto_movilidad_investigadores_creadores_unal = monto_movilidad_investigadores_creadores_unal['cifra'].sum(
)

total_monto_movilidad_investigadores_creadores_unal = f'{total_monto_movilidad_investigadores_creadores_unal:,}'.replace(
    ',', ' ')
total_monto_movilidad_investigadores_creadores_unal = '$ ' + \
    total_monto_movilidad_investigadores_creadores_unal

# Estudiantes de pregrado y posgrado

monto_movilidad_estudiantes_tmp = monto_movilidad_modalidad[monto_movilidad_modalidad[
    'Modalidad de las movilidades'] == 'Estudiantes de pregrado y posgrado']
monto_movilidad_estudiantes = monto_movilidad_estudiantes_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

monto_movilidad_estudiantes['Año'] = monto_movilidad_estudiantes['Año'].astype(
    'str')
monto_movilidad_estudiantes.fillna(0, inplace=True)
monto_movilidad_estudiantes['cifra'] = monto_movilidad_estudiantes['cifra'].astype(
    'float')

monto_movilidad_estudiantes = monto_movilidad_estudiantes.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_movilidad_estudiantes.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_movilidad_estudiantes), axis=1)

total_monto_movilidad_estudiantes = monto_movilidad_estudiantes['cifra'].sum()

total_monto_movilidad_estudiantes = f'{total_monto_movilidad_estudiantes:,}'.replace(
    ',', ' ')
total_monto_movilidad_estudiantes = '$ ' + total_monto_movilidad_estudiantes

# Pasantías de investigación o residencias artísticas de estudiantes de posgrado

monto_pasantias_residencias_posgrado_tmp = monto_movilidad_modalidad[monto_movilidad_modalidad['Modalidad de las movilidades']
                                                                     == 'Pasantías de investigación o residencias artísticas de estudiantes de posgrado']
monto_pasantias_residencias_posgrado = monto_pasantias_residencias_posgrado_tmp.rename(
    columns={'Monto total por tipo de movilidad': 'cifra'})

monto_pasantias_residencias_posgrado['Año'] = monto_pasantias_residencias_posgrado['Año'].astype(
    'str')
monto_pasantias_residencias_posgrado.fillna(0, inplace=True)
monto_pasantias_residencias_posgrado['cifra'] = monto_pasantias_residencias_posgrado['cifra'].astype(
    'float')

monto_pasantias_residencias_posgrado = monto_pasantias_residencias_posgrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

monto_pasantias_residencias_posgrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], monto_pasantias_residencias_posgrado), axis=1)

total_monto_pasantias_residencias_posgrado = monto_pasantias_residencias_posgrado['cifra'].sum(
)

total_monto_pasantias_residencias_posgrado = f'{total_monto_pasantias_residencias_posgrado:,}'.replace(
    ',', ' ')
total_monto_pasantias_residencias_posgrado = '$ ' + \
    total_monto_pasantias_residencias_posgrado

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
            dbc.NavItem(dbc.NavLink("Movilidades por tipo", 
                                    href='/movilidad-tipo-ICA')),
            dbc.NavItem(dbc.NavLink("Monto de las movilidades ", active=True,
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
                                        total_monto_movilidades,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "monto de las movilidades"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_monto_movilidad_entrante,
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
                                        total_monto_movilidad_saliente,
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
                                        total_monto_movilidad_investigadores_artistas_extranjeros,
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
                                        total_monto_movilidad_investigadores_creadores_unal,
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
                                        total_monto_movilidad_estudiantes,
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
                                        total_monto_pasantias_residencias_posgrado,
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
    html.H5('Monto del total de las movilidades'),
    dcc.Graph(id="graph_monto_total_movilidades_ICA",
              figure=px.bar(monto_movilidades,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto de las movilidades'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Monto de la movilidad entrante'),
    dcc.Graph(id="graph_monto_movilidad_entrante_ICA",
              figure=px.bar(monto_movilidad_entrante,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto de la movilidad entrante'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Monto de la movilidad saliente'),
    dcc.Graph(id="graph_monto_movilidad_saliente_ICA",
              figure=px.bar(monto_movilidad_saliente,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto de la movilidad saliente'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Monto de la movilidad de investigadores y artistas extranjeros'),
    dcc.Graph(id="graph_monto_movilidad_investigadores_artistas_extranjeros",
              figure=px.bar(monto_movilidad_investigadores_artistas_extranjeros,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto de la movilidad de investigadores y artistas extranjeros'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Monto de la modalidad de docentes investigadores o creadores UNAL'),
    dcc.Graph(id="graph_monto_movilidad_docentes_investigadores_creadore_unal",
              figure=px.bar(monto_movilidad_investigadores_creadores_unal,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto de la movilidad de docentes investigadores o creadores UNAL'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Monto de la movilidad de estudiantes de pregrado y posgrado'),
    dcc.Graph(id="graph_monto_movilidad_estudiantes_pregrado_posgrado",
              figure=px.bar(monto_movilidad_estudiantes,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto de la movilidad de estudiantes de pregrado y posgrado'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5(
        'Monto de la movilidad de pasantías de investigación o residencias artísticas de estudiantes de posgrado'),
    dcc.Graph(id="graph_monto_movilidad_tipo_pasantias_residencias_posgrado",
              figure=px.bar(monto_pasantias_residencias_posgrado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Monto de las Pasantías de investigación o residencias artísticas de estudiantes de posgrado'
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
                            id="facultad_monto_movilidad_ICA",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_monto_movilidad_ICA",
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
                                id='logros_tabla_monto_movilidad_ICA',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_monto_movilidad_ICA", "data"),
    [Input("facultad_monto_movilidad_ICA", "value"), Input("anio_monto_movilidad_ICA", "value")])
def logros_alcanzados_monto_movilidad_ICA(facultad, anio):
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

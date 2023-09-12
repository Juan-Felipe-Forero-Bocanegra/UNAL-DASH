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
    __name__, path='/movilidad-estudiantil-bienestar-universitario')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Bienestar Universitario&programa_param=La movilidad como apoyo de bienestar (cultura, arte o deportes)&actividad_param=Movilidad estudiantil"
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
                    'Logros': '',
                    'Beneficiados': '',
                    'Tipo': '',
                    'Nivel': '',
                    'Valor': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logros'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Beneficiados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Tipo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '4':
                if a['indice'] == j:
                    o['Nivel'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '5':
                if a['indice'] == j:
                    o['Valor'] = a['cifra']
                    i += 1
            if i == 5:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)


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


# estudiantes beneficiados

estudiantes_beneficiados_tmp = data[['Facultad', 'Año', 'Beneficiados']]
estudiantes_beneficiados = estudiantes_beneficiados_tmp.rename(
    columns={'Beneficiados': 'cifra'})

estudiantes_beneficiados['Año'] = estudiantes_beneficiados['Año'].astype('str')
estudiantes_beneficiados.fillna(0, inplace=True)
estudiantes_beneficiados['cifra'] = estudiantes_beneficiados['cifra'].astype(
    'int')

estudiantes_beneficiados = estudiantes_beneficiados.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

estudiantes_beneficiados.apply(lambda x: total_function(
    x['Facultad'], x['Año'], estudiantes_beneficiados), axis=1)

total_estudiantes_beneficiados = estudiantes_beneficiados['cifra'].sum()


# numero de movilidades por tipo

beneficiados_tipo_tmp = data[[
    'Facultad', 'Año', 'Beneficiados', 'Tipo']]
beneficiados_tipo = beneficiados_tipo_tmp.rename(
    columns={'Beneficiados': 'cifra'})


# movilidades entrante

movilidad_entrante_tmp = beneficiados_tipo[beneficiados_tipo['Tipo']
                                           == 'Movilidad entrante']
movilidad_entrante = movilidad_entrante_tmp.rename(
    columns={'Beneficiados': 'cifra'})


if movilidad_entrante.empty:
    movilidad_entrante['total'] = 0
    total_movilidad_entrante = 0
else:
    movilidad_entrante['Año'] = movilidad_entrante['Año'].astype('str')
    movilidad_entrante.fillna(0, inplace=True)
    movilidad_entrante['cifra'] = movilidad_entrante['cifra'].astype('int')

    movilidad_entrante = movilidad_entrante.groupby(
        ['Facultad', 'Año'])['cifra'].sum().reset_index()

    movilidad_entrante.apply(lambda x: total_function(
        x['Facultad'], x['Año'], movilidad_entrante), axis=1)

    total_movilidad_entrante = movilidad_entrante['cifra'].sum()

# movilidad saliente

movilidad_saliente_tmp = beneficiados_tipo[beneficiados_tipo['Tipo']
                                           == 'Movilidad saliente']
movilidad_saliente = movilidad_saliente_tmp.rename(
    columns={'Beneficiados': 'cifra'})

movilidad_saliente['Año'] = movilidad_saliente['Año'].astype('str')
movilidad_saliente.fillna(0, inplace=True)
movilidad_saliente['cifra'] = movilidad_saliente['cifra'].astype('int')

movilidad_saliente = movilidad_saliente.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

movilidad_saliente.apply(lambda x: total_function(
    x['Facultad'], x['Año'], movilidad_saliente), axis=1)

total_movilidad_saliente = movilidad_saliente['cifra'].sum()


# beneficiados por nivel

beneficiados_nivel_tmp = data[[
    'Facultad', 'Año', 'Beneficiados', 'Nivel']]
beneficiados_nivel = beneficiados_nivel_tmp.rename(
    columns={'Beneficiados': 'cifra'})


# beneficiados por nivel nacional

beneficiados_nacional_tmp = beneficiados_nivel[beneficiados_nivel[
    'Nivel'] == 'Nacional']
beneficiados_nacional = beneficiados_nacional_tmp.rename(
    columns={'Beneficiados': 'cifra'})

beneficiados_nacional['Año'] = beneficiados_nacional['Año'].astype(
    'str')
beneficiados_nacional.fillna(0, inplace=True)
beneficiados_nacional['cifra'] = beneficiados_nacional['cifra'].astype(
    'int')

beneficiados_nacional = beneficiados_nacional.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

beneficiados_nacional.apply(lambda x: total_function(
    x['Facultad'], x['Año'], beneficiados_nacional), axis=1)

total_beneficiados_nacional = beneficiados_nacional['cifra'].sum(
)

# beneficiados nivel internacional

beneficiados_internacional_tmp = beneficiados_nivel[beneficiados_nivel[
    'Nivel'] == 'Internacional']
beneficiados_internacional = beneficiados_internacional_tmp.rename(
    columns={'Beneficiados': 'cifra'})

beneficiados_internacional['Año'] = beneficiados_internacional['Año'].astype(
    'str')
beneficiados_internacional.fillna(0, inplace=True)
beneficiados_internacional['cifra'] = beneficiados_internacional['cifra'].astype(
    'int')

beneficiados_internacional = beneficiados_internacional.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

beneficiados_internacional.apply(lambda x: total_function(
    x['Facultad'], x['Año'], beneficiados_internacional), axis=1)

total_beneficiados_internacional = beneficiados_internacional['cifra'].sum(
)

data['Valor'] = data['Valor'].astype(
    'float')
data['Valor'] = '$ ' + data['Valor'].map("{:,.2f}".format)


layout = html.Div([
    html.H2('Bienestar Universitario'),
    html.H3('La movilidad como apoyo de bienestar (cultura, arte o deportes)'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Movilidad estudiantil", active=True,
                                    href='/movilidad-estudiantil-bienestar-universitario')),
            dbc.NavItem(dbc.NavLink("Movilidad estudiantil (valor de los apoyos)", 
                                    href='/movilidad-estudiantil-valor-bienestar-universitario')),
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
                                        total_estudiantes_beneficiados,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiantes beneficiados"),
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
                                        total_beneficiados_nacional,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "nivel nacional"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_beneficiados_nacional,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "nivel internacional"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Estudiantes beneficiados'),
    dcc.Graph(id="graph_total_beneficiados_movilidad_estudiantil_bienestar_universitario",
              figure=px.bar(estudiantes_beneficiados,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes beneficiados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad entrante'),
    dcc.Graph(id="graph_movilidad_entrante_bienestar_universitario",
              figure=px.bar(movilidad_entrante,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Movilidad entrante'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Movilidad saliente'),
    dcc.Graph(id="graph_movilidad_saliente_bienestar_universitario",
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
    html.H5('Nivel nacional'),
    dcc.Graph(id="graph_nivel_nacional_bienestar_universitario",
              figure=px.bar(beneficiados_nacional,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Nivel nacional'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Nivel internacional'),
    dcc.Graph(id="graph_nivel_internacional_bienestar_universitario",
              figure=px.bar(beneficiados_internacional,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Nivel internacional'
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
                            id="facultad_movilidad_estudiantil_bienestar_universitario",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_estudiantil_bienestar_universitario",
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
                                id='logros_tabla_movilidad_estudiantil_bienestar_universitario',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_movilidad_estudiantil_bienestar_universitario", "data"),
    [Input("facultad_movilidad_estudiantil_bienestar_universitario", "value"), Input("anio_movilidad_estudiantil_bienestar_universitario", "value")])
def logros_alcanzados_movilidad_estudiantil_bienestar_universitario(facultad, anio):
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

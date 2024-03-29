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
    __name__, path='/beca-exencion-derechos-economicos')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Reconocimientos económicos a estudiantes&actividad_param=Beca Exención de Derechos Académicos"
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
                    'Estudiantes beneficiados pregrado': '',
                    'Estudiantes beneficiados posgrado': '',
                    'Suma de los reconocimientos': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logro'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Estudiantes beneficiados pregrado'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Estudiantes beneficiados posgrado'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '4':
                if a['indice'] == j:
                    o['Suma de los reconocimientos'] = a['cifra']
                    i += 1
            if i == 4:
                list.append(o)
                i = 0
                j += 1

data = pd.DataFrame(list)


estudiantes_pregrado_tmp = data[['Facultad','Año', 'Estudiantes beneficiados pregrado']]
estudiantes_pregrado = estudiantes_pregrado_tmp.rename(
    columns={'Estudiantes beneficiados pregrado': 'cifra'})

estudiantes_posgrado_tmp = data[['Facultad',
                                'Año', 'Estudiantes beneficiados posgrado']]
estudiantes_posgrado = estudiantes_posgrado_tmp.rename(
    columns={'Estudiantes beneficiados posgrado': 'cifra'})

reconocimientos_tmp = data[['Facultad', 'Año', 'Suma de los reconocimientos']]
reconocimientos = reconocimientos_tmp.rename(
    columns={'Suma de los reconocimientos': 'cifra'})


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total

# Estudiantes beneficiados pregrado


estudiantes_pregrado['Año'] = estudiantes_pregrado['Año'].astype('str')
estudiantes_pregrado.fillna(0, inplace=True)
estudiantes_pregrado['cifra'] = estudiantes_pregrado['cifra'].astype('int')

estudiantes_pregrado = estudiantes_pregrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

estudiantes_pregrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], estudiantes_pregrado), axis=1)

total_estudiantes_pregrado = estudiantes_pregrado['cifra'].sum()

# Estudiantes beneficiados posgrado

estudiantes_posgrado['Año'] = estudiantes_posgrado['Año'].astype('str')
estudiantes_posgrado.fillna(0, inplace=True)
estudiantes_posgrado['cifra'] = estudiantes_posgrado['cifra'].astype('int')

estudiantes_posgrado = estudiantes_posgrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

estudiantes_posgrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], estudiantes_posgrado), axis=1)

total_estudiantes_posgrado = estudiantes_posgrado['cifra'].sum()

# Suma de los reconocimientos

reconocimientos['Año'] = reconocimientos['Año'].astype('str')
reconocimientos.fillna(0, inplace=True)
reconocimientos['cifra'] = reconocimientos['cifra'].astype('float')

reconocimientos = reconocimientos.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

reconocimientos.apply(lambda x: total_function(
    x['Facultad'], x['Año'], reconocimientos), axis=1)
reconocimientos['total'] = reconocimientos['total'].map("{:,.2f}".format)

total_reconocimientos = reconocimientos['cifra'].sum()
total_reconocimientos = f'{total_reconocimientos:,}'.replace(',', ' ')
total_reconocimientos = '$ ' + total_reconocimientos

data['Suma de los reconocimientos'] = data['Suma de los reconocimientos'].astype(
    'float')
data['Suma de los reconocimientos'] = '$ ' + \
    data['Suma de los reconocimientos'].map("{:,.2f}".format)

layout = html.Div([
    html.H2('Formación'),
    html.H3('Gestión de programas curriculares'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Beca auxiliar docente",
                        href="/beca-auxiliar-docente")),
            dbc.NavItem(dbc.NavLink("Beca asistente docente",
                        href="/beca-asistente-docente")),
            dbc.NavItem(dbc.NavLink("Estudiantes auxiliares",
                        href="/estudiantes-auxiliares")),
            dbc.NavItem(dbc.NavLink("Beca Exención de Derechos Académicos",
                        active=True, href="/beca-exencion-derechos-economicos")),
            dbc.NavItem(dbc.NavLink("Prácticas y pasantías",
                        href="/practicas-y-pasantias-formacion")),
            dbc.NavItem(dbc.NavLink("Convenios para prácticas y pasantías en el año",
                        href="/convenios-practicas-pasantias-formacion")),
            dbc.NavItem(dbc.NavLink("Otras becas o reconocimientos económicos",
                        href="/otras-becas-o-reconocimientos-economicos")),
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
                                        total_estudiantes_pregrado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiantes de pregrado beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_estudiantes_posgrado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "estudiantes de posgrado beneficiados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_reconocimientos,
                                        className="card-number",
                                    ),
                                    html.P("suma de los reconocimientos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Estudiantes de pregrado beneficiados de becas de exención de derechos académicos'),
    dcc.Graph(id="graph_estudiantes_beneficiados_pregrado_becas_exencion_derechos_academicos",
              figure=px.bar(estudiantes_pregrado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes de pregrado beneficiados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Estudiantes de posgrado beneficiados de becas de exención de derechos académicos'),
    dcc.Graph(id="graph_estudiantes_beneficiados_posgrado_becas_exencion_derechos_academicos",
              figure=px.bar(estudiantes_posgrado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes de posgrado beneficiados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Suma de los reconocimientos de becas de exención de derechos académicos'),
    dcc.Graph(id="graph_suma_reconocimientos_becas_exencion_derechos_academicos",
              figure=px.bar(reconocimientos,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Reconocimientos de becas de exención'
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
                            id="facultad_beca_exencion_derechos_academicos",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_beca_exencion_derechos_academicos",
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
                                id='logros_tabla_beca_exencion_derechos_academicos',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_beca_exencion_derechos_academicos", "data"),
    [Input("facultad_beca_exencion_derechos_academicos", "value"), Input("anio_beca_exencion_derechos_academicos", "value")])
def logros_alcanzados_beca_exencion_derechos_academicos(facultad, anio):
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

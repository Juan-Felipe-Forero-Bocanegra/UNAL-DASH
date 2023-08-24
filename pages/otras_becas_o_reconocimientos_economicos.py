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
    __name__, path='/otras-becas-o-reconocimientos-economicos')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Formación&programa_param=Reconocimientos económicos a estudiantes&actividad_param=Otras becas o reconocimientos económicos a estudiantes"
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
                    'Estudiantes beneficiados': '',
                    'Nivel': '',
                    'Suma de los reconocimientos': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Logro'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Estudiantes beneficiados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Nivel'] = a['cifra']
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

data['Nivel'] = data['Nivel'].replace(['581'], 'Pregrado')
data['Nivel'] = data['Nivel'].replace(['582'], 'Posgrado')


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# becas
becas_tmp = data[['Facultad', 'Año', 'Estudiantes beneficiados']]
becas = becas_tmp.rename(columns={'Estudiantes beneficiados': 'cifra'})

becas['Año'] = becas['Año'].astype('str')
becas.fillna(0, inplace=True)
becas['cifra'] = becas['cifra'].astype('int')

becas = becas.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

becas.apply(lambda x: total_function(
    x['Facultad'], x['Año'], becas), axis=1)

total_becas = becas['cifra'].sum()

#becas por nivel

becas_nivel_tmp = data[['Facultad', 'Año', 'Estudiantes beneficiados', 'Nivel']]
becas_nivel = becas_nivel_tmp.rename(columns={'Estudiantes beneficiados': 'cifra'})

# becas pregrado
becas_pregrado_tmp = becas_nivel[becas_nivel['Nivel'] == 'Pregrado']
becas_pregrado = becas_pregrado_tmp.rename(
    columns={'Estudiantes beneficiados': 'cifra'})

becas_pregrado['Año'] = becas_pregrado['Año'].astype('str')
becas_pregrado.fillna(0, inplace=True)
becas_pregrado['cifra'] = becas_pregrado['cifra'].astype('int')

becas_pregrado = becas_pregrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

becas_pregrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], becas_pregrado), axis=1)

total_becas_pregrado = becas_pregrado['cifra'].sum()

# becas posgrado
becas_posgrado_tmp = becas_nivel[becas_nivel['Nivel'] == 'Posgrado']
becas_posgrado = becas_posgrado_tmp.rename(
    columns={'Estudiantes beneficiados': 'cifra'})

becas_posgrado['Año'] = becas_posgrado['Año'].astype('str')
becas_posgrado.fillna(0, inplace=True)
becas_posgrado['cifra'] = becas_posgrado['cifra'].astype('int')

becas_posgrado = becas_posgrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

becas_posgrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], becas_posgrado), axis=1)

total_becas_posgrado = becas_posgrado['cifra'].sum()

# reconocimientos
reconocimientos_tmp = data[['Facultad','Año', 'Suma de los reconocimientos']]
reconocimientos = reconocimientos_tmp.rename(
    columns={'Suma de los reconocimientos': 'cifra'})

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

# reconocimientos por nivel
reconocimientos_nivel = data[['Facultad','Año', 'Suma de los reconocimientos', 'Nivel']]

# reconocimientos pregrado
reconocimientos_pregrado_tmp = reconocimientos_nivel[reconocimientos_nivel['Nivel'] == 'Pregrado']
reconocimientos_pregrado = reconocimientos_pregrado_tmp.rename(
    columns={'Suma de los reconocimientos': 'cifra'})

reconocimientos_pregrado['Año'] = reconocimientos_pregrado['Año'].astype('str')
reconocimientos_pregrado.fillna(0, inplace=True)
reconocimientos_pregrado['cifra'] = reconocimientos_pregrado['cifra'].astype(
    'float')

reconocimientos_pregrado = reconocimientos_pregrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

reconocimientos_pregrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], reconocimientos_pregrado), axis=1)
reconocimientos_pregrado['total'] = reconocimientos_pregrado['total'].map("{:,.2f}".format)

total_reconocimientos_pregrado = reconocimientos_pregrado['cifra'].sum()
total_reconocimientos_pregrado = f'{total_reconocimientos_pregrado:,}'.replace(
    ',', ' ')
total_reconocimientos_pregrado = '$ ' + total_reconocimientos_pregrado

# reconocimientos posgrado
reconocimientos_posgrado_tmp = reconocimientos_nivel[reconocimientos_nivel['Nivel'] == 'Posgrado']
reconocimientos_posgrado = reconocimientos_posgrado_tmp.rename(
    columns={'Suma de los reconocimientos': 'cifra'})

reconocimientos_posgrado['Año'] = reconocimientos_posgrado['Año'].astype('str')
reconocimientos_posgrado.fillna(0, inplace=True)
reconocimientos_posgrado['cifra'] = reconocimientos_posgrado['cifra'].astype(
    'float')

reconocimientos_posgrado = reconocimientos_posgrado.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

reconocimientos_posgrado.apply(lambda x: total_function(
    x['Facultad'], x['Año'], reconocimientos_posgrado), axis=1)
reconocimientos_posgrado['total'] = reconocimientos_posgrado['total'].map("{:,.2f}".format)

total_reconocimientos_posgrado = reconocimientos_posgrado['cifra'].sum()
total_reconocimientos_posgrado = f'{total_reconocimientos_posgrado:,}'.replace(
    ',', ' ')
total_reconocimientos_posgrado = '$ ' + total_reconocimientos_posgrado


data['Suma de los reconocimientos'] = data['Suma de los reconocimientos'].astype(
    'float')
data['Suma de los reconocimientos'] = '$ ' + \
    data['Suma de los reconocimientos'].map("{:,.2f}".format)

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
                        href="/convenios-practicas-pasantias-formacion")),
            dbc.NavItem(dbc.NavLink("Otras becas o reconocimientos económicos",
                        active=True, href="/otras-becas-o-reconocimientos-economicos")),
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
                                        total_becas,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "becas"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_becas_pregrado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "becas de pregrado"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_becas_posgrado,
                                        className="card-number",
                                    ),
                                    html.P("becas de posgrado"),
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
                                        total_reconocimientos,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "suma de los reconocimientos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_reconocimientos_pregrado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "suma de los reconocimentos pregrado"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_reconocimientos_posgrado,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "suma de los reconocimientos posgrado"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Estudiantes beneficiados por otras becas'),
    dcc.Graph(id="graph_estudiantes_beneficiados_otras becas",
              figure=px.bar(becas,
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
    html.H5('Estudiantes de pregrado beneficiados por otras becas'),
    dcc.Graph(id="graph_estudiantes_pregrado_beneficiados_otras becas",
              figure=px.bar(becas_pregrado,
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
    html.H5('Estudiantes de posgrado beneficiados por otras becas'),
    dcc.Graph(id="graph_estudiantes_posgrado_beneficiados_otras becas",
              figure=px.bar(becas_posgrado,
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
    html.H5('Suma de los reconocimientos de otras becas'),
    dcc.Graph(id="graph_suma_reconocimientos_otras_becas",
              figure=px.bar(reconocimientos,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Reconocimientos de otras becas'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Suma de los reconocimientos de otras becas a nivel de pregrado'),
    dcc.Graph(id="graph_suma_reconocimientos_otras_becas_pregrado",
              figure=px.bar(reconocimientos_pregrado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Reconocimientos de otras becas en pregrado'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Suma de los reconocimientos de otras becas a nivel de posgrado'),
    dcc.Graph(id="graph_suma_reconocimientos_otras_becas_posgrado",
              figure=px.bar(reconocimientos_posgrado,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Reconocimientos de otras becas en posgrado'
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
                            id="facultad_otras_becas_o_recnonocimientos_economicos",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_otras_becas_o_recnonocimientos_economicos",
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
                                id='logros_tabla_otras_becas_o_recnonocimientos_economicos',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_otras_becas_o_recnonocimientos_economicos", "data"),
    [Input("facultad_otras_becas_o_recnonocimientos_economicos", "value"), Input("anio_otras_becas_o_recnonocimientos_economicos", "value")])
def logros_alcanzados_otras_becas_o_recnonocimientos_economicos(facultad, anio):
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

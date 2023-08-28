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
    __name__, path='/grupos-investigacion-ICA')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Despliegue de la investigación &actividad_param=Grupos de investigación"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        j = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Descripción general': '',
                    'Tipo': '',
                    'Número de grupos': '',
                }
            if a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Descripción general'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Tipo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Número de grupos'] = a['cifra']
                    i += 1
            if i == 3:
                list.append(o)
                i = 0
                j += 1
    if c['informeActividadDetalle']['orden'] == 2:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list2.append(o)
    if c['informeActividadDetalle']['orden'] == 3:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list3.append(o)
    if c['informeActividadDetalle']['orden'] == 4:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list4.append(o)
    if c['informeActividadDetalle']['orden'] == 5:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list5.append(o)
    if c['informeActividadDetalle']['orden'] == 6:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list6.append(o)
    if c['informeActividadDetalle']['orden'] == 7:
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list7.append(o)

data = pd.DataFrame(list)
data2 = pd.DataFrame(list2)
data3 = pd.DataFrame(list3)
data4 = pd.DataFrame(list4)
data5 = pd.DataFrame(list5)
data6 = pd.DataFrame(list6)
data7 = pd.DataFrame(list7)


data['Tipo'] = data['Tipo'].replace(
    ['567'], 'A1')
data['Tipo'] = data['Tipo'].replace(
    ['568'], 'A')
data['Tipo'] = data['Tipo'].replace(
    ['569'], 'B')
data['Tipo'] = data['Tipo'].replace(
    ['570'], 'C')
data['Tipo'] = data['Tipo'].replace(
    ['571'], 'Reconocidos')
data['Tipo'] = data['Tipo'].replace(
    ['572'], 'Registrados y avalados')
data['Tipo'] = data['Tipo'].replace(
    ['573'], 'No avalados')


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# número de grupos

numero_grupos_tmp = data[['Facultad', 'Año',
                          'Número de grupos']]
numero_grupos = numero_grupos_tmp.rename(
    columns={'Número de grupos': 'cifra'})

numero_grupos['Año'] = numero_grupos['Año'].astype('str')
numero_grupos.fillna(0, inplace=True)
numero_grupos['cifra'] = numero_grupos['cifra'].astype('int')

numero_grupos = numero_grupos.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

numero_grupos.apply(lambda x: total_function(
    x['Facultad'], x['Año'], numero_grupos), axis=1)

total_numero_grupos = numero_grupos['cifra'].sum()


# grupos por tipo

grupos_x_tipo_tmp = data[[
    'Facultad', 'Año', 'Número de grupos', 'Tipo']]
grupos_x_tipo = grupos_x_tipo_tmp.rename(
    columns={'Número de grupos': 'cifra'})


# A1

A1_tmp = grupos_x_tipo[grupos_x_tipo['Tipo'] == 'A1']
A1 = A1_tmp.rename(
    columns={'Número de grupos': 'cifra'})

A1['Año'] = A1['Año'].astype('str')
A1.fillna(0, inplace=True)
A1['cifra'] = A1['cifra'].astype('int')

A1 = A1.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

A1.apply(lambda x: total_function(
    x['Facultad'], x['Año'], A1), axis=1)

total_A1 = A1['cifra'].sum()

# A

A_tmp = grupos_x_tipo[grupos_x_tipo['Tipo'] == 'A']
A = A_tmp.rename(
    columns={'Número de grupos': 'cifra'})

A['Año'] = A['Año'].astype('str')
A.fillna(0, inplace=True)
A['cifra'] = A['cifra'].astype('int')

A = A.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

A.apply(lambda x: total_function(
    x['Facultad'], x['Año'], A), axis=1)

total_A = A['cifra'].sum()

# B

B_tmp = grupos_x_tipo[grupos_x_tipo['Tipo'] == 'B']
B = B_tmp.rename(
    columns={'Número de grupos': 'cifra'})

B['Año'] = B['Año'].astype('str')
B.fillna(0, inplace=True)
B['cifra'] = B['cifra'].astype('int')

B = B.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

B.apply(lambda x: total_function(
    x['Facultad'], x['Año'], B), axis=1)

total_B = B['cifra'].sum()

# C

C_tmp = grupos_x_tipo[grupos_x_tipo['Tipo'] == 'C']
C = C_tmp.rename(
    columns={'Número de grupos': 'cifra'})

C['Año'] = C['Año'].astype('str')
C.fillna(0, inplace=True)
C['cifra'] = C['cifra'].astype('int')

C = C.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

C.apply(lambda x: total_function(
    x['Facultad'], x['Año'], C), axis=1)

total_C = C['cifra'].sum()

# Reconocidos

Reconocidos_tmp = grupos_x_tipo[grupos_x_tipo['Tipo'] == 'Reconocidos']
Reconocidos = Reconocidos_tmp.rename(
    columns={'Número de grupos': 'cifra'})

Reconocidos['Año'] = Reconocidos['Año'].astype('str')
Reconocidos.fillna(0, inplace=True)
Reconocidos['cifra'] = Reconocidos['cifra'].astype('int')

Reconocidos = Reconocidos.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

Reconocidos.apply(lambda x: total_function(
    x['Facultad'], x['Año'], Reconocidos), axis=1)

total_reconocidos = Reconocidos['cifra'].sum()

# Registrados y avalados

Registrados_y_avalados_tmp = grupos_x_tipo[grupos_x_tipo['Tipo']
                                           == 'Registrados y avalados']
Registrados_y_avalados = Registrados_y_avalados_tmp.rename(
    columns={'Número de grupos': 'cifra'})

Registrados_y_avalados['Año'] = Registrados_y_avalados['Año'].astype('str')
Registrados_y_avalados.fillna(0, inplace=True)
Registrados_y_avalados['cifra'] = Registrados_y_avalados['cifra'].astype('int')

Registrados_y_avalados = Registrados_y_avalados.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

Registrados_y_avalados.apply(lambda x: total_function(
    x['Facultad'], x['Año'], Registrados_y_avalados), axis=1)

total_Registrados_y_avalados = Registrados_y_avalados['cifra'].sum()


# No avalados

no_avalados_tmp = grupos_x_tipo[grupos_x_tipo['Tipo'] == 'No avalados']
no_avalados = no_avalados_tmp.rename(
    columns={'Número de grupos': 'cifra'})

no_avalados['Año'] = no_avalados['Año'].astype('str')
no_avalados.fillna(0, inplace=True)
no_avalados['cifra'] = no_avalados['cifra'].astype('int')

no_avalados = no_avalados.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

no_avalados.apply(lambda x: total_function(
    x['Facultad'], x['Año'], no_avalados), axis=1)

total_no_avalados = no_avalados['cifra'].sum()

# Número de docentes

data2["Año"] = data2["Año"].astype('str')
data2.fillna(0, inplace=True)
data2['cifra'] = data2['cifra'].astype('int')

data2.apply(lambda x: total_function(x['Facultad'], x['Año'], data2), axis=1)
total_data2 = data2['cifra'].sum()

# Número de estudiantes

data3["Año"] = data3["Año"].astype('str')
data3.fillna(0, inplace=True)
data3['cifra'] = data3['cifra'].astype('int')

data3.apply(lambda x: total_function(x['Facultad'], x['Año'], data3), axis=1)
total_data3 = data3['cifra'].sum()

# Total de investigadores

data4["Año"] = data4["Año"].astype('str')
data4.fillna(0, inplace=True)
data4['cifra'] = data4['cifra'].astype('int')

data4.apply(lambda x: total_function(x['Facultad'], x['Año'], data4), axis=1)
total_data4 = data4['cifra'].sum()

# Número de mujeres

data5["Año"] = data5["Año"].astype('str')
data5.fillna(0, inplace=True)
data5['cifra'] = data5['cifra'].astype('int')

data5.apply(lambda x: total_function(x['Facultad'], x['Año'], data5), axis=1)
total_data5 = data5['cifra'].sum()

# Número de hombres

data6["Año"] = data6["Año"].astype('str')
data6.fillna(0, inplace=True)
data6['cifra'] = data6['cifra'].astype('int')

data6.apply(lambda x: total_function(x['Facultad'], x['Año'], data6), axis=1)
total_data6 = data6['cifra'].sum()

# Número de docentes con formación doctoral

data7["Año"] = data7["Año"].astype('str')
data7.fillna(0, inplace=True)
data7['cifra'] = data7['cifra'].astype('int')

data7.apply(lambda x: total_function(x['Facultad'], x['Año'], data7), axis=1)
total_data7 = data7['cifra'].sum()


layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Despliegue de la investigación '),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Semilleros de investigación", href="/semillero-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Participación docente en la investigación", href="/participacion-docente-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Apoyos económicos a los docentes (educación formal, trabajo y desarrollo humano)", href="/apoyos-economicos-docentes-educacion-trabajo-desarrollo-humano-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Grupos de investigación", active=True, href="/grupos-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Grupos de investigación por población",  href="/grupos-investigacion-poblacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Escuelas y centros de pensamiento y de excelencia",  href="/escuelas-centros-pensamiento-excelencia")),
            dbc.NavItem(dbc.NavLink(
                        "Internacionalización de la investigación", href="/internacionalizacion-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Comités (Investigación, Ética)", href="/comites-investigacion-etica-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Actualización de bases de datos (Hermes y otras)", href="/actualizacion-bases-datos-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Articulación interistitucional",  href="/articulacion-interinstitucional_ICA")),

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
                                        total_numero_grupos,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "total de grupos"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_A1,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "grupos tipo A1"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_A,
                                        className="card-number",
                                    ),
                                    html.P("grupos tipo A"),
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
                                        total_B,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "grupos tipo B"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_C,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "grupos tipo C"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_reconocidos,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "grupos reconocidos"),
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
                                        total_Registrados_y_avalados,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "grupos registrados y avalados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_no_avalados,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "grupos no avalados"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),

                ],
            ),
        ]),
    html.H5('Grupos de investigación'),
    dcc.Graph(id="graph_total_grupos_investigacion_ICA",
              figure=px.bar(numero_grupos,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos de investigación'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Grupos tipo A1'),
    dcc.Graph(id="graph_grupos_investigacion_A1_ICA",
              figure=px.bar(A1,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos de investigación A1'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Grupos tipo A'),
    dcc.Graph(id="graph_grupos_investigacion_A_ICA",
              figure=px.bar(A,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos tipo A'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Grupos tipo B'),
    dcc.Graph(id="graph_grupos_investigacion_B_ICA",
              figure=px.bar(B,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos tipo B'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Grupos tipo C'),
    dcc.Graph(id="graph_grupos_investigacion_C_ICA",
              figure=px.bar(C,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos tipo C'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Grupos reconocidos'),
    dcc.Graph(id="graph_grupos_investigacion_reconocidos_ICA",
              figure=px.bar(Reconocidos,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos reconocidos'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Grupos registrados y avalados'),
    dcc.Graph(id="graph_grupos_investigacion_registrados_avalados_ICA",
              figure=px.bar(Registrados_y_avalados,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos registrados y avalados'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Grupos no avalados'),
    dcc.Graph(id="graph_grupos_investigacion_no_avalados_ICA",
              figure=px.bar(no_avalados,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Grupos no avalados'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Descripción general de los grupos de investigación'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_descripcion_grupos_investigacion",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_descripcion_grupos_investigacion",
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
                                id='logros_tabla_descripcion_grupos_investigacion',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_descripcion_grupos_investigacion", "data"),
    [Input("facultad_descripcion_grupos_investigacion", "value"), Input("anio_descripcion_grupos_investigacion", "value")])
def logros_alcanzados_descripcion_grupos_investigacion(facultad, anio):
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

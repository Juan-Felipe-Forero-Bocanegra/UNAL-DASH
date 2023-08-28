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
    __name__, path='/grupos-investigacion-poblacion-ICA')

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
                "Grupos de investigación", href="/grupos-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Grupos de investigación por población", active=True, href="/grupos-investigacion-poblacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Escuelas y centros de pensamiento y de excelencia",  href="/escuelas-centros-pensamiento-excelencia")),
            dbc.NavItem(dbc.NavLink(
                        "Internacionalización de la investigación",  href="/internacionalizacion-investigacion-ICA")),
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
                                        total_data2,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "numero de docentes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data3,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "numero de estudiantes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data4,
                                        className="card-number",
                                    ),
                                    html.P("investigadores"),
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
                                        total_data5,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "mujeres"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data6,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "hombres"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_data7,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "investigadores con formación doctoral"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Docentes'),
    dcc.Graph(id="graph_total_grupos_investigacion_docentes_ICA",
              figure=px.bar(data2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Docentes'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Estudiantes'),
    dcc.Graph(id="graph_grupos_investigacion_estudiantes_ICA",
              figure=px.bar(data3,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Investigadores'),
    dcc.Graph(id="graph_grupos_investigacion_investigadores_ICA",
              figure=px.bar(data4,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Investigadores'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Mujeres'),
    dcc.Graph(id="graph_grupos_investigacion_mujeres_ICA",
              figure=px.bar(data5,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Mujeres'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Hombres'),
    dcc.Graph(id="graph_grupos_investigacion_hombres_ICA",
              figure=px.bar(data6,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Hombres'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Investigadores con formación doctoral'),
    dcc.Graph(id="graph_grupos_investigacion_investigadores_doctorado_ICA",
              figure=px.bar(data7,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Investigadores con formación doctoral'
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "cifra": True,
                                'total': True,
                                'Año': True},
                            barmode="group"
                            )),


], className='layout')

import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/semillero-investigacion-ICA')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Investigación y Creación Artística&programa_param=Despliegue de la investigación &actividad_param=Semilleros de investigación"
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
        o = {
            'Facultad': c['facultad'],
            'Año': c['anio'],
            'cifra': c['informeActividadDetalle']['cifra']
        }
        list2.append(o)


data = pd.DataFrame(list)
data_2 = pd.DataFrame(list2)


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total

# Estudiantes participantes


data_2['Año'] = data_2['Año'].astype('str')
data_2.fillna(0, inplace=True)
data_2['cifra'] = data_2['cifra'].astype('int')


data_2.apply(lambda x: total_function(x['Facultad'], x['Año'], data_2), axis=1)
total_data_2 = data_2['cifra'].sum()


layout = html.Div([
    html.H2('Investigación y Creación Artística'),
    html.H3('Despliegue de la investigación '),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Semilleros de investigación", active=True, href="/semillero-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Participación docente en la investigación", href="/participacion-docente-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Apoyos económicos a los docentes (educación formal, trabajo y desarrollo humano)",  href="/apoyos-economicos-docentes-educacion-trabajo-desarrollo-humano-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Grupos de investigación",  href="/grupos-investigacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Grupos de investigación por población", href="/grupos-investigacion-poblacion-ICA")),
            dbc.NavItem(dbc.NavLink(
                "Escuelas y centros de pensamiento y de excelencia", href="/escuelas-centros-pensamiento-excelencia")),
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
                                        total_data_2,
                                        className="card-number",
                                    ),
                                    html.P("Estudiantes participantes"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Estudiantes participantes'),
    dcc.Graph(id="graph_estudiantes_participantes_semillero_investigacion_ICA",
              figure=px.bar(data_2,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Estudiantes participantes'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                "total": True,
                                'Año': True},
                            barmode="group"
                            )),
    html.H5('Logros alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_semillero_investigacion_ICA",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_semillero_investigacion_ICA",
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
                                id='logros_table_semillero_investigacion_ICA',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),

], className='layout')


@callback(
    Output("logros_table_semillero_investigacion_ICA", "data"),
    [Input("facultad_semillero_investigacion_ICA", "value"), Input("anio_semillero_investigacion_ICA", "value")])
def logros_alcanzados_semillero_investigacion_ICA(facultad, anio):
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

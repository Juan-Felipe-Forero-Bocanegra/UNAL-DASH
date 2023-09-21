import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(
    __name__, path='/intervencion-espacios-fisicos-infraestructura')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + \
    "/reporte_cifras/buscarCifras?area_param=Infraestructura&programa_param=Gestión de Ordenamiento y Desarrollo Físico&actividad_param=Intervención de espacios físicos"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []

for c in dataJson:
    if c['informeActividadDetalle']['orden'] == 1:
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': '',
                    'Área (m2)': ''
                }
            if a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if a['actividadDatoLista']['orden'] == '2':
                o['Área (m2)'] = a['cifra']
                i += 1
            if i == 2:
                list.append(o)
                i = 0


data = pd.DataFrame(list)


area_tmp = data[['Facultad', 'Año', 'Área (m2)']]
area = area_tmp.rename(
    columns={'Área (m2)': 'cifra'})


def total_function(facultad, anio, dataframe):
    df_facultad = dataframe[dataframe['Facultad'] == facultad]
    df_total = df_facultad['cifra'].sum()
    df_total = format(df_total, '.2f')
    dataframe.loc[(dataframe['Facultad'] == facultad) & (
        dataframe['Año'] == anio), 'total'] = df_total


# egresados participantes

area['Año'] = area['Año'].astype('str')
area.fillna(0, inplace=True)
area['cifra'] = area['cifra'].astype('float')

area = area.groupby(
    ['Facultad', 'Año'])['cifra'].sum().reset_index()

area.apply(lambda x: total_function(
    x['Facultad'], x['Año'], area), axis=1)

total_area = area['cifra'].sum()
total_data_4 = format(total_area, '.2f')

layout = html.Div([
    html.H2('Infraestructura'),
    html.H3('Gestión de Ordenamiento y Desarrollo Físico'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Elaboración y diseño de proyectos",
                                    href="/elaboracion-y-diseno-proyectos-infraestructura")),
            dbc.NavItem(dbc.NavLink("Intervención de espacios físicos", active=True,
                                    href="/intervencion-espacios-fisicos-infraestructura")),
            dbc.NavItem(dbc.NavLink("Gestión de espacios físicos y mantenimiento", 
                                    href="/gestion-espacios-fisicos-mantenimiento-infraestructura")),

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
                                        total_area,
                                        className="card-number",
                                    ),
                                    html.P(
                                        "area intervenida (m2)"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ],
            ),
        ]),
    html.H5('Área intervenida'),
    dcc.Graph(id="graph_intervencion_espacios_infraestructura",
              figure=px.bar(area,
                            x="cifra",
                            y="Facultad",
                            color='Año',
                            labels={
                                'Facultad': 'Dependencia',
                                'cifra': 'Área intervenida'
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "cifra": True,
                                'total': True,
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
                            id="facultad_intervencion_espacios_fisicos_infraestructura",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_intervencion_espacios_fisicos_infraestructura",
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
                                id='logros_tabla_intervencion_espacios_fisicos_infraestructura',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),


], className='layout')


@callback(
    Output("logros_tabla_intervencion_espacios_fisicos_infraestructura", "data"),
    [Input("facultad_intervencion_espacios_fisicos_infraestructura", "value"), Input("anio_intervencion_espacios_fisicos_infraestructura", "value")])
def logros_alcanzados_intervencion_espacios_fisicos_infraestructura(facultad, anio):
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

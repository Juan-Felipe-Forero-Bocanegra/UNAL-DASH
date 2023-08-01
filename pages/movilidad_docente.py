import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path='/movilidad-docente')

#data = pd.read_excel('pages/movilidad_docente_2.xlsx')
#data_2 = pd.read_excel('pages/logros_md.xlsx')


f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Relaciones Interinstitucionales&programa_param=Movilidad académica&actividad_param=Movilidad docente"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

list = []
list_2 = []
for c in dataJson:
    if c['informeActividadDetalle']['nombre'] == 'Docentes beneficiados':
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
            if a['actividadDatoLista']['nombre'] == 'Docentes beneficiados' and a['actividadDatoLista']['orden'] == '1':
                if a['indice'] == j:
                    o['Docentes beneficiados'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['nombre'] == 'Tipo' and a['actividadDatoLista']['orden'] == '2':
                if a['indice'] == j:
                    o['Tipo'] = a['cifra']
                    i += 1
            if a['actividadDatoLista']['nombre'] == 'Nivel' and a['actividadDatoLista']['orden'] == '3':
                if a['indice'] == j:
                    o['Nivel'] = a['cifra']
                    i += 1
            if i == 3:
                list.append(o)
                i = 0
                j += 1
    if c['informeActividadDetalle']['nombre'] == 'Logros alcanzados':
        i = 0
        for a in c['informeActividadDetalle']['listaDatoListaValor']:
            if i == 0:
                o = {
                    'Facultad': c['facultad'],
                    'Año': c['anio'],
                    'Logro': ''
                }
            if a['actividadDatoLista']['nombre'] == 'Logro' and a['actividadDatoLista']['orden'] == '1':
                o['Logro'] = a['cifra']
                i += 1
            if i == 1:
                list_2.append(o)
                i = 0

# DOCENTES BENEFICIADOS

df = pd.DataFrame(list)
df['Nivel'] = df['Nivel'].replace(['556'], 'Nacional')
df['Nivel'] = df['Nivel'].replace(['557'], 'Internacional')
df['Tipo'] = df['Tipo'].replace(['553'], 'Movilidad entrante')
df['Tipo'] = df['Tipo'].replace(['554'], 'Movilidad saliente')
data = df

data["Año"] = data["Año"].astype('str')
data['Docentes beneficiados'] = data['Docentes beneficiados'].astype(int)

# movilidad docente nacional
movilidad_docente_nacional = data[data['Nivel'] == 'Nacional']

# movilidad docente nacional entrante
movilidad_docente_nacional_entrante = movilidad_docente_nacional[
    movilidad_docente_nacional['Tipo'] == 'Movilidad entrante']
movilidad_docente_nacional_entrante = movilidad_docente_nacional_entrante.sort_values(
    'Facultad', ascending=False)
total_movilidad_docente_nacional_entrante = movilidad_docente_nacional_entrante['Docentes beneficiados'].sum()


# movilidad docente nacional saliente
movilidad_docente_nacional_saliente = movilidad_docente_nacional[movilidad_docente_nacional['Tipo']
                                                                 == 'Movilidad saliente']
movilidad_docente_nacional_saliente = movilidad_docente_nacional_saliente.sort_values(
    'Facultad', ascending=False)
total_movilidad_docente_nacional_saliente = movilidad_docente_nacional_saliente['Docentes beneficiados'].sum(
)

# movilidad docente internacional
movilidad_docente_internacional = data[data['Nivel'] == 'Internacional']
# movilidad internacional entrante
movilidad_docente_internacional_entrante = movilidad_docente_internacional[
    movilidad_docente_internacional['Tipo'] == 'Movilidad entrante']
movilidad_docente_internacional_entrante = movilidad_docente_internacional_entrante.sort_values(
    'Facultad', ascending=False)
total_movilidad_docente_internacional_entrante = movilidad_docente_internacional_entrante['Docentes beneficiados'].sum(
)

# movilidad docente internacional saliente
movilidad_docente_internacional_saliente = movilidad_docente_internacional[
    movilidad_docente_internacional['Tipo'] == 'Movilidad saliente']
movilidad_docente_internacional_saliente = movilidad_docente_internacional_saliente.sort_values(
    'Facultad', ascending=False)
total_movilidad_docente_internacional_saliente = movilidad_docente_internacional_saliente['Docentes beneficiados'].sum(
)

# LOGROS ALCANZADOS

df_logros = pd.DataFrame(list_2)
data_2 = df_logros

layout = html.Div([
    html.H2('Relaciones Interinstitucionales'),
    html.H3('Movilidad académica'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Movilidad estudiantil",
                                    href="/movilidad-estudiantil")),
            dbc.NavItem(dbc.NavLink('Movilidad docente',
                                    active=True, href="/movilidad-docente")),
        ],
        pills=True,),
    html.H5('Docentes beneficiados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_docente_nacional_entrante,
                                        className="card-number",
                                    ),
                                    html.P("movilidad nacional entrante"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_docente_nacional_saliente,
                                        className="card-number",
                                    ),
                                    html.P("movilidad nacional saliente"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                    dbc.Col(html.Div([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        total_movilidad_docente_internacional_entrante,
                                        className="card-number",
                                    ),
                                    html.P("movilidad internacional entrante"),
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
                                        total_movilidad_docente_internacional_saliente,
                                        className="card-number",
                                    ),
                                    html.H6("movilidad internacional saliente"),
                                ]
                            ),
                        )
                    ], className='card_container'), lg=4),
                ]
            ),
        ]),
    html.H5('Movilidad nacional saliente'),
    dcc.Graph(id="graph_movilidad_docente_nacional_saliente",
              figure=px.bar(movilidad_docente_nacional_saliente,
                            x="Docentes beneficiados",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "Docentes beneficiados": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional entrante'),
    dcc.Graph(id="graph_movilidad_docente_internacional_entrante",
              figure=px.bar(movilidad_docente_internacional_entrante,
                            x="Docentes beneficiados",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Docentes beneficiados": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional saliente'),
    dcc.Graph(id="graph_movilidad_docente_internacional_saliente",
              figure=px.bar(movilidad_docente_internacional_saliente,
                            x="Docentes beneficiados",
                            y="Facultad",
                            color="Año",
                            labels={
                                'Facultad': 'Dependencia',
                                },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Docentes beneficiados": True,
                                "Año": True},
                            barmode="group"
                            )),
    html.H5('Logros Alcanzados'),
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_movilidad_docente",
                            options=data_2['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_docente",
                            options=data_2['Año'].unique(),
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
                                id='logros_table_movilidad_docente',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("logros_table_movilidad_docente", "data"),
    [Input("facultad_movilidad_docente", "value"), Input("anio_movilidad_docente", "value")])
def logros_alcanzados_movilidad_docente(facultad, anio):
    if facultad or anio:
        if not anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            data = df.to_dict('records')
            return data
        if not facultad:
            df = data_2
            df = df[df['Año'] == anio]
            data = df.to_dict('records')
            return data
        if facultad and anio:
            df = data_2
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            data = df.to_dict('records')
            return data
    df = data_2
    data = df.to_dict('records')
    return data

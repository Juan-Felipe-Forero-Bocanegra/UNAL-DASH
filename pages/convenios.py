import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc
from flask import session
import requests

dash.register_page(__name__, path='/convenios')

#data = pd.read_excel('pages/convenios.xlsx')

f = open("file.txt", "r")
token = f.readline()
e = open("environment.txt", "r")
environment = e.readline()
url = environment + "/reporte_cifras/buscarCifras?area_param=Relaciones Interinstitucionales&programa_param=Convenios&actividad_param=Convenios"
headers = {'Content-type': 'application/json', 'Authorization': token}
r = requests.get(url, headers=headers)
dataJson = r.json()

# DESCRIPCIÓN DE LOS CONVENIOS

list = []
for c in dataJson:
  if c['informeActividadDetalle']['nombre'] == 'Descripción de los convenios':          
    i = 0
    j = 0
    for a in c['informeActividadDetalle']['listaDatoListaValor']:
      if i == 0:
        o = {
             'Facultad':c['facultad'],
             'Año':c['anio'],
             'Logro':'' ,
             'Entidades':'',
             'Área': '',
             'Tipo': ''                     
              } 
      if a['actividadDatoLista']['nombre'] == 'Logro' and a['actividadDatoLista']['orden'] == '1':
        if a['indice'] == j:
            o['Logro'] = a['cifra']
            i += 1
      if a['actividadDatoLista']['nombre'] == 'Entidades' and a['actividadDatoLista']['orden'] == '2':
        if a['indice'] == j:
            o['Entidades'] = a['cifra']
            i += 1
      if a['actividadDatoLista']['nombre'] == 'Área' and a['actividadDatoLista']['orden'] == '3':
        if a['indice'] == j:
            o['Área'] = a['cifra']
            i += 1
      if a['actividadDatoLista']['nombre'] == 'Tipo' and a['actividadDatoLista']['orden'] == '4':
        if a['indice'] == j:
            o['Tipo'] = a['cifra']
            i += 1            
      if i == 4: 
        list.append(o)
        i = 0 
        j += 1 

df = pd.DataFrame(list)

areas = {
    '528': 'Académica',
    '529': 'Investigativa',
    '530': 'Cultural',
    '531': 'Deportiva',
    '532': 'Artística',
    '533': 'Editorial',
    '534': 'Laboratorios',
    '535': 'Otro'
}
tipo = {
    '537': 'Cooperación académica',
    '538': 'Prácticas y pasantías',
    '539': 'Acuerdo Tripartita',
    '540': 'Cooperación e intercambio académico',
    '541': 'Adhesión a Redes',
    '542': 'Erasmus',
    '543': 'Oferta de programas',
    '544': 'Académicos',
    '545': 'Intercambio',
    '546': 'Estancia de investigación',
    '547': 'Subvención',
    '548': 'Cotutela doble titulación',
    '549': 'Doble titulación',
    '550': 'Marco',
    '551': 'Otro'
}

df['Área'] = df['Área'].apply(lambda x: areas[x]) 
df['Tipo'] = df['Tipo'].apply(lambda x: tipo[x]) 

data = df

data = data.iloc[1:]
new_cols = ["Facultad", "Año", "Área", "Tipo", 'Entidades', 'Logro']
data = data[new_cols]



layout = html.Div([
    html.H2('Relaciones Interinstitucionales'),
    html.H3('Convenios'),
    html.P(id='p-output'),
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink(
                "Convenios", active=True, href="/convenios")),
            dbc.NavItem(dbc.NavLink('Fortalecimiento de redes',
                                    href="/fortalecimiento-de-redes")),
        ],
        pills=True,),
    html.H5('Descripción de los convenios'),    
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="facultad_convenios",
                            options=data['Facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=4),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_convenios",
                            options=data['Año'].unique(),
                            clearable=True,
                            placeholder="Seleccione el año",
                        ),
                    ]), lg=4),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="Área_convenios",
                            options=data['Área'].unique(),
                            clearable=True,
                            placeholder="Seleccione el área",
                        ),
                    ]), lg=4),
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
                                        'backgroundColor':'rgb(29, 105, 150, 0.1)',
                                    }
                                ],
                                id='convenios',
                            ),
                        ], style={'paddingTop': '2%'})
                    )
                ]
            )
        ]),
], className='layout')


@callback(
    Output("convenios", "data"),
    [Input("facultad_convenios", "value"), Input("anio_convenios", "value"), Input("Área_convenios", "value")])
def convenios(facultad, anio, area):
    if area or anio or facultad:
        if not anio and not facultad:
            df = data
            df = df[df['Área'] == area]
            table = df.to_dict('records')
            return table
        if not area and not facultad:
            df = data
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if not area and not anio:
            df = data
            df = df[df['Facultad'] == facultad]
            table = df.to_dict('records')
            return table
        if facultad and area and not anio:
            df = data
            df = df[df['Facultad'] == facultad]
            df = df[df['Área'] == area]
            table = df.to_dict('records')
            return table
        if facultad and anio and not area:
            df = data
            df = df[df['Facultad'] == facultad]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if area and anio and not facultad:
            df = data
            df = df[df['Área'] == area]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
        if facultad and area and anio:
            df = data
            df = df[df['Facultad'] == facultad]
            df = df[df['Área'] == area]
            df = df[df['Año'] == anio]
            table = df.to_dict('records')
            return table
    df = data
    table = df.to_dict('records')
    return table




@callback(
    Output("p-output", "children"),
    Input("store", "data"),
)
def update(store):
    return 'Got token ' + store.get('token')


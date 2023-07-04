import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/movilidad-docente')

data = pd.read_excel('pages/movilidad_docente_2.xlsx')
data_2 = pd.read_excel('pages/logros_md.xlsx')

data["anio"] = data["anio"].astype('str')

# movilidad docente nacional
movilidad_docente_nacional = data[data['Nivel'] == 'Nacional']

# movilidad docente nacional entrante
movilidad_docente_nacional_entrante = movilidad_docente_nacional[
    movilidad_docente_nacional['Tipo'] == 'Movilidad entrante']
movilidad_docente_nacional_entrante = movilidad_docente_nacional_entrante.sort_values(
    'facultad', ascending=False)
total_movilidad_docente_nacional_entrante = movilidad_docente_nacional_entrante['Docentes beneficiados'].sum(
)


# movilidad docente nacional saliente
movilidad_docente_nacional_saliente = movilidad_docente_nacional[movilidad_docente_nacional['Tipo']
                                                                 == 'Movilidad saliente']
movilidad_docente_nacional_saliente = movilidad_docente_nacional_saliente.sort_values(
    'facultad', ascending=False)
total_movilidad_docente_nacional_saliente = movilidad_docente_nacional_saliente['Docentes beneficiados'].sum(
)

# movilidad docente internacional
movilidad_docente_internacional = data[data['Nivel'] == 'Internacional']
# movilidad internacional entrante
movilidad_docente_internacional_entrante = movilidad_docente_internacional[
    movilidad_docente_internacional['Tipo'] == 'Movilidad entrante']
movilidad_docente_internacional_entrante = movilidad_docente_internacional_entrante.sort_values(
    'facultad', ascending=False)
total_movilidad_docente_internacional_entrante = movilidad_docente_internacional_entrante['Docentes beneficiados'].sum(
)

# movilidad docente internacional saliente
movilidad_docente_internacional_saliente = movilidad_docente_internacional[
    movilidad_docente_internacional['Tipo'] == 'Movilidad saliente']
movilidad_docente_internacional_saliente = movilidad_docente_internacional_saliente.sort_values(
    'facultad', ascending=False)
total_movilidad_docente_internacional_saliente = movilidad_docente_internacional_saliente['Docentes beneficiados'].sum(
)


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
                            y="facultad",
                            color="anio",
                            labels={
                                'facultad': 'Dependencia',
                                'anio': 'año',
                            },
                            color_discrete_sequence=px.colors.qualitative.Prism,
                            hover_data={
                                "Docentes beneficiados": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional entrante'),
    dcc.Graph(id="graph_movilidad_docente_internacional_entrante",
              figure=px.bar(movilidad_docente_internacional_entrante,
                            x="Docentes beneficiados",
                            y="facultad",
                            color="anio",
                            labels={
                                'facultad': 'Dependencia',
                                'anio': 'año',
                            },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Docentes beneficiados": True,
                                "anio": True},
                            barmode="group"
                            )),
    html.H5('Movilidad internacional saliente'),
    dcc.Graph(id="graph_movilidad_docente_internacional_saliente",
              figure=px.bar(movilidad_docente_internacional_saliente,
                            x="Docentes beneficiados",
                            y="facultad",
                            color="anio",
                            labels={
                                'facultad': 'Dependencia',
                                'anio': 'año', },
                            color_discrete_sequence=px.colors.qualitative.G10,
                            hover_data={
                                "Docentes beneficiados": True,
                                "anio": True},
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
                            options=data_2['facultad'].unique(),
                            clearable=True,
                            placeholder="Seleccione la facultad",
                        ),
                    ]), lg=6),
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id="anio_movilidad_docente",
                            options=data_2['anio'].unique(),
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
            df = df[df['facultad'] == facultad]
            data = df.to_dict('records')
            return data
        if not facultad:
            df = data_2
            df = df[df['anio'] == anio]
            data = df.to_dict('records')
            return data
        if facultad and anio:
            df = data_2
            df = df[df['facultad'] == facultad]
            df = df[df['anio'] == anio]
            data = df.to_dict('records')
            return data
    df = data_2
    data = df.to_dict('records')
    return data

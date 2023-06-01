import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import requests, json

app = Dash(__name__, use_pages=True)

'''
url = "http://localhost:8070/authenticate"
data = {'username': 'jforerobo', 'password': 'T$Cc#s7%hPqk'}
headers = {'Content-type': 'application/json'}
r = requests.post(url, json=data)
jsonResponse = r.json()
token = 'Bearer ' + jsonResponse['token']
print(token)
 '''

app.layout = html.Div([
	
    dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Convenios", href='/convenios'),
                dbc.DropdownMenuItem("Fortalecimiento de redes", href="/fortalecimiento-de-redes"),
                dbc.DropdownMenuItem('Movilidad docente', href="/movilidad-docente"),
		        dbc.DropdownMenuItem('Movilidad estudiantil', href="/movilidad-estudiantil"),
            ],
            nav=True,
            in_navbar=True,
            label="Relaciones interinstitucionales",
        ),
    ],
    brand="Prig Data App",
    brand_href="/convenios",
    color="light",
    dark=False,
    ),
     html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
      
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)
# app.py
# Importaciones de librerías
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_cytoscape as cyto

#Importaciones de carpetas y funciones
from layouts.navbar import navbar
from layouts.form_page import form_page
from utils.visualization import update_network,update_network_personalizado
from helpers.form import get_form_data
from layouts.general_layouts import upload_component
# Crear la aplicación de Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, "style.css"])

# Crear el diseño de la aplicación
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='form-data-store'),
    navbar,
    html.Div(id='page-content')
])
# Callbacks para manejar la navegación y el almacenamiento de datos del formulario
@app.callback(
    Output('form-data-store', 'data'),
    [Input('aceptar', 'n_clicks')],
    [State('n-nodes-input', 'value'),
     State('is-complete-input', 'value'),
     State('is-connected-input', 'value'),
     State('is-weighted-input', 'value'),
     State('is-directed-input', 'value')]
)
def store_form_data(n_clicks, n_nodes, is_complete, is_connected, is_weighted, is_directed):
    if n_clicks:
        return {
            'n_nodes': n_nodes,
            'is_complete': is_complete,
            'is_connected': is_connected,
            'is_weighted': is_weighted,
            'is_directed': is_directed,
        }

# Callback para mostrar la página correspondiente
@app.callback(
    Output('page-content', 'children'),
    [Input('form-data-store', 'data')],
    [Input('url', 'pathname')]
)
def display_page(form_data, pathname):
    if pathname == '/formulario':
        return form_page
    if pathname == '/aleatorio':
            elements, stylesheet = update_network()
            return get_graph_div(elements, stylesheet)
    if pathname == '/personalizado':
            # Aquí puedes utilizar los datos del formulario para personalizar la página
            elements, stylesheet = grafo_personalizado(form_data)
            return get_graph_div(elements, stylesheet)
    if pathname == '/cargar-json':
        # TODO: Agregar la página para cargar un archivo JSON
        return  upload_component
    else:
        return "Esta es la página de inicio"  # Puedes reemplazar esto con tu propia página de inicio

# función para obtener el div del grafo de la red
def get_graph_div(elements, stylesheet=None):
    return html.Div(id='network-graph-container', className="container", children=[
        dcc.Loading(
            id="loading-graph",
            type="circle",
            children=[
                cyto.Cytoscape(
                    id='network-graph',
                    layout={'name': 'random'},
                    style={'width': '100%', 'height': '800px'},
                    stylesheet=stylesheet,
                    elements=elements
                ),
            ]
        )
    ])

def grafo_personalizado(form_data):
    n_nodes, is_complete, is_connected, is_weighted, is_directed = get_form_data(form_data)
    if n_nodes is not None:
        return update_network_personalizado(n_nodes, is_weighted, is_directed, is_connected, is_complete)
    return None, None

if __name__ == '__main__':
    app.run_server(debug=True)


# TODO : A La pantalla podria agregarsele botones para crear, eliminar y modificar nodos y aristas
# TODO : 
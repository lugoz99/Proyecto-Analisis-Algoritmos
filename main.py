# app.py
# Importaciones de librerías
import json
import random
import string
import time
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
#Importaciones de carpetas y funciones
from layouts.navbar import header
from layouts.form_page import modal
from utils.visualization import update_network,update_network_personalizado,load_json_file
from helpers.form import get_form_data
from layouts.general_layouts import rename_file
from callbacks.callbacks import register_callbacks
from utils.config import style_node, style_edge
from dash.exceptions import PreventUpdate


app = dash.Dash(__name__,prevent_initial_callbacks='initial_duplicate', suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, "style.css"])
register_callbacks(app)
cyto.load_extra_layouts()


app.layout = html.Div([
    modal,
    header,
    dcc.Upload(
        id='open-file',
        children=html.Button('Open File'),
        style={
            'display': 'inline-block'
        }
    ),
    html.Div([
    dbc.Button(
        children=[
            html.I(className="bi bi-plus-circle-fill"),  # Icono de +
            " Agregar"
        ],
        id='add-node-button',
        color="primary",  # Color del botón
        className="mr-1"  # Espacio a la derecha del botón
    ),

    dbc.Button(
        children=[
            html.I(className="bi bi-pencil-fill"),  # Icono de +
            " Actualizar"
        ],
        id='update-button',
        color="secondary",  # Color del botón
        className="mr-1"  # Espacio a la derecha del botón
    ),

    dbc.Button(
        children=[
            html.I(className="bi bi-trash3-fill"),  # Icono de +
            " Eliminar"
        ],
        id='delete-button',
        color="danger",  # Color del botón
        className="mr-1"  # Espacio a la derecha del botón
    ),
    html.Div([
    html.Label('Node Label:'),
    dcc.Input(id="node-label-input", type="text", placeholder="", style={'marginRight':'10px'}),
]),
], style={'display': 'flex', 'justifyContent': 'center'}),


    rename_file,
    dcc.Store(id='form-data-store'),
    dcc.Store(id='network-elements'),
    dcc.Store(id='image-data-store'),
    dcc.Store(id="list_elements"),   
    html.Div(id='container'),
    html.Div(id='page-content',children=cyto.Cytoscape(id='network-graph',
                                                        layout={'name': 'circle'},
                                                        elements=[],
                                                        stylesheet=[style_node, style_edge],
                                                        style={'width': '100%', 'height': '800px'},
                                                       )),

])

@app.callback(
    Output('network-graph', 'elements',allow_duplicate=True),
    [Input('close', 'n_clicks')],
    [Input('form-data-store', 'data')],
    Input('open-file', 'contents'),
    Input('open-file', 'filename'),
)
def update_graph(accept_clicks, form_data,file_name, file_contents):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'close':
        # Generar grafo personalizado y actualizar elementos
        n_nodes, is_complete, is_connected, is_weighted, is_directed = get_form_data(form_data)
        if n_nodes is not None:
            elements = update_network_personalizado(n_nodes, is_weighted, is_directed, is_connected, is_complete)
        else:
            elements = []
    elif button_id == 'open-file' and file_contents is not None and file_name is not None:
        # Aquí puedes procesar y visualizar los datos del archivo
        # Por ejemplo, si estás cargando un archivo JSON:
         print("ENTRE AQUI",file_contents,file_name)
         v = load_json_file(file_name,file_contents)
         if v is not None:
             elements = v

   

    return elements





def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Callback for adding nodes
    
@app.callback(
    Output('list_elements', 'data'),
    [Input('add-node-button', 'n_clicks')],
    [State('list_elements', 'data')]
)
def add_node(n_clicks, elements):

    if n_clicks is None:
        # Prevents the callback from being triggered on app load
        raise PreventUpdate

    # If elements is not None, update the global variable
    if elements is None:
        elements = []

    # Create a new node
    new_node = {
        'data': {'id': generate_id(), 'label': 'Node {}'.format(n_clicks)}
    }

    # Add the new node to the existing elements
    elements.append(new_node)

    return elements


@app.callback(
    Output('container', 'children'),
    Input('list_elements', 'data'),
)
def render_nodes(elements):
    if elements is not None:
        return html.Div([
            html.H3('Nodos'),
            html.Ul([
                html.Li('ID: {}, Label: {}'.format(node['data']['id'], node['data']['label']))
                for node in elements
            ])
        ])
    else:
        return html.Div([
            html.H3('Nodos'),
            html.P('No hay nodos')
        ])







































@app.callback(
    Output("download-text", "data",allow_duplicate=True),
    [Input("btn-download-txt", "n_clicks")],
    [State("network-graph", "elements")],
    prevent_initial_call=True,
)
def download_graph(n_clicks, elements):
    if n_clicks > 0 and elements is not None:
        # Convertir los elementos del grafo a una cadena JSON
        json_data = json.dumps(elements)

        # Devolver los datos para descargar en el sistema del usuario
        return dcc.send_string(json_data, filename="grafo.json")
    




    


#TODO: En este callback ponemos el grafo en modo imagen
    
@app.callback(
    Output('page-content', 'children'),
    Input('id-grafica', 'n_clicks'),
    State('image-data-store', 'data'),
    prevent_initial_call=True
)
def display_page(n_clicks, imageData):
    if n_clicks is not None and imageData is not None:
        img = html.Img(src=imageData)
        return html.Div(img)
    else:
        return html.Div([
            html.H1("Grafica"),
        ])






#TODO: ZONA DE MODAL DEL FORMULARIO

@app.callback(
    Output("modal", "is_open"),
    [Input("generate-button", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


























if __name__ == '__main__':
    app.run_server(debug=True)

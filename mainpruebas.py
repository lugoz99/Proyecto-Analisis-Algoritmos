# app.py
# Importaciones de librerías
import json
import random
import string
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
# Importaciones de carpetas y funciones
from layouts.navbar import header
from layouts.form_page import modal, modal_edit_node
from utils.visualization import update_network, update_network_personalizado, load_json_file
from helpers.form import get_form_data, get_form_node_edit
from layouts.general_layouts import rename_file, modal_guardar_como
from callbacks.callbacks import register_callbacks
from utils.config import style_node, style_edge
from dash.exceptions import PreventUpdate
from layouts.buttons import buttons_nodes,buttons_edges

app = dash.Dash(__name__, prevent_initial_callbacks='initial_duplicate', suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, "style.css"])
register_callbacks(app)
cyto.load_extra_layouts()

app.layout = html.Div([
    modal,
    modal_edit_node,
    modal_guardar_como,
    header,
    html.Div(
    style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'},
    children=[
        buttons_nodes,
        buttons_edges
        ]
    ),
    
    dcc.Store(id='form-data-store'),
    dcc.Store(id='network-elements'),
    dcc.Store(id='form-edit-store'),
    dcc.Store(id='image-data-store'),
    dcc.Store(id="list_elements"),
    html.Div(id='page-content',className="d-flex justify-content-center align-items-center",
              children=
                [
                    cyto.Cytoscape(id='network-graph',
                                                        layout={'name': 'circle'},
                                                        elements=[],
                                                        stylesheet=[style_node, style_edge],
                                                        style={'width': '100%', 'height': '800px'},
                                                         ),
                ]
    ),


])


@app.callback(
    [Output('network-graph', 'elements')],
    [
        Input('close', 'n_clicks'),
        Input('form-data-store', 'data'),
        Input('open-file', 'contents'),
        Input('open-file', 'filename'),
        Input('form-edit-store', 'data'),
        Input('add-node-button', 'n_clicks'),
        Input('delete-button', 'n_clicks'),
    ],
    [
        State('network-graph', 'elements'),
        State('network-graph', 'selectedNodeData'),
    ]
)
def update_graph(accept_clicks, form_data, file_name, file_contents, form_edit_data,
                 add_clicks, delete_clicks, elements, selected_node):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'close':
        # Generar grafo personalizado y actualizar elementos
        n_nodes, is_complete, is_connected, is_weighted, is_directed = get_form_data(form_data)
        if n_nodes is not None:
            elements = update_network_personalizado(n_nodes, is_weighted, is_directed, is_connected, is_complete)
        else:
            elements = []
    elif button_id == 'update-button':
        # Actualizar elementos del grafo
        label, color, size = get_form_node_edit(form_edit_data)
        print("Entre en actualizar")
        print(label, color, size)

    elif button_id == 'open-file' and file_contents is not None and file_name is not None:
        # Aquí puedes procesar y visualizar los datos del archivo
        # Por ejemplo, si estás cargando un archivo JSON:
        v = load_json_file(file_name, file_contents)
        if v is not None:
            elements = v

    elif button_id == 'add-node-button' and add_clicks is not None:
        # Añadir un nuevo nodo
        if elements is None:
            elements = []
        new_node = {
            'data': {'id': generate_id(), 'label': 'Node {}'.format(add_clicks)},
            'position': {'x': random.randint(0, 500), 'y': random.randint(0, 500)}  # Agrega coordenadas aleatorias al nodo
        }
        elements.append(new_node)

    elif button_id == 'delete-button' and delete_clicks is not None and selected_node is not None:
        # Eliminar nodo
        if elements is not None and selected_node is not None:
            selected_node = selected_node[0]  # Obtener el primer elemento de selected_node
            print('Deleting node:', selected_node['id'])
            # Remover el nodo seleccionado de los elementos
            elements = [element for element in elements if element['data']['id'] != selected_node['id']]

    return [elements]


def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# ZONA DE MODAL DEL FORMULARIO
@app.callback(
    Output("modal", "is_open"),
    [Input("generate-button", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal-edit-node", "is_open"),
    [Input("update-button", "n_clicks"),
     Input("close-update", "n_clicks")],
    [State("modal-edit-node", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



@app.callback(
    Output("modal-guardar-como", "is_open"),
    [Input("save-file-as", "n_clicks"),
    Input("guardar-como", "n_clicks")],
    [State("modal-guardar-como", "is_open")],
)
def toggle_modal_guardar_como(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



#---------------------------------------------------------------------
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
    



@app.callback(
    Output('page-content', 'children'),
    Input('id-grafica', 'n_clicks'),
    State('image-data-store', 'data'),
    prevent_initial_call=True
)
def display_page(n_clicks, imageData):
    if n_clicks is not None and imageData is not None:
        card_content = [
            dbc.CardBody(
                children=[
                    html.H4("Modo Imagen", className="card-title"),
                    html.Div(
                        dbc.CardImg(src=imageData, 
                                    style={'width': '100%', 
                                           'height': '100%', 
                                           'display': 'block', 
                                           'margin': 'auto',
                                           'object-fit': 'contain'}),
                        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                    ),
                ]
            ),
        ]
        return dbc.Card(card_content, className="w-100 h-100")
  

if __name__ == '__main__':
    app.run_server(debug=True)


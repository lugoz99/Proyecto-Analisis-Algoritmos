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
import numpy as np
import pandas as pd
from dash import dash_table

# Importaciones de carpetas y funciones
from layouts.navbar import header
from layouts.form_page import modal, modal_edit_node
from utils.visualization import (
    update_network,
    update_network_personalizado,
    load_json_file,
)
from helpers.form import get_form_data, get_form_node_edit
from layouts.general_layouts import rename_file, modal_guardar_como
from callbacks.callbacks import register_callbacks
from utils.config import config_stylesheet
from dash.exceptions import PreventUpdate
from layouts.buttons import buttons_nodes, buttons_edges, contenedor_info

app = dash.Dash(
    __name__,
    prevent_initial_callbacks="initial_duplicate",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, "style.css"],
)
register_callbacks(app)
cyto.load_extra_layouts()

app.layout = html.Div(
    [
        modal,
        modal_edit_node,
        modal_guardar_como,
        header,
        html.Div(
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
            },
            children=[buttons_nodes, contenedor_info, buttons_edges],
        ),
        dcc.Store(id="form-data-store"),
        dcc.Store(id="network-elements"),
        dcc.Store(id="form-edit-store"),
        dcc.Store(id="image-data-store"),
        dcc.Store(id="list_elements"),
        html.Div(
            id="page-content",
            className="d-flex justify-content-center align-items-center",
            style={"marginTop": "50px","overflow": "auto",  # Añade esta línea
                    "height": "800px"},
            children=[
                cyto.Cytoscape(
                    id="network-graph",
                    layout={"name": "random"},
                    elements=[],
                    stylesheet=config_stylesheet,
                    style={"width": "100%", "height": "800px"},
                    autoRefreshLayout=True,
                ),
            ],
        ),
    ]
)


@app.callback(
    [Output("network-graph", "elements"),
     Output("network-graph", "stylesheet")],
    [
        Input("close", "n_clicks"),
        Input("form-data-store", "data"),
        Input("open-file", "contents"),
        Input("open-file", "filename"),
        Input("add-node-button", "n_clicks"),
        Input("delete-button", "n_clicks"),
        Input("update-button", "n_clicks"),
        Input("add-edge-button", "n_clicks"),
        Input("delete-edge-button", "n_clicks"),
        Input("update-edge-button", "n_clicks"),
    ],
    [
        State("edge-label-input", "value"),
        State("line-style-dropdown", "value"),
        State("arrow-checklist", "value"),
        State("color-picker", "value"),
        
        State("node-label-input", "value"),
        State("node-value-input", "value"),
        State("color-picker-node", "value"),
        
        State("network-graph", "elements"),
        State("network-graph", "selectedNodeData"),
        State("network-graph", "selectedEdgeData"),
        State("network-graph", "stylesheet"),
    ],
)
def update_graph(
    accept_clicks,
    form_data,
    file_name,
    file_contents,
    # Argumentos para nodos
    add_clicks,
    delete_clicks,
    update_clicks,
    # Argumentos para edges
    add_edge_click,
    delete_e_clicks,
    update_e_clicks,
    edge_label,
    line_style,
    show_arrow,
    color_picker_value,
    node_label,
    node_value,
    color_picker_node,
    #-----------------------
    elements,
    selected_node,
    selected_edge,
    stylesheet,
):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "close":
        # Generar grafo personalizado y actualizar elementos
        n_nodes, is_complete, is_connected, is_weighted, is_directed = get_form_data(
            form_data
        )
        if n_nodes is not None:
            elements = update_network_personalizado(
                n_nodes, is_weighted, is_directed, is_connected, is_complete
            )
            #TODO : AQUI FALTA MODIFCAR LOS ESTILOS
            for style in config_stylesheet:
                if style["selector"] == "edge":
                    if is_directed:
                        style["style"]["target-arrow-shape"] = "triangle"
                    else:
                        if "target-arrow-shape" in style["style"]:
                            del style["style"]["target-arrow-shape"]

    elif button_id == "update-button":
        selected_node = selected_node[0]
        print("Selected node:", selected_node)
        elements_dict = {element["data"]["id"]: element for element in elements}
        print("Elements dict:", elements_dict)
        if selected_node["id"] in elements_dict:
            elements_dict[selected_node["id"]]["data"]["label"] = node_label
            elements_dict[selected_node["id"]]["data"]["value"] = node_value
            print("Updated node:", elements_dict[selected_node["id"]])
            
            node_style = {
                "selector": f'node[id = "{selected_node["id"]}"]',
                "style": {
                    "background-color": color_picker_node["hex"],
                },
            }
            # Agregar el nuevo selector a la hoja de estilos
            stylesheet.append(node_style)

    elif (
        button_id == "open-file" and file_contents is not None and file_name is not None
    ):
        # Aquí puedes procesar y visualizar los datos del archivo
        # Por ejemplo, si estás cargando un archivo JSON:
        v = load_json_file(file_name, file_contents)
        if v is not None:
            elements = v

    elif button_id == "add-node-button" and add_clicks is not None:
        # Añadir un nuevo nodo
        if elements is None:
            elements = []
        new_node = {
            "data": {"id": generate_id(), "label": "Node {}".format(add_clicks),"value":str(0)},
            "position": {
                "x": random.randint(0, 500),
                "y": random.randint(0, 500),
            },  # Agrega coordenadas aleatorias al nodo
        }
        elements.append(new_node)

    elif (
        button_id == "delete-button"
        and delete_clicks is not None
        and selected_node is not None
    ):
        # Eliminar nodo
        if elements is not None and selected_node is not None:
            selected_node = selected_node[
                0
            ]  # Obtener el primer elemento de selected_node
            print("Deleting node:", selected_node["id"])
            # Remover el nodo seleccionado de los elementos
            elements = [
                element
                for element in elements
                if element["data"]["id"] != selected_node["id"]
            ]
    # *******CREAR,EDITAR Y ELIMINAR ARISTAS**********************************************

    elif (
        button_id == "add-edge-button"
        and add_edge_click is not None
        and selected_node is not None
    ):
        # Añadir una nueva arista
        edge_id = generate_id()
        new_edge = {
            "data": {
                "id": edge_id,
                "source": selected_node[0]["id"],
                "target": selected_node[-1]["id"],
                "weight": 0,
            }
        }
        elements.append(new_edge)

    elif (
        button_id == "delete-edge-button"
        and delete_e_clicks is not None
        and selected_node is not None
    ):
        # Eliminar arista
        print("Deleting edge:", selected_edge)
        selected_edge_id = selected_edge[0][
            "id"
        ]  # Obtener el id de la arista seleccionada
        elements = [
            element for element in elements if element["data"]["id"] != selected_edge_id
        ]

    elif (
        button_id == "update-edge-button"
        and update_e_clicks is not None
        and selected_edge is not None
    ):
        print("Editing edge:", selected_edge)
        print("weight", edge_label)
        print("line style", line_style)
        print("arrow", show_arrow)
        print("color", color_picker_value)
        edge_id = selected_edge[0]["id"]  # Obtener el id de la arista seleccionada
        color_hex = color_picker_value["hex"]
        if selected_edge is not None:
            # Crear un diccionario con los elementos para buscar de manera eficiente
            elements_dict = {element["data"]["id"]: element for element in elements}
            # Ahora puedes buscar y modificar el peso de una arista de manera eficiente

            if edge_id in elements_dict and "source" in elements_dict[edge_id]["data"]:
                elements_dict[edge_id]["data"]["weight"] = edge_label

            edge_style = {
                "selector": f'edge[id = "{edge_id}"]',
                "style": {
                    "line-color": color_hex,
                    "line-style": line_style,
                    "target-arrow-shape": (
                        "triangle" if "show-arrow" in show_arrow else "none"
                    ),
                },
            }
            # Agregar el nuevo selector a la hoja de estilos
            stylesheet.append(edge_style)

    return elements, stylesheet



def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


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
    Output("modal-guardar-como", "is_open"),
    [Input("save-file-as", "n_clicks"), Input("guardar-como", "n_clicks")],
    [State("modal-guardar-como", "is_open")],
)
def toggle_modal_guardar_como(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# ---------------------------------------------------------------------
@app.callback(
    Output("download-text", "data", allow_duplicate=True),
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
    Output("info-grafo", "children"),
    Input("id-grafica", "n_clicks"),
    State("image-data-store", "data"),
    prevent_initial_call=True,
)
def display_page(n_clicks, imageData):
    if n_clicks is not None and imageData is not None:
        card_content = [
            dbc.CardBody(
                children=[
                    html.H4("Modo Imagen", className="card-title"),
                    html.Div(
                        dbc.CardImg(
                            src=imageData,
                            style={
                                "width": "100%",
                                "height": "100%",
                                "display": "block",
                                "margin": "auto",
                                "object-fit": "contain",
                            },
                        ),
                        style={
                            "display": "flex",
                            "justify-content": "center",
                            "align-items": "center",
                        },
                    ),
                ]
            ),
        ]
        return dbc.Card(card_content, className="w-100 h-100")










@app.callback(
    Output("info-grafo", "children",allow_duplicate=True),
    [Input("id-table", "n_clicks")],
    [State("network-graph", "elements")],
    prevent_initial_call=True,
)
def tabla(n_clicks, elements):
    if n_clicks is not None and elements is not None:
        conjunto_arista = [item["data"] for item in elements if 'source' in item['data'] and 'target' in item['data']]
        df = pd.DataFrame(conjunto_arista)
        nodes = pd.concat([df["source"], df["target"]]).unique()

        # Crear un mapeo de los nodos a números enteros
        node_mapping = {node: i for i, node in enumerate(nodes)}

        # Aplicar el mapeo a los datos de las aristas
        df["source"] = df["source"].map(node_mapping)
        df["target"] = df["target"].map(node_mapping)

        # Crear la matriz de adyacencia con los nodos mapeados
        adjacency_matrix = pd.DataFrame(np.zeros((len(nodes), len(nodes)), dtype=int), index=range(len(nodes)), columns=range(len(nodes)))

        for _, edge in df.iterrows():
            adjacency_matrix.loc[edge['source'], edge['target']] = 1
            adjacency_matrix.loc[edge['target'], edge['source']] = 1

        # Crear la tabla
        table = dash_table.DataTable(
                data=adjacency_matrix.reset_index().rename(columns={"index": ""}).to_dict('records'),
                columns=[{"name": str(i), "id": str(i)} if i != "" else {"name": i, "id": i} for i in adjacency_matrix.columns],
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_cell={
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',
                    'whiteSpace': 'normal',
                    'color':'black'
            }
        )
        title = html.H3('Matriz de Representación')

        if table is not None:
             return html.Div([title, table])


@app.callback(
    Output("info-grafo", "children",allow_duplicate=True),
[    Input("id-grafica", "n_clicks"),
     Input("open-file", "contents"),
     Input("open-file", "filename"),
     Input("close", "n_clicks"),
     Input("add-node-button", "n_clicks"),
     Input("add-edge-button", "n_clicks"),
     ],
    prevent_initial_call=True,
)
def clear_info_grafo(n1, n2, n3,n4,n7,n6):  # Añade más argumentos aquí si agregas más acciones
    # Este callback se activará si cualquiera de las acciones se realiza
    return None



if __name__ == "__main__":
    app.run_server(debug=True)

# Path: layouts/buttons.py

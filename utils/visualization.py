import io
import random
import itertools
import traceback
import networkx as nx
import base64
import json

from dash.exceptions import PreventUpdate

from utils.config import style_node, style_edge

def create_graph(num_nodes, is_weighted, is_directed, is_connected, is_complete):
    # Crear un grafo vacío
    if not is_directed:
        G = nx.Graph()
        edge_arrow_shape = None  # No se mostrarán flechas en las aristas
    else:
        G = nx.DiGraph()
        edge_arrow_shape = 'triangle' 
        style_edge['style']['target-arrow-shape'] = edge_arrow_shape

    # Añadir nodos
    G.add_nodes_from(range(num_nodes))

    # Añadir aristas para hacer el grafo completo, si se seleccionó esa opción
    if is_complete:
        G.add_edges_from(itertools.combinations(range(num_nodes), 2))

    # Añadir aristas para hacer el grafo conexo, si se seleccionó esa opción y el grafo no es completo
    elif is_connected and not is_complete:
        for i in range(1, num_nodes):
            G.add_edge(i - 1, i)

    # Añadir pesos a las aristas, si se seleccionó esa opción
    if is_weighted:
        for (u, v) in G.edges():
            G.edges[u,v]['weight'] = random.randint(1,100)

    # Convertir el gráfico de NetworkX a un formato que Cytoscape puede utilizar
    # TODO : COMO ASOCIO VALOR,LABEL
    cyto_elements = [
    {'data': {'id': str(node), 'label': str(node)}} for node in G.nodes()
]
#     cyto_elements.extend([
#     {'data': {'source': str(edge[0]), 'target': str(edge[1]), 'weight': str(G.edges[edge]['weight']) if is_weighted else None, 'label': str(G.edges[edge]['weight']) if is_weighted else None}} for edge in G.edges()
# ])
    
    cyto_elements.extend([
    {'data': {'source': str(edge[0]), 'target': str(edge[1]), 'weight': str(G.edges[edge].get('weight', 0)), 'label': str(G.edges[edge].get('weight', 0))}} for edge in G.edges()
])

    
    return cyto_elements

def update_network():
    # Generar características aleatorias
    num_nodes = random.randint(5, 10)
    is_weighted = random.choice([True, False])
    is_directed = random.choice([True, False])
    is_connected = random.choice([True, False])
    is_complete = random.choice([True, False])

    return create_graph(num_nodes, is_weighted, is_directed, is_connected, is_complete)

def update_network_personalizado(num_nodes, is_weighted, is_directed, is_connected, is_complete):
    return create_graph(num_nodes, is_weighted, is_directed, is_connected, is_complete)



def parse_graph_json(graph_json):
    graph_data = graph_json["graph"][0]["data"]

    # Crea los nodos y aristas para Dash-Cytoscape
    nodes = []
    edges = []

    for node in graph_data:
        node_id = str(node["id"])
        nodes.append({"data": {"id": node_id, "label": node["label"]}})

        for linked_node in node["linkedTo"]:
            edges.append(
                {
                    "data": {
                        "source": node_id,
                        "target": str(linked_node["nodeId"]),
                        "weight": linked_node["weight"],
                    }
                }
            )

    return nodes, edges



# -----------------------------------

def mapear_grafo(data_Json):
    if isinstance(data_Json, dict):
        graph_data = data_Json["graph"][0]["data"]

# Crea los nodos y aristas para Dash-Cytoscape
        nodes = []
        edges = []

        for node in graph_data:
            node_id = str(node["id"])
            nodes.append({"data": {"id": node_id, "label": node["label"]}})

            for linked_node in node["linkedTo"]:
                edges.append(
                    {
                        "data": {
                            "source": node_id,
                            "target": str(linked_node["nodeId"]),
                            "weight": linked_node["weight"],
                        }
                    }
                )
        return nodes+edges
    

def load_json_file(contents, filename):
    elements = None
    if contents is not None and ',' in contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                # Assume that the user uploaded a JSON file
                str_io = io.StringIO(decoded.decode('utf-8'))
                json_data = json.load(str_io)
                elements = mapear_grafo(json_data)
        except Exception as e:
            print(f"Error: {type(e).__name__}")
            print(f"Description: {e}")
            traceback.print_exc()
            return 'Hubo un error procesando este archivo.'
        return elements
    else:
        raise PreventUpdate
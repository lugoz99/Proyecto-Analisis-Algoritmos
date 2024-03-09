import random
import itertools
import networkx as nx

def create_graph(num_nodes, is_weighted, is_directed, is_connected, is_complete):
    # Crear un grafo vacío
    if not is_directed:
        G = nx.Graph()
        edge_arrow_shape = None  # No se mostrarán flechas en las aristas
    else:
        G = nx.DiGraph()
        edge_arrow_shape = 'triangle' 

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
            G.edges[u,v]['weight'] = random.randint(1,1001)

    # Convertir el gráfico de NetworkX a un formato que Cytoscape puede utilizar
    cyto_elements = [
        {'data': {'id': str(node)}} for node in G.nodes()
    ]
    cyto_elements.extend([
    {'data': {'source': str(edge[0]), 'target': str(edge[1]), 'weight': str(G.edges[edge]['weight']) if is_weighted else None, 'label': str(G.edges[edge]['weight']) if is_weighted else None}} for edge in G.edges()
])

    node_style = {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(id)'
        }
    }

    edge_style = {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': edge_arrow_shape,
            'label': 'data(label)',
            'font-size': '10px'
        }
    }
    return cyto_elements, [node_style,edge_style]

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




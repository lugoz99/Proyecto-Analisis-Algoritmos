import base64
from dash import Input,Output, callback
import json
import dash
import io
from dash import html
from dash.exceptions import PreventUpdate
import traceback





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

stylesheet = [
    {"selector": "node", "style": {"width": 50, "height": 50, "label": "data(label)", "font-size": "14px"}},
    {"selector": "edge", "style": {"width": 3, "label": "data(weight)"}},
]

def register_callbacks(app):
    @app.callback(
    Output('network-elements', 'data'),
    Output('network-stylesheet', 'data'),
    [Input('upload-json', 'contents'), Input('upload-json', 'filename')]
)
    def update_output(list_of_contents, list_of_names):
        elements = None
        if list_of_contents is not None:
            children = []
            for contents, filename in zip(list_of_contents, list_of_names):
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                try:
                    if 'json' in filename:
                        # Assume that the user uploaded a JSON file
                        str_io = io.StringIO(decoded.decode('utf-8'))
                        json_data = json.load(str_io)

                        elements = mapear_grafo(json_data)
                        print(elements)
                        #children.append(html.Pre(json.dumps(json_data, indent=2)))
                        
                except Exception as e:
                    print(f"Error: {type(e).__name__}")
                    print(f"Description: {e}")
                    traceback.print_exc()
                    children.append(html.Div([
                        'Hubo un error procesando este archivo.'
                    ]))
            return elements,stylesheet
        else:
            raise PreventUpdate
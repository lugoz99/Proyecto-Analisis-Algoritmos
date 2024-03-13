import base64
from dash import Input,Output,State,no_update,callback_context,dcc
import json
import io
from dash import html
from dash.exceptions import PreventUpdate
import traceback
import os



# Mapeo para el json
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


# Callbacks
def register_callbacks(app):
    @app.callback(
    Output('network-elements', 'data'),
    Output('network-stylesheet', 'data'),
    [Input('upload-json', 'contents'), 
     Input('upload-json', 'filename')]
)
    # Función para cargar el archivo JSON y retornar los elementos y el estilo
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
                        print("mapeo")
                except Exception as e:
                    print(f"Error: {type(e).__name__}")
                    print(f"Description: {e}")
                    traceback.print_exc()
                    children.append(html.Div([
                        'Hubo un error procesando este archivo.'
                    ]))
            return elements,[]
        else:
            raise PreventUpdate
        
    
    # Callbacks para la página de personalización en donde se guarda la imagen 
    @app.callback(
    Output('network-graph', 'generateImage',allow_duplicate=True),
    Input('network-graph', 'elements'),
    )
    def update_generate_image(elements):
        return {'type': 'png', 'action': 'store'}
    
    @app.callback(
        Output('image-data-store', 'data'),
        Input('network-graph', 'imageData')
    )
    def store_image_data(imageData):
        return imageData
    



    # callback que guarda los datos del formulario
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
        

    # Callback para la generancion de una imagen de tipo png y jpg
    @app.callback(
        Output('network-graph', 'generateImage'),
        [Input('btn-get-jpg', 'n_clicks'),
        Input('btn-get-png', 'n_clicks'),
        ])
    def update_output(jpg_clicks, png_clicks):
        ctx = callback_context 

        if not ctx.triggered:
            return no_update
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            image_type = button_id.split('-')[-1]

            return {'type': image_type, 'action': 'download', 'filename': 'grafo','options': {'full': True}}




    # Callback para guardar el archivo JSON , Dandole un nombre
    @app.callback(
    Output("download", "data"),
    [Input("btn", "n_clicks"), Input("input", "value")],
    [State("network-graph-elements", "data")], # Aquí puedes agregar más estados si los necesitas
    prevent_initial_call=True,
    )
    def func(n_clicks, value,data):
        if n_clicks > 0 and value is not None and data is not None:
            # Guardar el objeto JSON en un archivo en el servidor
            with open(os.path.join(os.getcwd(),'data', value + ".json"), 'w') as f:
                json.dump(data, f)
            # Devolver los datos para descargar en el sistema del usuario
            return dcc.send_string(json.dumps(data), filename=value + ".json")


    @app.callback(
        Output('network-graph-elements', 'data'),
        Input('network-graph', 'elements')
    )
    def store_elements_data(elements):
        if elements:
            return elements
        return no_update

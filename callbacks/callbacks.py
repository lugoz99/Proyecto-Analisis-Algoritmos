import base64
from dash import Input,Output,State,no_update,callback_context,dcc
import json
import io
from dash import html
from dash.exceptions import PreventUpdate
import traceback
import os
import dash_cytoscape as cyto
import pandas as pd



# Callbacks
def register_callbacks(app):

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
    



    #TODO: callback que guarda los datos del formulario [EN USO]
    @app.callback(
    Output('form-data-store', 'data'),
    [Input('close', 'n_clicks')],
    [State('n-nodes-input', 'value'),
     State('is-complete-input', 'value'),
     State('is-connected-input', 'value'),
     State('is-weighted-input', 'value'),
     State('is-directed-input', 'value')]
)
    def store_form_data(n_clicks, n_nodes, is_complete, is_connected, is_weighted, is_directed):
        if not n_clicks:
            return no_update

        form_data = {
            'n_nodes': n_nodes,
            'is_complete': is_complete,
            'is_connected': is_connected,
            'is_weighted': is_weighted,
            'is_directed': is_directed
        }
        return form_data
    

    #TODO: AQUI VOY A EDITAR EL CALLBACK PARA QUE GUARDE LOS DATOS DEL FORMULARIO DE EDICION
    @app.callback(
    Output('form-edit-store', 'data'),
    [Input('close-update"', 'n_clicks')],
    [State('input-label', 'value'),
     State('input-value', 'value'),
     State('input-color', 'value')],
    )
    def store_form_edit(n_clicks, label, valor, color):
        if not n_clicks:
            return no_update
        
        print(form_data)
        form_data = {
            'label': label,
            'value': valor,
            'color': color,
        }
        return form_data
        

    #TODO:Callback para la generancion de una imagen de tipo png y jpg
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
        [Input("guardar-como", "n_clicks")],  # Agregado "save-file-as" como Input
        [State("network-graph", "elements"),
        State("input", "value")],  # Cambiado "rename_file" a "input"
        prevent_initial_call=True,
    )
    def func(save_as_clicks, data, filename): 
        print(save_as_clicks, data, filename)
        if save_as_clicks > 0 and filename is not None and data is not None:  # Cambiado "n_clicks" a "save_as_clicks"
            # Serializar los datos a una cadena JSON
            json_data = json.dumps(data)
            
            # Guardar el objeto JSON en un archivo en el servidor
            with open(os.path.join(os.getcwd(), 'data', filename + ".json"), 'w') as f:
                f.write(json_data)
            
            # Devolver los datos para descargar en el sistema del usuario
            return dcc.send_string(json_data, filename=filename + ".json") 
        else:
            print("No se ha seleccionado un archivo para guardar") 



# ****************************************************************
# ***Callback para descargar la matriz de adyacencia en Excel***
            
    @app.callback(
        Output("download-excel", "data",allow_duplicate=True),
        [Input("btn", "n_clicks"), Input("network-graph", "elements")],
        prevent_initial_call=True,
    )

    def func(n_clicks,elements):
        if n_clicks > 0:
            print(elements)
            print("tamaño de la lista",len(elements))
            # Crear dos DataFrames vacíos con los nodos como índices y columnas
            nodes = [str(i) for i in range(len(elements))]
            df_binary = pd.DataFrame(0, index=nodes, columns=nodes)
            df_weights = pd.DataFrame(0, index=nodes, columns=nodes)

            # Iterar sobre las aristas del grafo
            for element in elements:
                if 'source' in element['data'] and 'target' in element['data']:
                    # Para cada arista, establecer el valor correspondiente en el DataFrame al peso de la arista
                    df_binary.loc[element['data']['source'], int(element['data']['target'])] = 1
                    df_binary.loc[element['data']['target'], int(element['data']['source'])] = 1
                    df_weights.loc[element['data']['source'],int( element['data']['target'])] = element['data'].get('weight', 0)
                    df_weights.loc[element['data']['target'],int( element['data']['source'])] = element['data'].get('weight', 0)

            # Agregar una columna vacía al principio de cada DataFrame
            # df_binary.insert(0, '', '')
            # df_weights.insert(0, '', '')

            # Agregar el título 'Origen/Destino' en la primera celda superior izquierda
            df_binary.columns = ['Origen/Destino'] + [str(i) for i in df_binary.columns[1:]]
            df_weights.columns = ['Origen/Destino'] + [str(i) for i in df_weights.columns[1:]]

            # Generar un nombre de archivo automáticamente
            file_path = os.path.join(os.getcwd(), 'data', "adjacency_matrix.xlsx")

            # Crear un escritor de Excel y escribir ambos DataFrames en diferentes hojas
            with pd.ExcelWriter(file_path) as writer:
                df_binary.to_excel(writer, sheet_name='Binary', index=False)
                df_weights.to_excel(writer, sheet_name='Weights', index=False)

            # Devolver los datos para que se descarguen en el sistema del usuario
            return dcc.send_file(file_path)
        



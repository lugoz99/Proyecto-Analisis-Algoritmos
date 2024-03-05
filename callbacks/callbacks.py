from dash import Input,Output



def read_json(json):
    with open(json, 'r') as file:
        data = json.load(file)
    return data


Output('page-content', 'children')
Input('upload-data', 'contents')
def mapear_grafo(data):
    data = data['graph']
    nodes = []
    edges = []
    cyto_elements = {
        {data : {
            "id" : "",
        }}
    }
    for i in range(len(data)):
        cyto_elements = data[i]['data']


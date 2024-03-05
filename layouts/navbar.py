import dash_bootstrap_components as dbc


navbar = dbc.NavbarSimple(
        className="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm",
        children=[
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Nuevo Grafo", header=True),
                    dbc.DropdownMenuItem("Personalizado", href="/formulario"),
                    dbc.DropdownMenuItem("Aleatorio",id="generate-random", href="/aleatorio"),
                ],
                nav=True,
                in_navbar=True,
                label="Generate",
            ),

            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Procesos", header=True),
                    dbc.DropdownMenuItem("Proceso 1", id='open-file-p'),
                    dbc.DropdownMenuItem("Proceso 2", id='open-p-p'),

                ],
                nav=True,
                in_navbar=True,
                label="Ejecutar",
            ),

            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Ver en Modo", header=True),
                    dbc.DropdownMenuItem("Grafica", id='open-file-m'),
                    dbc.DropdownMenuItem("Tabla", id='close-file-m-1'),
                ],
                nav=True,
                in_navbar=True,
                label="Ventana",
            ),
    
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Nodo", header=True),
                    dbc.DropdownMenuItem("Agregar", id='open-file-M-M'),
                    dbc.DropdownMenuItem("Editar", id='close-file-M-1'),
                    dbc.DropdownMenuItem("Eliminar", id='save-file-1'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Arista", header=True),
                    dbc.DropdownMenuItem("Agregar", id='open-file-a-1-S'),
                    dbc.DropdownMenuItem("Editar", id='close-file-a'),
                    dbc.DropdownMenuItem("Eliminar", id='save-file-SS'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Deshacer", id='open-file-a-Z'),

                ],
                nav=True,
                in_navbar=True,
                label="Gestion Grafo",
            ),

            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Opciones", header=True),
                    dbc.DropdownMenuItem("Open File", id='open-file', href="/cargar-json"),
                    dbc.DropdownMenuItem("Close File", id='close-file'),
                    dbc.DropdownMenuItem("Save File", id='save-file'),
                    dbc.DropdownMenuItem("Save File As", id='save-file-as'),
                    # Agrega aquí más operaciones si las necesitas
                ],
                nav=True,
                in_navbar=True,
                label="Operaciones Archivos",
            ),

            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Importar Datos", header=True),
                    dbc.DropdownMenuItem("Formato txt", href="#"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Exportar datos", header=True),
                    dbc.DropdownMenuItem("Excel", href="#"),
                    dbc.DropdownMenuItem("Imagen", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="Gestion datos",
            ),
        
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Ayuda", header=True),
                    dbc.DropdownMenuItem("Herramienta", id='open-file-x-x'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Documentacion", header=True),
                    dbc.DropdownMenuItem("Manual usuario", id='open-file-a-1'),
                    dbc.DropdownMenuItem("Acerca grafos", id='close-file-a-d'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Salir", id='open-file-a-s'),

                ],
                nav=True,
                in_navbar=True,
                label="Usuario",
            ),
            
        ],
        brand="AYDA-2024",
        brand_href="#",
        color="primary",
        dark=True,
    )
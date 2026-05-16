import flet as ft
from ui.components import Style, create_card

def render_input_form(n_v, n_r, on_calculate):
    """
    Renderiza el formulario de entrada para el problema de PL.
    
    Args:
        n_v: Número de variables
        n_r: Número de restricciones
        on_calculate: Callback cuando se presiona "Calcular Solución"
    
    Returns:
        Tupla (container_column, inputs_c, inputs_A, inputs_b, inputs_signs)
    """
    inputs_c = []
    inputs_A = []
    inputs_b = []
    inputs_signs = []
    
    input_container = ft.Column()

    # Función objetivo
    c_row = ft.Row(wrap=True, spacing=10)
    for i in range(n_v):
        field = ft.TextField(label=f"c{i+1}", width=70, text_align="center")
        inputs_c.append(field)
        c_row.controls.append(field)
    
    input_container.controls.append(create_card("Coeficientes de la Función Objetivo", c_row))

    # Restricciones
    r_col = ft.Column(spacing=10)
    for i in range(n_r):
        row = ft.Row(wrap=True, spacing=10)
        fila_fields = []
        for j in range(n_v):
            f = ft.TextField(label=f"a{i+1},{j+1}", width=70)
            fila_fields.append(f)
            row.controls.append(f)

        sign = ft.Dropdown(
            width=80,
            value="≤",
            options=[
                ft.dropdown.Option("≤"),
                ft.dropdown.Option("≥"),
                ft.dropdown.Option("=")
            ]
        )
        rhs = ft.TextField(label="RHS", width=80, border_color=Style.SECONDARY)
        inputs_A.append(fila_fields)
        inputs_signs.append(sign)
        inputs_b.append(rhs)
        row.controls.extend([sign, rhs])
        r_col.controls.append(row)
    
    input_container.controls.append(create_card("Matriz de Restricciones", r_col))
    input_container.controls.append(
        ft.Button("Calcular Solución", icon=ft.Icons.ANALYTICS, 
                         on_click=on_calculate, bgcolor=Style.PRIMARY, color="white")
    )

    return input_container, inputs_c, inputs_A, inputs_b, inputs_signs

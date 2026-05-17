import flet as ft
from ui.components import Style

def _format_cell(value, highlighted=False, bold=False):
    """Formatea una celda de tabla con estilos opcionales adaptables"""
    # Al dejar color=None, Flet usará blanco en modo oscuro y negro en modo claro automáticamente
    text = ft.Text(f"{value}", weight="bold" if bold else "normal")
    
    if highlighted:
        # Usamos una opacidad ligera ("#20FFFFFF" en oscuro o una variante suave)
        # Para ir a la fija en ambos modos, un fondo grisáceo sutil con bordes definidos:
        return ft.DataCell(
            ft.Container(
                content=text, 
                bgcolor="surfacecontainerhighest", # Variante nativa excelente para resaltar celdas
                padding=5, 
                border_radius=4
            )
        )
    return ft.DataCell(ft.Container(content=text, padding=5))

def render_table(info):
    """
    Renderiza una tabla individual con su información de fase e iteración.
    
    Args:
        info: Diccionario con tabla, columnas, base, entering, leaving, phase, iter
    
    Returns:
        ft.Card con la tabla renderizada
    """
    tabla = info["tabla"]
    columnas = info["columns"]
    base = info["base"]
    entering = info.get("entering")
    leaving = info.get("leaving")
    fase = info.get("phase", "Fase")
    iteracion = info.get("iter", 0)

    header_text = f"{fase} - Iteración {iteracion}"
    phase_label = ft.Text(header_text, size=18, weight="bold", color=Style.ACCENT)
    selector_label = ft.Text(
        f"Variable entrante: {entering or '-'}    |    Variable saliente: {leaving or '-'}",
        size=14
    )

    # Headers de la tabla
    columns_widgets = [ft.DataColumn(ft.Text("Base", weight="bold"))]
    for col in columnas:
        col_color = Style.ACCENT if col == entering else None
        columns_widgets.append(ft.DataColumn(ft.Text(col, weight="bold", color=col_color)))
    columns_widgets.append(ft.DataColumn(ft.Text("RHS", weight="bold")))

    # Filas de restricciones
    rows = []
    for row_index, fila in enumerate(tabla[:-1]):
        cells = []
        base_name = base[row_index]
        base_highlight = base_name == leaving
        cells.append(_format_cell(base_name, highlighted=base_highlight, bold=True))
        for col_index, value in enumerate(fila[:-1]):
            is_pivot_column = columnas[col_index] == entering
            is_pivot_row = base_name == leaving
            cells.append(_format_cell(f"{value:.2f}", highlighted=is_pivot_column or is_pivot_row))
        cells.append(_format_cell(f"{fila[-1]:.2f}", highlighted=is_pivot_row))
        rows.append(ft.DataRow(cells=cells))

    # Fila de función objetivo
    objective_cells = [ft.DataCell(ft.Text("Z/W", weight="bold"))]
    for col_index, value in enumerate(tabla[-1][:-1]):
        objective_cells.append(_format_cell(f"{value:.2f}", highlighted=columnas[col_index] == entering))
    objective_cells.append(_format_cell(f"{tabla[-1, -1]:.2f}"))
    rows.append(ft.DataRow(cells=objective_cells))

    dt = ft.DataTable(columns=columns_widgets, rows=rows)
    
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                phase_label,
                selector_label,
                dt
            ], spacing=10),
            padding=20
        ),
        elevation=3,
        margin=ft.Margin(bottom=15)
    )

def render_all_tables_cascade(tablas_historial):
    """
    Renderiza todas las tablas en cascada sin botones de navegación.
    
    Args:
        tablas_historial: Lista de diccionarios con información de tablas
    
    Returns:
        ft.Column con todas las tablas apiladas
    """
    if not tablas_historial:
        return ft.Column([
            ft.Text("No hay tablas disponibles", size=14, color=ft.Colors.GREY)
        ])
    
    tables_column = ft.Column(spacing=10)
    for info in tablas_historial:
        table_card = render_table(info)
        tables_column.controls.append(table_card)
    
    return tables_column

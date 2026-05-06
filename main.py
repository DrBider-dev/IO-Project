import flet as ft
import numpy as np
from solver.simplex_engine import SimplexSolver
from ui.components import Style, create_header, create_card

def main(page: ft.Page):
    page.title = "Optimización de Producción - Equipo 6"
    page.theme_mode = ft.ThemeMode.LIGHT # Tema inicial
    page.scroll = "adaptive"
    page.padding = 40

    # --- Función para cambiar el tema ---
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE_OUTLINED
            theme_button.tooltip = "Cambiar a modo claro"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE_OUTLINED
            theme_button.tooltip = "Cambiar a modo oscuro"
        page.update()

    # Botón de tema
    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE_OUTLINED,
        tooltip="Cambiar a modo oscuro",
        on_click=change_theme
    )

    # Contenedores principales
    input_container = ft.Column()
    results_container = ft.Column()

    # Referencias de inputs
    inputs_c = []
    inputs_A = []
    inputs_b = []

    def on_generate_click(e):
        try:
            n_v, n_r = int(txt_v.value), int(txt_r.value)
            render_form(n_v, n_r)
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Ingresa valores válidos"))
            page.snack_bar.open = True
            page.update()

    def render_form(n_v, n_r):
        input_container.controls.clear()
        results_container.controls.clear()
        inputs_c.clear(); inputs_A.clear(); inputs_b.clear()

        # F. Objetivo
        c_row = ft.Row(wrap=True, spacing=10)
        for i in range(n_v):
            field = ft.TextField(label=f"c{i+1}", width=70, text_align="center")
            inputs_c.append(field)
            c_row.controls.append(field)
        
        input_container.controls.append(create_card("Márgenes de Contribución (Z)", c_row))

        # Restricciones
        r_col = ft.Column(spacing=10)
        for i in range(n_r):
            row = ft.Row(wrap=True, spacing=10)
            fila_fields = []
            for j in range(n_v):
                f = ft.TextField(label=f"a{i+1},{j+1}", width=70)
                fila_fields.append(f)
                row.controls.append(f)
            
            rhs = ft.TextField(label="RHS", width=80, border_color=Style.SECONDARY)
            inputs_A.append(fila_fields)
            inputs_b.append(rhs)
            row.controls.extend([ft.Text("≤"), rhs])
            r_col.controls.append(row)
        
        input_container.controls.append(create_card("Matriz de Restricciones", r_col))
        input_container.controls.append(
            ft.ElevatedButton("Calcular Solución", icon=ft.Icons.ANALYTICS, 
                             on_click=run_calculation, bgcolor=Style.PRIMARY, color="white")
        )
        page.update()

    def run_calculation(e):
        try:
            c = [float(i.value) for i in inputs_c]
            A = [[float(i.value) for i in fila] for fila in inputs_A]
            b = [float(i.value) for i in inputs_b]
            
            tablas = SimplexSolver.resolver(c, A, b)
            display_tables(tablas, len(c), len(b))
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()

    def display_tables(tablas, nv, nr):
        results_container.controls.clear()
        
        # 1. Definir nombres de las columnas para las tablas
        cols = [f"X{i+1}" for i in range(nv)] + [f"S{i+1}" for i in range(nr)] + ["RHS"]
        
        # 2. Renderizar cada tabla del proceso iterativo
        for i, t in enumerate(tablas):
            dt = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(c, weight="bold")) for c in cols],
                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(f"{v:.2f}")) for v in fila]) for fila in t]
            )
            title = f"Iteración {i}" + (" - ÓPTIMO" if i == len(tablas)-1 else "")
            results_container.controls.append(create_card(title, dt))

        # 3. --- SECCIÓN DE RESULTADOS ENTENDIBLES ---
        tabla_optima = tablas[-1]
        valor_maximo = tabla_optima[-1, -1]
        
        # Nombres de los productos según el documento
        productos = ["Mesas de Comedor", "Sillas Tapizadas", "Libreros Modulares", "Escritorios Ergonómicos"]
        
        # Lista para guardar los mensajes de producción
        mensajes_produccion = []
        
        # Lógica para identificar cuánto de cada variable X hay en la solución
        # (Buscamos columnas básicas para las variables originales)
        for j in range(nv):
            columna = tabla_optima[:-1, j]
            # Si la columna es un vector unitario (columna básica)
            if np.sum(columna == 1) == 1 and np.sum(columna == 0) == len(columna) - 1:
                fila_donde_esta_el_uno = np.where(columna == 1)[0][0]
                cantidad = tabla_optima[fila_donde_esta_el_uno, -1]
            else:
                cantidad = 0
            
            nombre_prod = productos[j] if j < len(productos) else f"Producto {j+1}"
            mensajes_produccion.append(
                ft.Text(f"• {nombre_prod}: {cantidad:.2f} unidades", size=16)
            )

        # Crear la tarjeta de resumen final
        resumen_final = ft.Container(
            content=ft.Column([
                ft.Text("RECOMENDACIÓN DE PRODUCCIÓN", size=20, weight="bold", color=Style.ACCENT),
                ft.Text("Para maximizar la utilidad este mes, la empresa debe fabricar:", size=16),
                ft.Column(mensajes_produccion),
                ft.Divider(),
                ft.Text(f"UTILIDAD MÁXIMA ESTIMADA: COP ${valor_maximo:,.2f}", 
                        size=22, weight="bold", color=Style.PRIMARY),
            ], spacing=10),
            padding=30,
            bgcolor=Style.BG_LIGHT if page.theme_mode == ft.ThemeMode.LIGHT else Style.BG_DARK,
            border_radius=15,
            border=ft.border.all(2, Style.ACCENT),
            margin=ft.margin.only(top=20)
        )

        results_container.controls.append(resumen_final)
        page.update()

    # --- Layout Inicial ---
    # Colocamos el header y el botón de tema en una fila
    header_row = ft.Row(
        controls=[
            create_header(), # Tu componente de encabezado
            theme_button
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    txt_v = ft.TextField(label="Variables", width=120)
    txt_r = ft.TextField(label="Restricciones", width=120)
    
    page.add(
        header_row,
        ft.Row([txt_v, txt_r, ft.IconButton(ft.Icons.SETTINGS_SUGGEST_OUTLINED, on_click=on_generate_click)], alignment="center"),
        input_container,
        results_container
    )

if __name__ == "__main__":
    ft.app(target=main)
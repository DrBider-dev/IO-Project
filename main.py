import flet as ft
import numpy as np
from solver.solver_wrapper import SolverWrapper
from ui.components import Style, create_header
from ui.input_form import render_input_form
from ui.table_renderer import render_all_tables_cascade
from ui.results_display import create_final_summary

def main(page: ft.Page):
    page.title = "Optimización de Producción - Equipo 6"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"
    page.padding = 40

    # Estado global
    state = {
        "method": "simplex",
        "tablas": [],
        "inputs_c": [],
        "inputs_A": [],
        "inputs_b": [],
        "inputs_signs": []
    }

    # Contenedores
    input_container = ft.Column()
    results_container = ft.Column()

    # --- Cambio de tema ---
    def on_theme_change(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE_OUTLINED
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE_OUTLINED
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE_OUTLINED,
        tooltip="Cambiar tema",
        on_click=on_theme_change
    )

    # --- Métodos ---
    def on_simplex_select(e):
        state["method"] = "simplex"
        update_method_buttons()

    def on_dos_fases_select(e):
        state["method"] = "dos_fases"
        update_method_buttons()

    def update_method_buttons():
        if state["method"] == "simplex":
            btn_simplex.bgcolor = Style.PRIMARY
            btn_simplex.color = "white"
            btn_dos_fases.bgcolor = Style.SECONDARY
            btn_dos_fases.color = "black"
        else:
            btn_simplex.bgcolor = Style.SECONDARY
            btn_simplex.color = "black"
            btn_dos_fases.bgcolor = Style.PRIMARY
            btn_dos_fases.color = "white"
        page.update()

    btn_simplex = ft.ElevatedButton("Simplex", on_click=on_simplex_select, bgcolor=Style.PRIMARY, color="white")
    btn_dos_fases = ft.ElevatedButton("Dos Fases", on_click=on_dos_fases_select, bgcolor=Style.SECONDARY, color="black")

    # --- Generación de formulario ---
    def on_generate_form(e):
        try:
            n_v = int(txt_vars.value)
            n_r = int(txt_restrictions.value)
            if n_v < 1 or n_r < 1:
                raise ValueError("Mínimo 1 variable y 1 restricción")
            generate_form(n_v, n_r)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()

    def generate_form(n_v, n_r):
        input_container.controls.clear()
        results_container.controls.clear()
        
        form_container, inputs_c, inputs_A, inputs_b, inputs_signs = render_input_form(
            n_v, n_r, on_calculate
        )
        
        state["inputs_c"] = inputs_c
        state["inputs_A"] = inputs_A
        state["inputs_b"] = inputs_b
        state["inputs_signs"] = inputs_signs
        
        input_container.controls.append(form_container)
        page.update()

    # --- Cálculo y visualización ---
    def on_calculate(e):
        try:
            c = [float(i.value) for i in state["inputs_c"]]
            A = [[float(i.value) for i in fila] for fila in state["inputs_A"]]
            b = [float(i.value) for i in state["inputs_b"]]
            signos_ui = [sign.value for sign in state["inputs_signs"]]
            signos = ["le" if s == "≤" else "ge" if s == "≥" else "=" for s in signos_ui]

            # Resolver
            tablas = SolverWrapper.solve(state["method"], c, A, b, signos)
            state["tablas"] = tablas
            
            # Mostrar resultados
            display_results(tablas, len(c))
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            page.snack_bar.open = True
            page.update()

    def display_results(tablas, n_vars):
        results_container.controls.clear()
        
        # Mostrar todas las tablas en cascada
        tables_view = render_all_tables_cascade(tablas)
        results_container.controls.append(tables_view)
        
        # Mostrar resumen final
        tabla_optima = tablas[-1]["tabla"]
        summary = create_final_summary(tabla_optima, n_vars, state["method"])
        results_container.controls.append(summary)
        
        page.update()

    # --- Layout ---
    txt_vars = ft.TextField(label="Variables", width=120, hint_text="2")
    txt_restrictions = ft.TextField(label="Restricciones", width=120, hint_text="3")

    header_row = ft.Row(
        controls=[create_header(), theme_button],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    controls_row = ft.Row(
        [
            txt_vars,
            txt_restrictions,
            btn_simplex,
            btn_dos_fases,
            ft.IconButton(ft.Icons.SETTINGS_SUGGEST_OUTLINED, on_click=on_generate_form),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True
    )

    main_container = ft.Column(
        controls=[
            header_row,
            controls_row,
            input_container,
            results_container
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(main_container)

if __name__ == "__main__":
    ft.run(main)

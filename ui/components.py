import flet as ft

class Style:
    PRIMARY = ft.Colors.BLUE_900
    SECONDARY = ft.Colors.BLUE_700
    ACCENT = ft.Colors.GREEN_700
    BG_LIGHT = ft.Colors.BLUE_50
    BG_DARK = ft.Colors.BLUE_GREY_900 # Nuevo color para modo oscuro

def create_header():
    return ft.Container(
        content=ft.Column([
            ft.Text("Investigación de Operaciones 1", size=28, weight="bold", color=Style.PRIMARY),
            ft.Text("Optimización de Producción - Universidad Distrital", size=16, color=ft.Colors.GREY_700),
            ft.Divider(color=Style.PRIMARY, height=20)
        ]),
        margin=ft.margin.only(bottom=20)
    )

def create_card(title, content_ui):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(title, weight="bold", size=16, color=Style.SECONDARY),
                content_ui
            ]),
            padding=20
        ),
        elevation=3
    )
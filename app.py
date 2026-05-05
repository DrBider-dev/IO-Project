import flet as ft

def main(page: ft.Page):
    page.title = "Programación Lineal Simplex"
    page.add(ft.Text("✅ Flet funciona en Arch Linux!"))
    page.add(ft.TextField(label="Ingresa tu función objetivo"))
    page.add(ft.ElevatedButton("Resolver", on_click=lambda _: print("Click!")))

ft.app(target=main)
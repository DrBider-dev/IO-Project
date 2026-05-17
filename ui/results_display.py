import flet as ft
import numpy as np
from ui.components import Style

def create_final_summary(tabla_optima, n_vars, method_selected):
    """
    Crea el resumen final con la recomendación de producción.
    """
    valor_maximo = tabla_optima[-1, -1]
    productos = ["Mesas de Comedor", "Sillas Tapizadas", "Libreros Modulares", "Escritorios Ergonómicos"]
    mensajes_produccion = []
    
    for j in range(n_vars):
        columna = tabla_optima[:-1, j]
        if np.sum(columna == 1) == 1 and np.sum(columna == 0) == len(columna) - 1:
            fila_donde_esta_el_uno = np.where(columna == 1)[0][0]
            cantidad = tabla_optima[fila_donde_esta_el_uno, -1]
        else:
            cantidad = 0
        nombre_prod = productos[j] if j < len(productos) else f"Producto {j+1}"
        mensajes_produccion.append(ft.Text(f"• {nombre_prod}: {cantidad:.2f} unidades", size=16))

    metodo_texto = "Simplex" if method_selected == "simplex" else "Dos Fases"
    
    return ft.Container(
        content=ft.Column([
            ft.Text("RECOMENDACIÓN DE PRODUCCIÓN", size=20, weight="bold", color=Style.ACCENT),
            ft.Text(f"Método seleccionado: {metodo_texto}", size=16, weight="bold"),
            ft.Text("Para maximizar la utilidad este mes, la empresa debe fabricar:", size=16),
            ft.Column(mensajes_produccion),
            ft.Divider(),
            ft.Text(f"UTILIDAD MÁXIMA ESTIMADA: COP ${valor_maximo:,.2f}", 
                    size=22, weight="bold", color=Style.PRIMARY),
        ], spacing=10),
        padding=30,
        # AL QUITAR EL BGCOLOR, QUEDA EXACTAMENTE IGUAL AL FONDO DE LA APP
        border_radius=15,
        border=ft.Border.all(2, Style.ACCENT),
        margin=ft.Margin(top=20)
    )
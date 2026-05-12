import numpy as np

class SimplexSolver:
    """Solver para el método Simplex estándar (solo restricciones ≤)"""
    
    @staticmethod
    def resolver(c, A, b):
        """
        Resuelve un problema de programación lineal usando el método Simplex.
        
        Args:
            c: Lista de coeficientes de la función objetivo
            A: Matriz de coeficientes de restricciones
            b: Vector de términos independientes
        
        Returns:
            Lista de diccionarios con el historial de tablas de cada iteración
        """
        num_vars = len(c)
        num_restricciones = len(b)
        nombres_columnas = [f"x{i+1}" for i in range(num_vars)] + [f"s{i+1}" for i in range(num_restricciones)]
        variables_base = [f"s{i+1}" for i in range(num_restricciones)]
        tabla = np.zeros((num_restricciones + 1, len(nombres_columnas) + 1))

        for i in range(num_restricciones):
            tabla[i, :num_vars] = A[i]
            tabla[i, num_vars + i] = 1.0
            tabla[i, -1] = b[i]

        tabla[-1, :num_vars] = -np.array(c)

        tablas_historial = [{
            "tabla": np.copy(tabla),
            "base": variables_base.copy(),
            "columns": nombres_columnas.copy(),
            "phase": "Simplex",
            "iter": 0,
            "entering": None,
            "leaving": None
        }]

        SimplexSolver._simplex_optimize(tabla, nombres_columnas, variables_base, tablas_historial)
        return tablas_historial

    @staticmethod
    def _simplex_optimize(tabla, nombres_columnas, variables_base, tablas_historial, start_iter=0, max_iter=100):
        """Realiza la optimización Simplex iterativa"""
        num_restricciones = tabla.shape[0] - 1
        iteracion = start_iter

        while True:
            if np.all(tabla[-1, :-1] >= -1e-9):
                break

            col_pivote = np.argmin(tabla[-1, :-1])
            razones = []
            for i in range(num_restricciones):
                valor_pivote = tabla[i, col_pivote]
                if valor_pivote > 1e-9:
                    razones.append(tabla[i, -1] / valor_pivote)
                else:
                    razones.append(np.inf)

            if min(razones) == np.inf:
                raise ValueError("El problema no está acotado.")

            fila_pivote = np.argmin(razones)
            entering = nombres_columnas[col_pivote]
            leaving = variables_base[fila_pivote]
            variables_base[fila_pivote] = entering
            tabla = SimplexSolver._pivot(tabla, fila_pivote, col_pivote)
            iteracion += 1
            tablas_historial.append({
                "tabla": np.copy(tabla),
                "base": variables_base.copy(),
                "columns": nombres_columnas.copy(),
                "phase": "Simplex",
                "iter": iteracion,
                "entering": entering,
                "leaving": leaving
            })

            if iteracion >= max_iter:
                break

        return tabla, variables_base

    @staticmethod
    def _pivot(tabla, fila, col):
        """Realiza la operación de pivote en la tabla Simplex"""
        tabla[fila, :] /= tabla[fila, col]
        for i in range(tabla.shape[0]):
            if i != fila:
                tabla[i, :] -= tabla[i, col] * tabla[fila, :]
        return tabla

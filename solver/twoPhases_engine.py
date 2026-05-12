import numpy as np

class TwoPhaseSolver:
    """Solver para el método Dos Fases (soporta restricciones ≤, ≥, =)"""
    
    @staticmethod
    def resolver(c, A, b, signos=None):
        """
        Resuelve un problema de programación lineal usando el método Dos Fases.
        
        Args:
            c: Lista de coeficientes de la función objetivo
            A: Matriz de coeficientes de restricciones
            b: Vector de términos independientes
            signos: Lista con tipos de restricciones ('le', 'ge', '=')
        
        Returns:
            Lista de diccionarios con el historial de tablas de cada iteración
        """
        if signos is None:
            signos = ["le"] * len(b)
        
        return TwoPhaseSolver._resolver_dos_fases(c, A, b, signos)

    @staticmethod
    def _build_phase1_table(c, A, b, signos):
        """Construye la tabla inicial para la Fase 1"""
        num_vars = len(c)
        num_restricciones = len(b)
        nombres_columnas = [f"x{i+1}" for i in range(num_vars)]
        variables_base = []
        slack_columns = [None] * num_restricciones
        excess_columns = [None] * num_restricciones
        artificial_columns = [None] * num_restricciones

        for i, sign in enumerate(signos):
            if sign == "le":
                slack_columns[i] = len(nombres_columnas)
                nombres_columnas.append(f"s{i+1}")
                variables_base.append(f"s{i+1}")
            elif sign == "ge":
                excess_columns[i] = len(nombres_columnas)
                nombres_columnas.append(f"e{i+1}")
                artificial_columns[i] = len(nombres_columnas)
                nombres_columnas.append(f"a{i+1}")
                variables_base.append(f"a{i+1}")
            elif sign == "=":
                artificial_columns[i] = len(nombres_columnas)
                nombres_columnas.append(f"a{i+1}")
                variables_base.append(f"a{i+1}")
            else:
                raise ValueError(f"Tipo de restricción desconocido: {sign}")

        tabla = np.zeros((num_restricciones + 1, len(nombres_columnas) + 1))
        for i in range(num_restricciones):
            tabla[i, :num_vars] = A[i]
            if signos[i] == "le":
                tabla[i, slack_columns[i]] = 1.0
            elif signos[i] == "ge":
                tabla[i, excess_columns[i]] = -1.0
                tabla[i, artificial_columns[i]] = 1.0
            elif signos[i] == "=":
                tabla[i, artificial_columns[i]] = 1.0
            tabla[i, -1] = b[i]

        tabla[-1, :] = 0.0
        for ai in artificial_columns:
            if ai is not None:
                tabla[-1, ai] = -1.0
        for i, ai in enumerate(artificial_columns):
            if ai is not None:
                tabla[-1, :] += tabla[i, :]

        tabla[-1, :] *= -1.0
        return tabla, nombres_columnas, variables_base, artificial_columns

    @staticmethod
    def _simplex_optimize(tabla, nombres_columnas, variables_base, tablas_historial, phase="Fase", start_iter=0, max_iter=100):
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
            tabla = TwoPhaseSolver._pivot(tabla, fila_pivote, col_pivote)
            iteracion += 1
            tablas_historial.append({
                "tabla": np.copy(tabla),
                "base": variables_base.copy(),
                "columns": nombres_columnas.copy(),
                "phase": phase,
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

    @staticmethod
    def _remove_artificial_columns(tabla, nombres_columnas, variables_base, artificial_columns):
        """Elimina las columnas artificiales después de la Fase 1"""
        artificial_indices = [idx for idx in artificial_columns if idx is not None]
        if not artificial_indices:
            return tabla, nombres_columnas, variables_base

        num_restricciones = tabla.shape[0] - 1
        for i, ai in enumerate(artificial_columns):
            if ai is None:
                continue
            if variables_base[i] == nombres_columnas[ai]:
                pivot_candidate = None
                for j in range(len(nombres_columnas)):
                    if j in artificial_indices:
                        continue
                    if not np.isclose(tabla[i, j], 0.0):
                        pivot_candidate = j
                        break

                if pivot_candidate is None:
                    if not np.isclose(tabla[i, -1], 0.0):
                        raise ValueError("No existe solución factible: la variable artificial no puede ser eliminada.")
                    variables_base[i] = "0"
                else:
                    variables_base[i] = nombres_columnas[pivot_candidate]
                    tabla = TwoPhaseSolver._pivot(tabla, i, pivot_candidate)

        keep_cols = [j for j in range(len(nombres_columnas)) if j not in artificial_indices]
        keep_cols.append(tabla.shape[1] - 1)
        tabla = tabla[:, keep_cols]
        nombres_columnas = [nombres_columnas[j] for j in keep_cols[:-1]]

        return tabla, nombres_columnas, variables_base

    @staticmethod
    def _resolver_dos_fases(c, A, b, signos):
        """Resuelve el problema usando el método Dos Fases"""
        tabla, nombres_columnas, variables_base, artificial_columns = TwoPhaseSolver._build_phase1_table(c, A, b, signos)
        tablas_historial = [{
            "tabla": np.copy(tabla),
            "base": variables_base.copy(),
            "columns": nombres_columnas.copy(),
            "phase": "Fase 1",
            "iter": 0,
            "entering": None,
            "leaving": None
        }]

        TwoPhaseSolver._simplex_optimize(tabla, nombres_columnas, variables_base, tablas_historial, phase="Fase 1")

        if not np.isclose(tabla[-1, -1], 0.0, atol=1e-6):
            raise ValueError("No existe solución factible para la fase 1.")

        tabla, nombres_columnas, variables_base = TwoPhaseSolver._remove_artificial_columns(
            tabla, nombres_columnas, variables_base, artificial_columns
        )

        tabla[-1, :] = 0.0
        for j, col in enumerate(nombres_columnas):
            if col.startswith("x"):
                idx = int(col[1:]) - 1
                tabla[-1, j] = -c[idx]

        for i, basic in enumerate(variables_base):
            if basic.startswith("x"):
                idx = int(basic[1:]) - 1
                tabla[-1, :] += c[idx] * tabla[i, :]

        tablas_historial.append({
            "tabla": np.copy(tabla),
            "base": variables_base.copy(),
            "columns": nombres_columnas.copy(),
            "phase": "Fase 2",
            "iter": 0,
            "entering": None,
            "leaving": None
        })

        TwoPhaseSolver._simplex_optimize(tabla, nombres_columnas, variables_base, tablas_historial, phase="Fase 2")
        return tablas_historial

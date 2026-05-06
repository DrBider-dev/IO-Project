import numpy as np

class SimplexSolver:
    @staticmethod
    def resolver(c, A, b):
        num_vars = len(c)
        num_restricciones = len(b)
        
        # Tabla inicial [ A | I | b ]
        columnas_totales = num_vars + num_restricciones + 1
        tabla = np.zeros((num_restricciones + 1, columnas_totales))
        
        for i in range(num_restricciones):
            tabla[i, :num_vars] = A[i]
            tabla[i, num_vars + i] = 1.0
            tabla[i, -1] = b[i]
            
        for j in range(num_vars):
            tabla[-1, j] = -c[j]
            
        tablas_historial = [np.copy(tabla)]
        iteracion = 0
        
        while True:
            if np.all(tabla[-1, :-1] >= -1e-9):
                break
                
            col_pivote = np.argmin(tabla[-1, :-1])
            razones = []
            for i in range(num_restricciones):
                if tabla[i, col_pivote] > 1e-9:
                    razones.append(tabla[i, -1] / tabla[i, col_pivote])
                else:
                    razones.append(np.inf)
                    
            if min(razones) == np.inf:
                raise ValueError("El problema no está acotado.")
                
            fila_pivote = np.argmin(razones)
            valor_pivote = tabla[fila_pivote, col_pivote]
            tabla[fila_pivote, :] /= valor_pivote
            
            for i in range(num_restricciones + 1):
                if i != fila_pivote:
                    multiplicador = tabla[i, col_pivote]
                    tabla[i, :] -= multiplicador * tabla[fila_pivote, :]
                    
            tablas_historial.append(np.copy(tabla))
            iteracion += 1
            if iteracion > 50: break
                
        return tablas_historial
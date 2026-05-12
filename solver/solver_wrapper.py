from solver.simplex_engine import SimplexSolver
from solver.twoPhases_engine import TwoPhaseSolver

class SolverWrapper:
    """Wrapper que unifica el acceso a ambos métodos de resolución"""
    
    @staticmethod
    def solve(method, c, A, b, signos=None):
        """
        Resuelve un problema de PL usando el método especificado.
        
        Args:
            method: 'simplex' o 'dos_fases'
            c: Coeficientes de función objetivo
            A: Matriz de restricciones
            b: Términos independientes
            signos: Tipos de restricciones (solo para dos_fases)
        
        Returns:
            Lista de diccionarios con historial de tablas
        
        Raises:
            ValueError: Si el método es desconocido o los datos son inválidos
        """
        if method == "simplex":
            if signos and any(sign != "le" for sign in signos):
                raise ValueError("El método Simplex estándar solo soporta restricciones ≤ (le).")
            return SimplexSolver.resolver(c, A, b)
        elif method == "dos_fases":
            if signos is None:
                signos = ["le"] * len(b)
            return TwoPhaseSolver.resolver(c, A, b, signos=signos)
        else:
            raise ValueError(f"Método desconocido: {method}")

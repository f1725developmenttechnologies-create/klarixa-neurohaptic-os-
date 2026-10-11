# src/utils/biomechanical_mapper.py
"""
Klarixa NeuroHaptic OS - Biomechanical Mapper
Traduce la dinámica de pulsación humana (Keystroke Dynamics) 
en parámetros de control físico para robots (Impedancia y Cinemática).
"""

import numpy as np

class BiomechanicalMapper:
    """
    Convierte firmas neuromusculares humanas en comandos físicos para el Nonacortex.
    """
    
    def __init__(self):
        # Límites físicos de seguridad para el robot (en Newtons y m/s)
        self.MAX_FORCE_N = 5.0       # Fuerza máxima absoluta (para no romper nada)
        self.MAX_VELOCITY_MS = 0.5   # Velocidad máxima del efector final
        
        # Rango típico humano en el dataset CMU (en milisegundos)
        self.HUMAN_HOLD_TIME_MIN = 30.0
        self.HUMAN_HOLD_TIME_MAX = 200.0
        
        self.HUMAN_FLIGHT_TIME_MIN = 10.0
        self.HUMAN_FLIGHT_TIME_MAX = 150.0

    def normalize(self, value, min_val, max_val):
        """Normaliza un valor entre 0.0 y 1.0"""
        if max_val == min_val:
            return 0.5
        return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))

    def map_hold_time_to_force(self, hold_time_ms: float) -> float:
        """
        Traduce el tiempo de presión (hold_time) a Fuerza de Agarre (Newtons).
        Un hold_time más largo y deliberado implica un control de fuerza más fino.
        """
        # Normalizamos el tiempo humano
        norm_hold = self.normalize(hold_time_ms, self.HUMAN_HOLD_TIME_MIN, self.HUMAN_HOLD_TIME_MAX)
        
        # Mapeo inverso: mayor tiempo de presión = menor fuerza bruta (más delicadeza)
        # Aplicamos una curva suave para simular la respuesta muscular
        force = self.MAX_FORCE_N * (1.0 - (norm_hold ** 0.8))
        
        # Aseguramos un mínimo de fuerza para que el robot no suelte el objeto
        return max(0.2, min(force, self.MAX_FORCE_N))

    def map_flight_time_to_velocity(self, flight_time_ms: float) -> float:
        """
        Traduce el tiempo de vuelo (flight_time) a Velocidad de Trayectoria (m/s).
        Un flight_time corto implica movimientos rápidos y seguros.
        """
        norm_flight = self.normalize(flight_time_ms, self.HUMAN_FLIGHT_TIME_MIN, self.HUMAN_FLIGHT_TIME_MAX)
        
        # Mapeo directo: menor tiempo de vuelo = mayor velocidad
        velocity = self.MAX_VELOCITY_MS * (1.0 - norm_flight)
        
        return max(0.05, min(velocity, self.MAX_VELOCITY_MS))

    def get_physical_parameters(self, hold_time_ms: float, flight_time_ms: float) -> dict:
        """
        Calcula todos los parámetros físicos para el Chip de Control del Nonacortex.
        """
        force = self.map_hold_time_to_force(hold_time_ms)
        velocity = self.map_flight_time_to_velocity(flight_time_ms)
        
        # Calculamos la "Suavidad" (Smoothness) basada en la consistencia
        # (En una versión real, esto usaría la desviación estándar de las últimas N pulsaciones)
        smoothness = 1.0 - abs(velocity - 0.25) * 2 

        return {
            "grip_force_N": round(force, 3),
            "trajectory_velocity_ms": round(velocity, 3),
            "motion_smoothness": round(max(0.0, min(1.0, smoothness)), 3),
            "status": "DELICATE_MODE" if force < 1.5 else "STANDARD_MODE"
        }

# --- PRUEBA DE CONCEPTO LOCAL ---
if __name__ == "__main__":
    mapper = BiomechanicalMapper()
    
    # Simulamos un humano tecleando con estrés (hold_time corto, flight_time errático)
    print("🧠 Estrés Humano (Toque rápido y brusco):")
    print(mapper.get_physical_parameters(hold_time_ms=40.0, flight_time_ms=20.0))
    
    # Simulamos un humano acariciando o tocando con delicadeza (hold_time largo)
    print("\n🖐️ Delicadeza Humana (Toque suave y prolongado):")
    print(mapper.get_physical_parameters(hold_time_ms=150.0, flight_time_ms=80.0))
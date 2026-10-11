# src/nonacortex/router.py
"""
Klarixa NeuroHaptic OS - Nonacortex Router (Chip Central)
Orquesta los 9 cerebros especializados basándose en la firma biomécanica.
"""

import sys
import os

# Aseguramos que Python pueda encontrar nuestros módulos en la carpeta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.biomechanical_mapper import BiomechanicalMapper

class NonacortexRouter:
    """
    El Chip Central del Nonacortex 5-3-1.
    Recibe datos crudos de entrada, los procesa y los enruta a los chips especializados.
    """
    
    def __init__(self):
        # Inicializamos el Chip 5 (Control de Fuerza/Delicadeza)
        self.biomechanical_mapper = BiomechanicalMapper()
        
        # Estado actual del sistema (simulado)
        self.current_mode = "STANDBY"
        print("⚡ Nonacortex Router inicializado. 9 cerebros en espera.")

    def process_human_input(self, hold_time_ms: float, flight_time_ms: float, task_type: str):
        """
        Procesa la entrada humana y decide cómo debe actuar el androide.
        """
        # 1. Traducir firma neuromuscular a física
        physical_params = self.biomechanical_mapper.get_physical_parameters(hold_time_ms, flight_time_ms)
        
        # 2. Lógica de Enrutamiento (Routing) basada en el estado
        self.current_mode = physical_params["status"]
        
        response = {
            "task": task_type,
            "mode": self.current_mode,
            "physical_params": physical_params,
            "routed_to": ""
        }

        # 3. Decisión de los 9 Cerebros
        if self.current_mode == "DELICATE_MODE":
            # Si es delicado, activamos los chips de empatía y control fino
            response["routed_to"] = "Chip 4 (Cinemática Suave) + Chip 7 (Empatía)"
            response["action"] = "Ejecutando movimiento de alta precisión y baja fuerza."
        else:
            # Si es estándar, usamos los chips de velocidad y eficiencia
            response["routed_to"] = "Chip 2 (Cinemática Rápida) + Chip 8 (Eficiencia)"
            response["action"] = "Ejecutando movimiento estándar optimizado."

        return response

# --- PRUEBA DE CONCEPTO DEL ROUTER ---
if __name__ == "__main__":
    router = NonacortexRouter()
    
    print("\n--- Escenario 1: Escribiendo en un Smartphone (Delicado) ---")
    result1 = router.process_human_input(
        hold_time_ms=120.0, 
        flight_time_ms=90.0, 
        task_type="typing_on_glass_screen"
    )
    for k, v in result1.items():
        print(f"{k}: {v}")

    print("\n--- Escenario 2: Agarrando una botella de agua (Estándar) ---")
    result2 = router.process_human_input(
        hold_time_ms=45.0, 
        flight_time_ms=30.0, 
        task_type="grasping_water_bottle"
    )
    for k, v in result2.items():
        print(f"{k}: {v}")
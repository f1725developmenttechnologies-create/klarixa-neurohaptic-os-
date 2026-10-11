# src/nonacortex/unified_router.py
"""
Klarixa NeuroHaptic OS - Unified Nonacortex Router (v2.0)
Fusiona Biometría, Contexto Ambiental y Memoria Evolutiva.
"""

import sys
import os

# Ajuste de rutas para móviles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.biomechanical_mapper import BiomechanicalMapper
from sensors.context_bridge import ContextSensorBridge
from nonacortex.learning_memory import LearningMemory

class UnifiedRouter:
    """
    El Cerebro Central definitivo.
    Ninguna acción física se ejecuta sin pasar por este filtro de 3 capas.
    """
    
    def __init__(self):
        self.mapper = BiomechanicalMapper()
        self.bridge = ContextSensorBridge()
        self.memory = LearningMemory(forget_rate=0.2, clone_rate=0.5)
        print(" Unified Nonacortex Router Online. 9-Chip Architecture Active.")

    def process_input(self, hold_time: float, flight_time: float, task: str):
        """
        Procesa la entrada humana, verifica el entorno y aplica la memoria.
        """
        # CAPA 1: Biometría Base (El tecleo)
        bio_params = self.mapper.get_physical_parameters(hold_time, flight_time)
        bio_state = bio_params["status"]

        # CAPA 2: Contexto Ambiental (Los sensores del OS)
        context = self.bridge.read_all_sensors()
        discrepancy = self.bridge.evaluate_context_discrepancy(bio_state)

        # CAPA 3: Lógica de Anulación (El "Modo Cuidador")
        final_mode = bio_state
        if context["thermal"]["status"] == "FEVER" or context["proximity"]["status"] == "INTRUSION":
            final_mode = "CAREGIVER_MODE"
            # Forzar delicadeza extrema
            bio_params["grip_force_N"] = min(bio_params["grip_force_N"], 0.5)
            bio_params["motion_smoothness"] = 0.95
            bio_params["status"] = "CAREGIVER_MODE"

        # CAPA 4: Memoria Evolutiva (Clonación de éxitos)
        if self.memory.successes_db:
            best_params = self.memory.get_best_parameters()
            bio_params.update(best_params)

        # Salida final del Nonacortex
        return {
            "task": task,
            "final_mode": final_mode,
            "environmental_context": context,
            "discrepancy_check": discrepancy,
            "final_physical_params": bio_params
        }

# --- PRUEBA DE CONCEPTO ---
if __name__ == "__main__":
    router = UnifiedRouter()
    
    print("\n--- Simulación: Usuario con Fiebre tecleando normal ---")
    result = router.process_input(
        hold_time=100.0, 
        flight_time=80.0, 
        task="handing_water_glass"
    )
    
    print(f"Modo Final: {result['final_mode']}")
    print(f"Contexto Térmico: {result['environmental_context']['thermal']}")
    print(f"Fuerza Aplicada: {result['final_physical_params']['grip_force_N']} N")
    print(f"Discrepancia: {result['discrepancy_check']}")
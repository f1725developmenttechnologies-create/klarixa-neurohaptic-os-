# src/simulation/training_loop.py
"""
Klarixa NeuroHaptic OS - Training Loop
Simula el aprendizaje del Nonacortex: actúa, evalúa, olvida errores y clona éxitos.
"""

import sys
import os

# Ajuste de rutas para que los imports funcionen desde cualquier carpeta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_loader import CMUDataLoader
from nonacortex.router import NonacortexRouter
from simulation.robot_env import NeuroHapticEnv
from nonacortex.learning_memory import LearningMemory

def run_training_simulation(iterations=5):
    print("⚡ Iniciando Bucle de Entrenamiento NeuroHaptic...")
    print("--------------------------------------------------")

    # 1. Inicializar componentes
    loader = CMUDataLoader("data/raw/DSL-StrongPasswordData.csv")
    loader.load_dataset()
    
    router = NonacortexRouter()
    env = NeuroHapticEnv("smartphone_screen")
    memory = LearningMemory(forget_rate=0.5, clone_rate=1.0) # Olvido rápido, clonación agresiva

    # Obtenemos la firma base del humano
    signature = loader.get_user_signature("S002")

    # 2. Bucle de aprendizaje
    for i in range(1, iterations + 1):
        print(f"\n Intento #{i}")
        
        # A. El Nonacortex calcula los parámetros base
        base_result = router.process_human_input(
            hold_time_ms=signature["avg_hold_time_ms"],
            flight_time_ms=signature["avg_flight_time_ms"],
            task_type="smartphone_typing"
        )
        params = base_result["physical_params"]

        # B. La Memoria Interfiere: Si hay un éxito aprendido, lo usamos en lugar del base
        if memory.successes_db:
            print("🧠 Memoria: Aplicando éxito clonado...")
            params = memory.get_best_parameters()

        # C. El Entorno Físico evalúa la acción
        outcome_msg = env.step(params)
        success = not env.is_broken
        print(outcome_msg)

        # D. La Memoria registra el resultado
        memory.record_outcome(params, success)

        # E. Actualización de la memoria (Olvidar y Clonar)
        memory.forget_errors()
        memory.clone_successes()

        # Reiniciamos el entorno para el siguiente intento
        env.is_broken = False 

    print("\n--------------------------------------------------")
    print("🏁 Entrenamiento finalizado.")
    print("📊 Estadísticas finales de la memoria:")
    stats = memory.get_stats()
    for k, v in stats.items():
        print(f"  - {k}: {v}")

if __name__ == "__main__":
    # Ejecutamos 5 intentos para ver la evolución
    run_training_simulation(iterations=5)
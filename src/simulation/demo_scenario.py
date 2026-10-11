# src/simulation/demo_scenario.py
"""
Klarixa NeuroHaptic OS - Final Demo Scenario
Simula la interacción completa: Biometría + Contexto + Prevención de Daños.
Escenario: Servir una taza de café caliente con una persona cerca.
"""

import sys
import os

# Ajuste de rutas para que los imports funcionen desde la carpeta simulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nonacortex.unified_router import UnifiedRouter
from safety.hazard_avoidance import HazardAvoidanceSystem

def run_hot_cup_scenario():
    print("⚡ KLARIXA NeuroHaptic OS - Escenario Demo: Taza Caliente + Bystander")
    print("=" * 65)
    
    # 1. Inicializar Cerebro (Nonacortex) y Seguridad (Hazard Avoidance)
    brain = UnifiedRouter()
    safety = HazardAvoidanceSystem()
    
    # 2. Estado del Entorno (Simulado por los sensores del OS)
    # Taza de cerámica con líquido a 85°C
    object_state = {"temperature_c": 85.0, "material": "ceramic"}
    # Persona (bystander) a solo 20 cm de distancia
    bystander_state = {"distance_cm": 20.0} 
    
    # 3. Entrada Humana (El usuario teclea con calma)
    hold_time = 100.0
    flight_time = 80.0
    task = "serving_hot_beverage"
    
    print(f"\n[1] Nonacortex procesando entrada humana (Tarea: {task})...")
    brain_output = brain.process_input(hold_time, flight_time, task)
    
    # Parámetros que el cerebro planeaba ejecutar inicialmente
    planned_velocity = brain_output["final_physical_params"]["trajectory_velocity_ms"]
    planned_force = brain_output["final_physical_params"]["grip_force_N"]
    
    print(f"    -> Velocidad planeada inicial: {planned_velocity} m/s")
    print(f"    -> Fuerza de agarre planeada: {planned_force} N")
    
    # 4. Intercepción de Seguridad (El Instinto de Protección)
    print(f"\n[2] Sistema de Seguridad (Hazard Avoidance) evaluando entorno...")
    print(f"    -> Objeto detectado: {object_state['material']} a {object_state['temperature_c']}°C")
    print(f"    -> Bystander detectado a: {bystander_state['distance_cm']} cm")
    
    safety_output = safety.evaluate_scenario(object_state, bystander_state, planned_velocity)
    
    # 5. Resolución Final del Nonacortex
    print(f"\n[3] Resolución Final del Nonacortex:")
    print(f"    -> Nivel de Riesgo: {safety_output['risk_level']}")
    print(f"    -> Acción Ejecutada: {safety_output['overrides']['action']}")
    print(f"    -> Alerta del Sistema: {safety_output['overrides']['alert']}")
    
    # La velocidad final es la que realmente se envía a los motores del robot
    final_velocity = safety_output['overrides'].get('trajectory_velocity_ms', planned_velocity)
    print(f"\n    -> VELOCIDAD FINAL ENVIADA A MOTORES: {final_velocity} m/s")
    
    print("\n" + "=" * 65)
    print("✅ Demo completada. El androide evitó quemar al bystander y romper la taza.")

if __name__ == "__main__":
    run_hot_cup_scenario()
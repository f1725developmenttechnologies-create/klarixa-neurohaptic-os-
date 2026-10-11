# src/safety/hazard_avoidance.py
"""
Klarixa NeuroHaptic OS - Dynamic Hazard Avoidance
Previene daños colaterales: no quema, no rompe, no golpea.
"""

class HazardAvoidanceSystem:
    """
    Sub-sistema de seguridad que intercepta los comandos del Nonacortex.
    Si detecta un objeto peligroso (caliente/frágil) y un obstáculo dinámico (persona),
    anula el movimiento y ejecuta una trayectoria evasiva.
    """
    
    def __init__(self):
        print("🛡️ Sistema de Prevención de Daños Colaterales Activo.")
        self.SAFE_DISTANCE_CM = 30.0
        self.HOT_OBJECT_THRESHOLD_C = 50.0

    def evaluate_scenario(self, object_state: dict, bystander_state: dict, planned_velocity: float):
        """
        Analiza si el movimiento planeado es seguro para el entorno.
        """
        risk_level = "LOW"
        override_params = {}

        # 1. Detección de Objeto Peligroso (Ej: Taza con líquido caliente)
        is_hot = object_state.get("temperature_c", 20) > self.HOT_OBJECT_THRESHOLD_C
        is_fragile = object_state.get("material", "plastic") == "ceramic"

        # 2. Detección de Obstáculo Dinámico (Ej: Alguien acercándose)
        bystander_close = bystander_state.get("distance_cm", 100) < self.SAFE_DISTANCE_CM

        # Lógica de Intervención de Seguridad
        if is_hot and bystander_close:
            risk_level = "CRITICAL"
            # Anular velocidad planeada para evitar salpicaduras
            override_params["trajectory_velocity_ms"] = 0.05 # Movimiento ultra lento
            override_params["action"] = "FREEZE_AND_RETRACT"
            override_params["alert"] = "⚠️ ¡ALERTA! Taza caliente detectada. Persona cerca. Deteniendo movimiento para evitar quemaduras."
            
        elif is_fragile and bystander_close:
            risk_level = "HIGH"
            # Reducir velocidad para no romper la taza por inercia
            override_params["trajectory_velocity_ms"] = min(planned_velocity, 0.1)
            override_params["action"] = "SLOW_DOWN"
            override_params["alert"] = "⚠️ Objeto frágil con personas cerca. Reduciendo inercia."
            
        else:
            override_params["action"] = "CONTINUE_PLANNED_PATH"
            override_params["alert"] = "✅ Entorno seguro. Continuando trayectoria."

        return {
            "risk_level": risk_level,
            "overrides": override_params
        }

# --- PRUEBA DE CONCEPTO ---
if __name__ == "__main__":
    safety_sys = HazardAvoidanceSystem()
    
    print("\n--- Escenario: Taza de café caliente (85°C) y persona a 20cm ---")
    result = safety_sys.evaluate_scenario(
        object_state={"temperature_c": 85, "material": "ceramic"},
        bystander_state={"distance_cm": 20},
        planned_velocity=0.4
    )
    
    print(f"Nivel de Riesgo: {result['risk_level']}")
    print(f"Acción: {result['overrides']['action']}")
    print(f"Alerta: {result['overrides']['alert']}")
    if "trajectory_velocity_ms" in result['overrides']:
        print(f"Nueva Velocidad: {result['overrides']['trajectory_velocity_ms']} m/s")
# src/simulation/robot_env.py
"""
Klarixa NeuroHaptic OS - Mock Physics Environment
Simula la respuesta física del entorno (MuJoCo/Isaac Sim) a los comandos del Nonacortex.
"""

class NeuroHapticEnv:
    """
    Simula un objeto frágil en el mundo real y evalúa si el robot lo rompe.
    """
    
    def __init__(self, object_name="smartphone_screen"):
        self.object_name = object_name
        # Umbral de rotura en Newtons (Simulación de física de materiales)
        # Una pantalla de vidrio típica se rompe con impactos > 1.5N en un punto pequeño
        self.breaking_threshold_N = 1.5 
        self.is_broken = False
        self.history = []

    def step(self, physical_params: dict):
        """
        Aplica los parámetros físicos generados por el Nonacortex al objeto.
        """
        force = physical_params["grip_force_N"]
        velocity = physical_params["trajectory_velocity_ms"]
        
        # Lógica de colisión y daño
        if force > self.breaking_threshold_N:
            self.is_broken = True
            result = f"💥 FALLO CRÍTICO: El {self.object_name} se rompió. Fuerza: {force}N > Umbral: {self.breaking_threshold_N}N"
        else:
            result = f"✅ ÉXITO: Interacción delicada lograda. Fuerza: {force}N | Velocidad: {velocity}m/s"
            
        self.history.append(result)
        return result

    def get_status(self):
        """Retorna el estado actual del objeto."""
        status = "ROTO" if self.is_broken else "INTEGRAL"
        return f"[Estado del {self.object_name}: {status}]"

# --- PRUEBA DE CONCEPTO DEL ENTORNO ---
if __name__ == "__main__":
    env = NeuroHapticEnv("smartphone_screen")
    
    # Simulamos un comando brusco (Modo Estándar)
    print(env.step({"grip_force_N": 2.5, "trajectory_velocity_ms": 0.4}))
    print(env.get_status())
    
    # Reiniciamos para probar el modo delicado
    env.is_broken = False 
    
    # Simulamos un comando suave (Modo Delicado)
    print("\n" + env.step({"grip_force_N": 0.8, "trajectory_velocity_ms": 0.1}))
    print(env.get_status())
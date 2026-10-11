# src/nonacortex/learning_memory.py
"""
Klarixa NeuroHaptic OS - Learning Memory
Mecanismo de refuerzo selectivo: olvida errores, clona éxitos.
"""

import copy

class LearningMemory:
    """
    Mantiene dos bases de datos:
    - Errores: se repiten virtualmente hasta que su peso llega a cero (se olvidan).
    - Éxitos: se clonan (su peso aumenta) para que el sistema siempre los replique.
    """
    
    def __init__(self, forget_rate=0.1, clone_rate=0.2):
        # Base de datos de errores: {param_key: {"params": {...}, "weight": float}}
        self.errors_db = {}
        
        # Base de datos de éxitos: {param_key: {"params": {...}, "weight": float}}
        self.successes_db = {}
        
        # Tasa de olvido (cuánto se reduce el peso de un error por iteración)
        self.forget_rate = forget_rate
        
        # Tasa de clonación (cuánto aumenta el peso de un éxito por iteración)
        self.clone_rate = clone_rate
        
        print("🧠 Memoria de Aprendizaje inicializada.")

    def _generate_key(self, params: dict) -> str:
        """Genera una clave única basada en los parámetros físicos."""
        return f"force_{params['grip_force_N']}_vel_{params['trajectory_velocity_ms']}"

    def record_outcome(self, params: dict, success: bool):
        """
        Registra el resultado de una acción.
        - Si fue éxito: se añade/clona en successes_db.
        - Si fue error: se añade en errors_db.
        """
        key = self._generate_key(params)
        
        if success:
            if key in self.successes_db:
                # Clonar: aumentar el peso del éxito existente
                self.successes_db[key]["weight"] += self.clone_rate
            else:
                # Nuevo éxito: registrar con peso inicial
                self.successes_db[key] = {
                    "params": copy.deepcopy(params),
                    "weight": 1.0
                }
            print(f"✅ Éxito registrado y clonado: {key} (peso: {self.successes_db[key]['weight']:.2f})")
        else:
            if key in self.errors_db:
                # El error ya existe, no hacemos nada (se olvidará solo)
                pass
            else:
                # Nuevo error: registrar con peso inicial
                self.errors_db[key] = {
                    "params": copy.deepcopy(params),
                    "weight": 1.0
                }
            print(f"❌ Error registrado: {key} (peso: {self.errors_db[key]['weight']:.2f})")

    def forget_errors(self):
        """
        Reduce el peso de todos los errores.
        Cuando el peso llega a 0 o menos, el error se "olvida" (se elimina).
        """
        keys_to_remove = []
        for key, entry in self.errors_db.items():
            entry["weight"] -= self.forget_rate
            if entry["weight"] <= 0:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.errors_db[key]
            print(f"🗑️ Error olvidado: {key}")
        
        print(f" Errores restantes: {len(self.errors_db)}")

    def clone_successes(self):
        """
        Aumenta el peso de todos los éxitos (clonación virtual).
        """
        for key, entry in self.successes_db.items():
            entry["weight"] += self.clone_rate
        
        print(f"📈 Éxitos clonados. Total: {len(self.successes_db)}")

    def get_best_parameters(self) -> dict:
        """
        Retorna los parámetros del éxito con mayor peso (el más clonado).
        Si no hay éxitos, retorna un valor por defecto seguro.
        """
        if not self.successes_db:
            print("⚠️ Sin éxitos registrados. Usando parámetros por defecto seguros.")
            return {
                "grip_force_N": 0.5,
                "trajectory_velocity_ms": 0.1,
                "motion_smoothness": 0.8,
                "status": "SAFE_DEFAULT"
            }
        
        # Encontrar el éxito con mayor peso
        best_key = max(self.successes_db, key=lambda k: self.successes_db[k]["weight"])
        best_params = copy.deepcopy(self.successes_db[best_key]["params"])
        best_params["status"] = "LEARNED_SUCCESS"
        
        print(f"🏆 Mejor parámetro seleccionado: {best_key} (peso: {self.successes_db[best_key]['weight']:.2f})")
        return best_params

    def get_stats(self) -> dict:
        """Retorna estadísticas de la memoria."""
        return {
            "total_errors": len(self.errors_db),
            "total_successes": len(self.successes_db),
            "error_weights": sum(e["weight"] for e in self.errors_db.values()),
            "success_weights": sum(s["weight"] for s in self.successes_db.values())
        }

# --- PRUEBA DE CONCEPTO ---
if __name__ == "__main__":
    memory = LearningMemory(forget_rate=0.3, clone_rate=0.5)
    
    # Simulamos un error (fuerza demasiado alta)
    error_params = {"grip_force_N": 2.5, "trajectory_velocity_ms": 0.4, "motion_smoothness": 0.3}
    memory.record_outcome(error_params, success=False)
    
    # Simulamos un éxito (fuerza delicada)
    success_params = {"grip_force_N": 0.8, "trajectory_velocity_ms": 0.1, "motion_smoothness": 0.9}
    memory.record_outcome(success_params, success=True)
    
    # Clonamos el éxito varias veces
    print("\n--- Clonando éxitos ---")
    for _ in range(3):
        memory.clone_successes()
    
    # Olvidamos errores
    print("\n--- Olvidando errores ---")
    memory.forget_errors()
    memory.forget_errors() # Segunda iteración para olvidar completamente
    
    # Obtenemos el mejor parámetro
    print("\n--- Mejor parámetro aprendido ---")
    best = memory.get_best_parameters()
    print(best)
    
    print("\n--- Estadísticas ---")
    print(memory.get_stats())
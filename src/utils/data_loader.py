# src/utils/data_loader.py
"""
Klarixa NeuroHaptic OS - CMU Data Loader
Ingesta y procesamiento del dataset de Dinámica de Pulsación de CMU.
"""

import csv
import os

class CMUDataLoader:
    """
    Carga y parsea el dataset de CMU para extraer firmas neuromusculares.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.dataset = []
        self.user_profiles = {}

    def load_dataset(self):
        """Carga el CSV crudo y lo estructura en memoria."""
        if not os.path.exists(self.file_path):
            print(f"⚠️ Advertencia: Archivo no encontrado en {self.file_path}. Usando datos simulados.")
            return False

        print(f"📥 Cargando dataset desde: {self.file_path}")
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Limpiamos y convertimos los datos a floats
                try:
                    entry = {
                        "subject": row["subject"],
                        "session": int(row["session"]),
                        "rep": int(row["rep"]),
                        "key": row["key"],
                        "hold_time": float(row["hold_time"]),
                        "flight_time": float(row["flight_time"])
                    }
                    self.dataset.append(entry)
                except (ValueError, KeyError):
                    continue # Saltamos filas corruptas
        
        print(f"✅ Dataset cargado: {len(self.dataset)} muestras de firma neuromuscular.")
        self._build_user_profiles()
        return True

    def _build_user_profiles(self):
        """Agrupa los datos por usuario para calcular su 'firma promedio'."""
        for entry in self.dataset:
            user = entry["subject"]
            if user not in self.user_profiles:
                self.user_profiles[user] = {"hold_times": [], "flight_times": []}
            
            self.user_profiles[user]["hold_times"].append(entry["hold_time"])
            self.user_profiles[user]["flight_times"].append(entry["flight_time"])

    def get_user_signature(self, user_id: str) -> dict:
        """
        Obtiene el promedio de la firma motora de un usuario específico.
        Esto simula el 'estado base' del humano para el Nonacortex.
        """
        if user_id not in self.user_profiles:
            return {"avg_hold": 100.0, "avg_flight": 80.0} # Fallback
        
        profile = self.user_profiles[user_id]
        avg_hold = sum(profile["hold_times"]) / len(profile["hold_times"])
        avg_flight = sum(profile["flight_times"]) / len(profile["flight_times"])
        
        return {
            "user_id": user_id,
            "avg_hold_time_ms": round(avg_hold, 2),
            "avg_flight_time_ms": round(avg_flight, 2),
            "samples": len(profile["hold_times"])
        }

# --- PRUEBA DE CONCEPTO ---
if __name__ == "__main__":
    # Ruta relativa (ajustar según la estructura final del repo)
    loader = CMUDataLoader("data/raw/DSL-StrongPasswordData.csv")
    if loader.load_dataset():
        # Obtenemos la firma del primer usuario (S002 suele ser el primero en este dataset)
        signature = loader.get_user_signature("S002")
        print("\n🧬 Firma Neuromuscular Extraída (Usuario S002):")
        print(signature)
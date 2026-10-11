# src/sensors/context_bridge.py
"""
Klarixa NeuroHaptic OS - Context Sensor Bridge (Sub-Capa HAL)
Unifica los sensores físicos del dispositivo (Android OS) en un solo paquete de contexto.
Evita discrepancias entre la biometría (tecleo) y el entorno físico.
"""

import random

class ContextSensorBridge:
    """
    Sub-capa que abstrae los sensores del Hardware (Android/iOS).
    En producción, esto se conecta a las APIs nativas (ej. Android SensorManager).
    Aquí simulamos la lectura para la arquitectura del Nonacortex.
    """
    
    def __init__(self):
        print(" Sub-capa de Sensores Contextuales inicializada.")
        # Umbrales de alerta
        self.TEMP_FEVER_THRESHOLD = 37.5
        self.PROXIMITY_ALERT_CM = 10.0

    def read_all_sensors(self) -> dict:
        """
        Lee todos los sensores y devuelve un 'Paquete de Contexto' unificado.
        """
        # En un dispositivo real, aquí se llamaría a las APIs de Android
        # Por ahora, simulamos lecturas realistas para probar el Nonacortex
        context = {
            "thermal": self._get_thermal_state(),
            "proximity": self._get_proximity_state(),
            "audio": self._get_audio_state(),
            "optical": self._get_optical_state(),
            "timestamp": "2026-10-11T12:00:00Z"
        }
        return context

    def _get_thermal_state(self) -> dict:
        """Sensor de temperatura (Infrarrojo / Batería / Ambiente)"""
        # Simulación: 36.8 es normal, >37.5 es fiebre
        temp = random.uniform(36.0, 38.2) 
        status = "FEVER" if temp > self.TEMP_FEVER_THRESHOLD else "NORMAL"
        return {"value_celsius": round(temp, 1), "status": status}

    def _get_proximity_state(self) -> dict:
        """Sensor de proximidad (Detecta si el usuario está muy cerca)"""
        # Simulación: distancia en cm
        distance = random.uniform(5.0, 50.0)
        status = "INTRUSION" if distance < self.PROXIMITY_ALERT_CM else "SAFE"
        return {"distance_cm": round(distance, 1), "status": status}

    def _get_audio_state(self) -> dict:
        """Micrófono (Analiza nivel de ruido y tono de voz)"""
        # Simulación: decibeles (dB)
        db_level = random.randint(30, 90)
        status = "HIGH_STRESS" if db_level > 75 else "CALM"
        return {"decibels": db_level, "status": status}

    def _get_optical_state(self) -> dict:
        """Cámara / Sensor de luz (Analiza iluminación y fatiga visual)"""
        # Simulación: Lux (iluminación)
        lux = random.randint(10, 800)
        status = "LOW_LIGHT" if lux < 50 else "OPTIMAL"
        return {"lux": lux, "status": status}

    def evaluate_context_discrepancy(self, biomechanical_state: str) -> str:
        """
        Detecta si hay contradicción entre el tecleo y el entorno.
        Ej: Tecleo rápido (Estrés) + Ruido bajo (Calma) = Discrepancia.
        """
        context = self.read_all_sensors()
        discrepancies = []
        
        if biomechanical_state == "STRESS" and context["audio"]["status"] == "CALM":
            discrepancies.append("El tecleo indica estrés, pero el entorno está en calma.")
        if biomechanical_state == "CALM" and context["thermal"]["status"] == "FEVER":
            discrepancies.append("El tecleo es calmado, pero el usuario tiene fiebre (malestar físico).")
            
        if discrepancies:
            return "⚠️ DISCREPANCIA DETECTADA: " + " | ".join(discrepancies)
        return "✅ Contexto coherente."

# --- PRUEBA DE CONCEPTO ---
if __name__ == "__main__":
    bridge = ContextSensorBridge()
    print("\n📡 Lectura de Sensores en Tiempo Real:")
    context = bridge.read_all_sensors()
    for sensor, data in context.items():
        print(f"  - {sensor}: {data}")
        
    print("\n🔍 Análisis de Coherencia:")
    print(bridge.evaluate_context_discrepancy("STRESS"))
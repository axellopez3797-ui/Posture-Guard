"""
Cálculo de ángulos articulares a partir de landmarks de MediaPipe Pose.
"""

import numpy as np

from src.pose_detector import PoseDetector


def calculate_angle(a, b, c):
    """
    Calcula el ángulo en grados en el punto articular b formado por a-b-c.

    Usa arctan2 sobre los vectores BA y BC. Si alguno de los tres puntos
    es None, devuelve None.

    Args:
        a: Tupla (x, y) del primer punto.
        b: Tupla (x, y) del vértice (articulación).
        c: Tupla (x, y) del tercer punto.

    Returns:
        Ángulo en grados (0–180) o None si falta algún punto.
    """
    try:
        if a is None or b is None or c is None:
            return None

        # Vectores desde el vértice b hacia a y c
        radianes_a = np.arctan2(a[1] - b[1], a[0] - b[0])
        radianes_c = np.arctan2(c[1] - b[1], c[0] - b[0])

        angulo_radianes = radianes_c - radianes_a
        angulo_grados = np.abs(np.degrees(angulo_radianes))

        # Normalizar al rango [0, 180]
        if angulo_grados > 180.0:
            angulo_grados = 360.0 - angulo_grados

        return float(angulo_grados)
    except Exception as error:
        print(f"[AngleCalculator] Error al calcular ángulo: {error}")
        return None


def smooth_angle(history: list, new_angle: float, max_frames: int = 5):
    """
    Aplica media móvil sobre un historial de ángulos para reducir jitter.

    Agrega new_angle al historial, lo recorta a max_frames elementos
    y devuelve el promedio de los valores almacenados.

    Args:
        history: Lista mutable donde se acumulan ángulos recientes.
        new_angle: Nuevo ángulo medido en el frame actual.
        max_frames: Cantidad máxima de frames en el historial.

    Returns:
        Promedio del historial o None si está vacío o new_angle es None.
    """
    try:
        if new_angle is None:
            if not history:
                return None
            return float(np.mean(history))

        history.append(new_angle)

        # Mantener solo los últimos max_frames valores
        if len(history) > max_frames:
            del history[:-max_frames]

        return float(np.mean(history))
    except Exception as error:
        print(f"[AngleCalculator] Error al suavizar ángulo: {error}")
        return None


def extract_angles(landmarks, detector: PoseDetector, frame_w, frame_h):
    """
    Extrae los ángulos posturales clave a partir de los landmarks detectados.

    Usa get_landmark del PoseDetector para obtener coordenadas en píxeles
    y calculate_angle para cada articulación relevante.

    Args:
        landmarks: Objeto pose_landmarks devuelto por PoseDetector.process_frame.
        detector: Instancia de PoseDetector para resolver coordenadas.
        frame_w: Ancho del frame en píxeles.
        frame_h: Alto del frame en píxeles.

    Returns:
        Dict con claves neck_tilt, spine_angle, shoulder_elevation y knee_angle.
        Cada valor es un float (grados) o None si no se pudo calcular.
    """
    try:
        if landmarks is None:
            return {
                "neck_tilt": None,
                "spine_angle": None,
                "shoulder_elevation": None,
                "knee_angle": None,
            }

        def obtener(indice):
            """Atajo para obtener un landmark en píxeles."""
            return detector.get_landmark(landmarks, indice, frame_w, frame_h)

        # Índices MediaPipe Pose: 0 nariz, 11/12 hombros, 13/15 brazo izq,
        # 23/25/27 pierna izquierda (cadera, rodilla, tobillo)
        nariz = obtener(0)
        hombro_izq = obtener(11)
        hombro_der = obtener(12)
        codo_izq = obtener(13)
        muneca_izq = obtener(15)
        cadera_izq = obtener(23)
        rodilla_izq = obtener(25)
        tobillo_izq = obtener(27)

        return {
            "neck_tilt": calculate_angle(nariz, hombro_izq, hombro_der),
            "spine_angle": calculate_angle(hombro_izq, cadera_izq, rodilla_izq),
            "shoulder_elevation": calculate_angle(hombro_izq, codo_izq, muneca_izq),
            "knee_angle": calculate_angle(cadera_izq, rodilla_izq, tobillo_izq),
        }
    except Exception as error:
        print(f"[AngleCalculator] Error al extraer ángulos: {error}")
        return {
            "neck_tilt": None,
            "spine_angle": None,
            "shoulder_elevation": None,
            "knee_angle": None,
        }

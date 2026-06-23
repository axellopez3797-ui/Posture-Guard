"""
Wrapper de MediaPipe Pose para detección de landmarks corporales en PostureGuard.
"""

import cv2
import mediapipe as mp


class PoseDetector:
    """Encapsula mediapipe.solutions.pose para procesar frames de OpenCV."""

    VISIBILITY_MINIMA = 0.6

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        model_complexity: int = 1,
    ):
        """
        Inicializa el detector de pose de MediaPipe.

        Args:
            min_detection_confidence: Confianza mínima para detectar una pose.
            min_tracking_confidence: Confianza mínima para seguir una pose entre frames.
            model_complexity: Complejidad del modelo (0, 1 o 2).
        """
        self._mp_pose = mp.solutions.pose
        self._mp_drawing = mp.solutions.drawing_utils
        self._pose = self._mp_pose.Pose(
            static_image_mode=False,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process_frame(self, frame):
        """
        Procesa un frame BGR de OpenCV y devuelve los landmarks detectados.

        Convierte el frame a RGB, ejecuta MediaPipe Pose y retorna la lista
        de landmarks normalizados, o None si no se detecta ninguna pose.

        Args:
            frame: Imagen en formato BGR (numpy array de OpenCV).

        Returns:
            Objeto pose_landmarks de MediaPipe o None si no hay detección.
        """
        try:
            if frame is None or frame.size == 0:
                return None

            # MediaPipe espera RGB; OpenCV captura en BGR
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb.flags.writeable = False

            resultados = self._pose.process(frame_rgb)
            return resultados.pose_landmarks
        except Exception as error:
            print(f"[PoseDetector] Error al procesar frame: {error}")
            return None

    def get_landmark(self, landmarks, index, ancho_frame, alto_frame):
        """
        Obtiene las coordenadas (x, y) en píxeles de un landmark.

        Filtra landmarks con visibility inferior a 0.6 y devuelve None
        cuando el punto no es confiable o no está disponible.

        Args:
            landmarks: Objeto pose_landmarks devuelto por process_frame.
            index: Índice del landmark (0-32 en el modelo Pose de MediaPipe).
            ancho_frame: Ancho del frame en píxeles.
            alto_frame: Alto del frame en píxeles.

        Returns:
            Tupla (x, y) en píxeles, o None si el landmark no es válido.
        """
        try:
            if landmarks is None:
                return None

            lista_landmarks = landmarks.landmark
            if index < 0 or index >= len(lista_landmarks):
                return None

            punto = lista_landmarks[index]

            if punto.visibility < self.VISIBILITY_MINIMA:
                return None

            x_pixeles = int(punto.x * ancho_frame)
            y_pixeles = int(punto.y * alto_frame)
            return (x_pixeles, y_pixeles)
        except Exception as error:
            print(f"[PoseDetector] Error al obtener landmark {index}: {error}")
            return None

    def draw_landmarks(self, frame, landmarks):
        """
        Dibuja el esqueleto corporal sobre el frame usando drawing_utils.

        Args:
            frame: Imagen BGR de OpenCV donde se dibujará el skeleton.
            landmarks: Objeto pose_landmarks devuelto por process_frame.

        Returns:
            El mismo frame con los landmarks dibujados (modificación in-place).
        """
        try:
            if frame is None or landmarks is None:
                return frame

            self._mp_drawing.draw_landmarks(
                frame,
                landmarks,
                self._mp_pose.POSE_CONNECTIONS,
                self._mp_drawing.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=2,
                    circle_radius=2,
                ),
                self._mp_drawing.DrawingSpec(
                    color=(0, 0, 255),
                    thickness=2,
                    circle_radius=2,
                ),
            )
            return frame
        except Exception as error:
            print(f"[PoseDetector] Error al dibujar landmarks: {error}")
            return frame

    def close(self):
        """Libera los recursos internos del detector de MediaPipe Pose."""
        try:
            if self._pose is not None:
                self._pose.close()
                self._pose = None
        except Exception as error:
            print(f"[PoseDetector] Error al liberar recursos: {error}")

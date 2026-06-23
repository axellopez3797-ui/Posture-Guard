# 🧍 PostureGuard

> Sistema de reconocimiento de posturas en tiempo real para fisioterapia, oficina y gimnasio usando MediaPipe y OpenCV.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9.0-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📋 Descripción

PostureGuard utiliza la cámara web para detectar en tiempo real los 33 puntos clave del cuerpo humano, calcula ángulos articulares críticos y determina si la postura del usuario es correcta o incorrecta. Emite alertas visuales inmediatas y registra estadísticas de sesión para seguimiento a largo plazo.

**Casos de uso:**
- 🖥️ Trabajadores de oficina — detecta encorvamiento, inclinación cervical y elevación de hombros
- 🏋️ Gimnasio — evalúa sentadilla, peso muerto y press

---

## 🚀 Demo

> *Video/GIF demo próximamente*

---

## 🛠️ Tecnologías

| Librería | Versión | Uso |
|---|---|---|
| MediaPipe | 0.10.9 | Detección de landmarks corporales |
| OpenCV | 4.9.0 | Captura de cámara y overlay visual |
| NumPy | 1.26.4 | Cálculo de ángulos articulares |
| Pandas | 2.2.1 | Registro de sesiones en CSV |
| Matplotlib | 3.8.4 | Dashboard de estadísticas |

---

## 📦 Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/axellopez3797-ui/posture-guard.git
cd posture-guard

# 2. Crea un entorno virtual (recomendado en Cursor)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instala dependencias
pip install -r requirements.txt
```

> ⚠️ Requiere cámara web conectada. Probado en Python 3.10 y 3.11.

---

## 💻 Uso

```bash
# Perfil oficina (postura sentada)
python main.py --profile office

# Perfil gimnasio
python main.py --profile gym

# Con calibración inicial (recomendado la primera vez)
python main.py --profile office --calibrate
```

**Controles durante la sesión:**
- `Q` — salir y ver resumen
- `C` — recalibrar postura de referencia
- `S` — guardar captura del frame actual

---

## 📁 Estructura del proyecto

```
posture-guard/
├── src/
│   ├── pose_detector.py        # Wrapper de MediaPipe Pose
│   ├── angle_calculator.py     # Cálculo de ángulos entre landmarks
│   ├── posture_rules.py        # Motor de reglas por perfil
│   ├── alert_system.py         # Lógica de umbrales y temporizadores
│   ├── overlay.py              # Renderizado del skeleton y alertas en OpenCV
│   └── session_logger.py       # Guardado de sesiones en CSV
├── profiles/
│   ├── office.json             # Umbrales para postura sentada
│   └── gym.json                # Umbrales por ejercicio
├── data/
│   └── sessions/               # CSVs generados por sesión
├── notebooks/
│   └── angle_exploration.ipynb # Exploración de ángulos
├── main.py
├── requirements.txt
└── README.md
```

---

## 🧠 Cómo funciona

```
Cámara → MediaPipe Pose → 33 Landmarks (x, y, z)
    → Extractor de ángulos (cuello, hombros, columna, rodillas)
        → Motor de reglas por perfil
            → Overlay verde/rojo + alerta en pantalla
            → Log CSV de sesión
```

Los ángulos se calculan con la función vectorial:

```python
angle = arctan2(C-B) - arctan2(A-B)   # en el punto articular B
```

Se aplica un filtro de media móvil (5 frames) para eliminar jitter de la cámara, y las alertas solo se activan si la mala postura persiste más de 3 segundos continuos.

---

## 📊 Resultados esperados

| Métrica | Valor objetivo |
|---|---|
| FPS en tiempo real | ≥ 25 fps |
| Latencia de alerta | < 200 ms |
| Precisión de detección | > 90% en condiciones de luz normal |

---

## 🔮 Mejoras futuras

- [ ] Calibración personalizada por usuario
- [ ] Interfaz web con Flask + JavaScript
- [ ] Soporte para múltiples personas en cámara
- [ ] Exportar reporte PDF de sesión
- [ ] App móvil con MediaPipe en browser (WASM)

---

## 👤 Autor

**Axel Lopez** — [@axellopez3797-ui](https://github.com/axellopez3797-ui)

---

## 📄 Licencia

MIT License — libre para uso educativo y personal.

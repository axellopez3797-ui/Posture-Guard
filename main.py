"""
PostureGuard — punto de entrada principal.
Uso:
    python main.py --profile office
    python main.py --profile gym --calibrate
"""

import argparse
import cv2

def parse_args():
    parser = argparse.ArgumentParser(description="PostureGuard")
    parser.add_argument("--profile", choices=["office", "gym"], default="office")
    parser.add_argument("--calibrate", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"[PostureGuard] Iniciando perfil: {args.profile}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] No se encontró cámara.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # TODO: integrar pose_detector, angle_calculator, posture_rules, overlay
        cv2.imshow("PostureGuard", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

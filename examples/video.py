# Copyright 2024 cvpose
# Licensed under the Apache License, Version 2.0

import os
import cv2
import mediapipe as mp
from virtual_landmark import VirtualLandmark, landmark, calculus as calc
from virtual_landmark import Connections, get_extended_pose_landmarks_style

# ==========================
# CUSTOM LANDMARK CLASS
# ==========================

class HelloWorld(VirtualLandmark):
    
    @landmark("MIDDLE_SHOULDER", connection=["RIGHT_SHOULDER", "LEFT_SHOULDER", "NECK"])
    def _middle_shoulder(self):
        return calc.middle(
            self[self.virtual_landmark.RIGHT_SHOULDER],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

    @landmark("NECK", connection=["MIDDLE_SHOULDER", "NOSE"])
    def _neck(self):
        return calc.middle(
            self[self.virtual_landmark.NOSE],
            self[self.virtual_landmark.MIDDLE_SHOULDER],
        )

    @landmark("MIDDLE_HIP", connection=["MIDDLE_SHOULDER", "LEFT_HIP", "RIGHT_HIP"])
    def _middle_hip(self):
        return calc.middle(
            self[self.virtual_landmark.LEFT_HIP],
            self[self.virtual_landmark.RIGHT_HIP],
        )

    @landmark("LEFT_RIB", connection=["LEFT_SHOULDER", "LEFT_HIP"])
    def _left_rib(self):
        return calc.middle(
            self[self.virtual_landmark.LEFT_HIP],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

    @landmark("RIGHT_RIB", connection=["RIGHT_SHOULDER", "RIGHT_HIP"])
    def _right_rib(self):
        return calc.middle(
            self[self.virtual_landmark.RIGHT_HIP],
            self[self.virtual_landmark.RIGHT_SHOULDER],
        )

    @landmark("THORAX", connection=["RIGHT_RIB", "LEFT_RIB", "MIDDLE_SHOULDER", "MIDDLE_HIP"])
    def _thorax(self): 
        return calc.middle(
            self[self.virtual_landmark.RIGHT_RIB],
            self[self.virtual_landmark.LEFT_RIB],
        )
        
# ==========================
# MAIN EXECUTION (VIDEO FILE)
# ==========================

def main():
    # Caminho para o vídeo
    video_path = os.path.join("examples", "videos", "video-1.mp4")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found at: {video_path}")

    # Inicializa captura de vídeo
    cap = cv2.VideoCapture(video_path)
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break  # Fim do vídeo

            # Converte BGR para RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Processa pose
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                # Cria landmarks virtuais
                landmarks = HelloWorld(results.pose_landmarks.landmark)
                connections = Connections(landmarks)
                style = get_extended_pose_landmarks_style(landmarks)

                # Desenha no frame
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=landmarks.as_landmark_list(),
                    connections=connections.ALL_CONNECTIONS,
                    landmark_drawing_spec=style,
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(255, 255, 255), thickness=2
                    ),
                )

            # Mostra o frame processado
            cv2.imshow("Pose Estimation - Video", frame)

            # Sai com 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
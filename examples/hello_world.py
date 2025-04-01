# Copyright 2024 cvpose
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import cv2
import numpy as np
import mediapipe as mp
from virtual_landmark import VirtualLandmark
from virtual_landmark import landmark

import mediapipe as mp

from virtual_landmark.drawing_utils import (
    Connections,
    get_extended_pose_landmarks_style,
)

PoseLandmark = mp.solutions.pose.PoseLandmark

from mediapipe.python.solutions.drawing_styles import get_default_pose_landmarks_style
from virtual_landmark import calculus as tg
# === Create Custom Landmark class ===


class HelloWorld(VirtualLandmark):
    @landmark(
        "MIDDLE_SHOULDER",
        connection=["RIGHT_SHOULDER", "LEFT_SHOULDER", "NECK"],
    )
    def _middle_shoulder(self):
        return tg.middle(
            self[self.virtual_landmark.RIGHT_SHOULDER],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

    @landmark(
        "NECK",
        connection=["MIDDLE_SHOULDER", "NOSE"],
    )
    def _neck(self):
        return tg.middle(
            self[self.virtual_landmark.NOSE],
            self[self.virtual_landmark.MIDDLE_SHOULDER],
        )

    @landmark("PROJECTION")
    def _norm(self):
        return tg.project_point_on_line(
            self[self.virtual_landmark.LEFT_HIP],
            self[self.virtual_landmark.LEFT_KNEE],
            self[self.virtual_landmark.LEFT_SHOULDER]
        )



# === Inicializa o modelo do MediaPipe Pose ===
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=True, model_complexity=2, enable_segmentation=False
)

# === Carrega a imagem ===
image_path = os.path.join(os.getcwd(), "examples", "images", "vitruvian.jpeg")

if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image not found at path: {image_path}")

image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# === Executa a pose no frame ===
results = pose.process(image_rgb)

if results.pose_landmarks:
    # Inicializa desenho (opcional)
    mp_drawing = mp.solutions.drawing_utils

    # Cria objeto de landmarks customizados
    landmarks = HelloWorld(results.pose_landmarks.landmark)

    cc = Connections(landmarks)
    # print(cc.CUSTOM_CONNECTION)

    mp_drawing = mp.solutions.drawing_utils

    img_copy = image.copy()
    mp_drawing.draw_landmarks(
        image=img_copy,
        landmark_list=landmarks.as_landmark_list(),  # results.pose_landmarks,
        connections=Connections(landmarks).ALL_CONNECTIONS,  # mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=get_extended_pose_landmarks_style(landmarks=landmarks),
        connection_drawing_spec=mp_drawing.DrawingSpec(
            color=(255, 255, 255), thickness=1
        ),
    )

    cv2.imshow("Extended Landmarks", img_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("No landmarks detected in the image.")


# === Libera recursos ===
pose.close()

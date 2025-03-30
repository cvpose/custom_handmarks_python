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
from custom_landmarks import CustomLandmark
from custom_landmarks import landmark

import mediapipe as mp

from custom_landmarks.drawing_utils import (
    CustomConnections,
    get_extended_pose_landmarks_style,
)

PoseLandmark = mp.solutions.pose.PoseLandmark

# === Create Custom Landmark class ===


class HelloWorld(CustomLandmark):
    def _middle(self, p1, p2):
        print(type(p1))
        print(type(p2))
        
        
        p1 = np.array([p1.x, p1.y, p1.z]) if hasattr(p1, 'x') else np.array(p1)
        p2 = np.array([p2.x, p2.y, p2.z]) if hasattr(p2, 'x') else np.array(p2)
        return tuple((p1 + p2) / 2)

    @landmark(
        "MIDDLE_SHOULDER",
        connection=[
            PoseLandmark.RIGHT_SHOULDER,
            PoseLandmark.LEFT_SHOULDER,
            "NECK"
        ],
    )
    def _middle_shoulder(self):
        return self._middle(
            self._landmarks[PoseLandmark.RIGHT_SHOULDER.value],
            self._landmarks[PoseLandmark.LEFT_SHOULDER.value],
        )

    @landmark(
        "NECK",
        connection=["MIDDLE_SHOULDER", PoseLandmark.NOSE],
    )
    def _neck(self):
        return self._middle(
            self._landmarks[PoseLandmark.NOSE.value],
            self.MIDDLE_SHOULDER # usa diretamente o ponto como (x, y, z)
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

    # Acessa o ponto virtual NECK usando .value
    # neck_index = landmarks.NECK.value
    # neck_coords = landmarks[neck_index]

    # print(
    #     f"NECK (index {neck_index}): x={neck_coords.x:.3f}, y={neck_coords.y:.3f}, z={neck_coords.z:.3f}"
    # )

    cc = CustomConnections(landmarks)
    print(cc.CUSTOM_CONNECTION)

    mp_drawing = mp.solutions.drawing_utils

    img_copy = image.copy()
    mp_drawing.draw_landmarks(
        image=img_copy,
        landmark_list=landmarks,  # results.pose_landmarks,
        connections=CustomConnections(
            landmarks
        ).ALL_CONNECTIONS,  # mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=get_extended_pose_landmarks_style(),
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

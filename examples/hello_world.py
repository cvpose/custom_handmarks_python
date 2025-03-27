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


# === Create Custom Landmark class ===

def HelloWorld(CustomLandmark):
    
    def _middle(self, p1, p2):
        p1 = np.ndarray([p1.x, p1.y, p1.z])
        p2 = np.ndarray([p2.x, p2.y, p2.z])
        
        return tuple((p1 + p2) / 2)
    
    @landmark("MIDDLE_SHOULDER")
    def _middle_shoulder(self):
        return self._middle(self._middle(
            self._landmarks[self._plm.LEFT_HIP.value],
            self._landmarks[self._plm.LEFT_SHOULDER.value],
        ))

    @landmark("NECK")
    def _neck(self):
        return self._middle(
            self._landmarks[self._plm.NOSE.value], tuple(self.MIDDLE_SHOULDER)
        )
        

# === Inicializa o modelo do MediaPipe Pose ===
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=False
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
    landmarks = DefaultCustomLandmark(results.pose_landmarks.landmark)

    # Acessa o ponto virtual NECK usando .value
    neck_index = landmarks.NECK.value
    neck_coords = landmarks[neck_index]

    print(f"NECK (index {neck_index}): x={neck_coords.x:.3f}, y={neck_coords.y:.3f}, z={neck_coords.z:.3f}")
else:
    print("No landmarks detected in the image.")

# === Libera recursos ===
pose.close()
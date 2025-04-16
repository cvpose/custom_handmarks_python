# Copyright 2024 cvpose
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ==========================
# IMPORTS
# ==========================

import os
import cv2
import numpy as np
import mediapipe as mp

from virtual_landmark import VirtualLandmark, landmark, calculus as calc
from virtual_landmark import (
    Connections,
    get_extended_pose_landmarks_style,
)

# Shortcut to MediaPipe enum
PoseLandmark = mp.solutions.pose.PoseLandmark

# ==========================
# CUSTOM LANDMARK CLASS
# ==========================

class HelloWorld(VirtualLandmark):
    @landmark(
        "MIDDLE_SHOULDER",
        connection=["RIGHT_SHOULDER", "LEFT_SHOULDER", "NECK"],
    )
    def _middle_shoulder(self):
        return calc.middle(
            self[self.virtual_landmark.RIGHT_SHOULDER],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

    @landmark(
        "NECK",
        connection=["MIDDLE_SHOULDER", "NOSE"],
    )
    def _neck(self):
        return calc.middle(
            self[self.virtual_landmark.NOSE],
            self[self.virtual_landmark.MIDDLE_SHOULDER],
        )

    @landmark("PROJECTION")
    def _norm(self):
        return calc.projection(
            self[self.virtual_landmark.LEFT_HIP],
            self[self.virtual_landmark.LEFT_KNEE],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

# ==========================
# MAIN EXECUTION
# ==========================

def main():
    # Initialize MediaPipe pose model
    with mp.solutions.pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=False
    ) as pose:

        # Load image
        image_name = 'image-2.jpeg'
        image_path = os.path.join(os.getcwd(), "examples", "images", image_name)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Run pose estimation
        results = pose.process(image_rgb)

        if not results.pose_landmarks:
            print("No landmarks detected in the image.")
            return

        # Build custom landmark object
        landmarks = HelloWorld(results.pose_landmarks.landmark)

        # Generate drawing configuration
        mp_drawing = mp.solutions.drawing_utils
        extended_style = get_extended_pose_landmarks_style(landmarks)
        connections = Connections(landmarks)

        # Draw results on image
        img_copy = image.copy()
        mp_drawing.draw_landmarks(
            image=img_copy,
            landmark_list=landmarks.as_landmark_list(),
            connections=connections.ALL_CONNECTIONS,
            landmark_drawing_spec=extended_style,
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 255, 255), thickness=1
            ),
        )

        # Display result
        cv2.imshow("Extended Landmarks", img_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
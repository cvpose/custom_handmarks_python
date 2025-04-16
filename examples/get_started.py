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

# =======================
# IMPORTS
# =======================

import os
import cv2
import mediapipe as mp

from virtual_landmark import (
    VirtualLandmark,
    landmark,
    calculus as calc,
    Connections,
)

# =======================
# VIRTUAL LANDMARK CLASS
# =======================

class HelloWorld(VirtualLandmark):
    @landmark("MIDDLE_SHOULDER", connection=["RIGHT_SHOULDER", "LEFT_SHOULDER", "NECK"])
    def _middle_shoulder(self):
        # Calculates the center between the two shoulders
        return calc.middle(
            self[self.virtual_landmark.RIGHT_SHOULDER],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

    @landmark("NECK", connection=["MIDDLE_SHOULDER", "NOSE"])
    def _neck(self):
        # Calculates the midpoint between the nose and shoulder center
        return calc.middle(
            self[self.virtual_landmark.NOSE],
            self[self.virtual_landmark.MIDDLE_SHOULDER],
        )

    @landmark("PROJECTION")
    def _projection(self):
        # Projects the shoulder point onto the line from hip to knee
        return calc.projection(
            self[self.virtual_landmark.LEFT_HIP],
            self[self.virtual_landmark.LEFT_KNEE],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

# =======================
# MAIN EXECUTION
# =======================

def main():
    # Initialize MediaPipe Pose model
    with mp.solutions.pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=False,
    ) as pose:

        # Load the input image
        image_path = os.path.join(os.getcwd(), "examples", "images", "image-1.jpeg")
        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(f"Image not found at: {image_path}")

        # Convert image to RGB format
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Run pose estimation
        results = pose.process(image_rgb)

        if not results.pose_landmarks:
            print("No landmarks detected in the image.")
            return

        # Process virtual landmarks
        vl = HelloWorld(results.pose_landmarks.landmark)
        vpl = vl.virtual_landmark
        connections = Connections(vl)

        # Print useful debugging or summary info
        print("\n\n", f"{'='*5} Landmarks processed successfully {'='*5}")
        print("\nCustom landmarks:\n", list(vpl.keys()))
        print("\nCustom connections:\n", connections.ALL_CONNECTIONS)


if __name__ == "__main__":
    main()
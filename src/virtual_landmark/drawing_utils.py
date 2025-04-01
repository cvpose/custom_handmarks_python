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

import mediapipe as mp
from typing import List, Tuple
import matplotlib.pyplot as plt
from mediapipe.python.solutions.drawing_styles import get_default_pose_landmarks_style

from .virtual_landmark import VirtualLandmark

class Connections:
    def __init__(self, landmarks: VirtualLandmark):
        connections = getattr(landmarks, '_connections')
        vl = landmarks.virtual_landmark
        
        self._connections = [(vl[x1], vl[x2]) for x1, x2 in connections]
        
    @property
    def CUSTOM_CONNECTION(self):
        return list(self._connections)
    
    
    @property
    def POSE_CONNECTIONS(self):
        """
        Returns the original MediaPipe pose connections.

        These are the predefined anatomical connections used by MediaPipe
        to link standard pose landmarks (e.g., shoulder to elbow, hip to knee, etc.).

        Returns:
            List[Tuple[int, int]]: List of index pairs from MediaPipe's POSE_CONNECTIONS.
        """
        return list(mp.solutions.pose.POSE_CONNECTIONS)

    @property
    def ALL_CONNECTIONS(self):
        """
        Returns the combined list of all landmark connections.

        This includes both the original MediaPipe pose connections and the
        custom virtual connections defined via @landmark(..., connection=[...]).

        Returns:
            List[Tuple[int, int]]: Combined list of MediaPipe and custom landmark connections.
        """
        return  self.POSE_CONNECTIONS + self.CUSTOM_CONNECTION



def get_extended_pose_landmarks_style(landmarks):
    """
    Returns a landmark drawing style dictionary with:
    - Default MediaPipe styles for real landmarks (0–32)
    - Custom color-coded styles for dynamically added landmarks:
        - Orange for left-side points
        - Green for right-side points
        - Gray for center/virtual points

    Args:
        landmarks (CustomLandmark): An instance of a CustomLandmark or DefaultCustomLandmark

    Returns:
        Dict[int, DrawingSpec]: Drawing styles for each landmark index
    """
    plm = mp.solutions.pose.PoseLandmark
    base_style = get_default_pose_landmarks_style()

    # Base reference styles (copied, not tupled)
    left_style = base_style[plm.LEFT_SHOULDER.value]
    right_style = base_style[plm.RIGHT_SHOULDER.value]
    center_style = base_style[plm.NOSE.value]

    # Only style custom landmarks (index >= 33)
    for idx in range(len(plm), len(landmarks)):
        point = landmarks[idx]
        x = point.x

        style = next(
            s
            for cond, s in [
                (x < 0.45, right_style),
                (x > 0.55, left_style),
                (True, center_style),
            ]
            if cond
        )

        base_style[idx] = style

    return base_style

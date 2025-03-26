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

from custom_landmarks.default_custom_landmark import DefaultCustomLandmark

class CustomConnections:
    """
    Provides access to default MediaPipe pose connections and extended custom connections.
    """

    # Type alias for readability
    Connection = Tuple[int, int]

    # Default MediaPipe pose connections
    POSE_CONNECTIONS: List[Connection] = list(mp.solutions.pose.POSE_CONNECTIONS)

    # Custom virtual connections (must match indices used in CustomLandmarkItem)
    VIRTUAL_CONNECTIONS: List[Connection] = [
        # Spine and upper trunk
        (
            DefaultCustomLandmark.MIDDLE_HIP.value,
            DefaultCustomLandmark.MIDDLE_SHOULDER.value,
        ),  # MIDDLE_HIP → MIDDLE_SHOULDER
        (
            DefaultCustomLandmark.MIDDLE_SHOULDER.value,
            DefaultCustomLandmark.NECK.value,
        ),  # MIDDLE_SHOULDER → NECK
        (
            DefaultCustomLandmark.LEFT_RIB.value,
            DefaultCustomLandmark.THORAX.value,
        ),  # LEFT_RIB → THORAX
        (
            DefaultCustomLandmark.THORAX.value,
            DefaultCustomLandmark.RIGHT_RIB.value,
        ),  # THORAX → RIGHT_RIB
    ]

    # Combination of all connections
    ALL_CONNECTIONS: List[Connection] = POSE_CONNECTIONS + VIRTUAL_CONNECTIONS


def get_extended_pose_landmarks_style():
    """
    Returns a landmark drawing style dict with default MediaPipe styles for real landmarks
    and custom color-coded styles for virtual landmarks:
        - Orange for left-side points
        - Green for right-side points
        - Gray for center/virtual points
    """
    plm = mp.solutions.pose.PoseLandmark

    # Get base MediaPipe styles (0–32)
    base_style = get_default_pose_landmarks_style()

    side_colors = {
        "LEFT": base_style[plm.LEFT_SHOULDER.value],
        "RIGHT": base_style[plm.RIGHT_SHOULDER.value],
    }

    center_style = base_style[plm.NOSE.value]

    # Loop through virtual landmarks (starting from index 33)
    for item in CustomLandmarkItem:
        idx = item.value
        name = item.name.upper()

        style = next((s for k, s in side_colors.items() if k in name), center_style)

        base_style[idx] = style

    return base_style
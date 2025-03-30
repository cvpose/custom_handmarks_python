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
import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark
from typing import Tuple


def middle(p1: NormalizedLandmark, p2: NormalizedLandmark) -> Tuple[float, float, float]:
    """
    Calculates the midpoint between two landmarks.

    Args:
        p1 (NormalizedLandmark): First landmark.
        p2 (NormalizedLandmark): Second landmark.

    Returns:
        tuple: The midpoint as (x, y, z).
    """
    a = np.array([p1.x, p1.y, p1.z])
    b = np.array([p2.x, p2.y, p2.z])
    return tuple((a + b) / 2)


def project_point_on_line(p1: NormalizedLandmark, p2: NormalizedLandmark, target: NormalizedLandmark) -> Tuple[float, float, float]:
    """
    Projects a point onto a line defined by two other points.

    Args:
        p1 (NormalizedLandmark): First point on the line.
        p2 (NormalizedLandmark): Second point on the line.
        target (NormalizedLandmark): The point to be projected.

    Returns:
        tuple: Projected point on the line (x, y, z).
    """
    a = np.array([p1.x, p1.y, p1.z])
    b = np.array([p2.x, p2.y, p2.z])
    p = np.array([target.x, target.y, target.z])

    ab = b - a
    ap = p - a

    t = np.dot(ap, ab) / np.dot(ab, ab)
    projection = a + t * ab
    return tuple(projection)
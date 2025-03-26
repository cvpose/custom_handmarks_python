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

from custom_landmarks.abstract_custom_landmark import AbstractCustomLandmark
from custom_landmarks.custom_landmark_base import CustomLandmarkBase


class CustomLandmark(AbstractCustomLandmark, CustomLandmarkBase):
    """
    Implementation base class for custom landmark systems.

    This class combines the landmark management capabilities from
    `AbstractCustomLandmark` with the dynamic point registration from
    `CustomLandmarkBase`. It scans all methods decorated with @point("NAME")
    and registers their results as virtual landmarks.

    The resulting object supports access to landmarks via:
    - `self.LANDMARK_NAME` → returns LandmarkRef with (x, y, z)
    - `self.LANDMARK_NAME.value` → index in the landmark list
    """

    def __init__(self, landmarks):
        """
        Initializes the custom landmark object.

        Args:
            landmarks (List[NormalizedLandmark]):
                List of MediaPipe landmarks to be wrapped and extended.
        """
        super().__init__(landmarks)
        self._custom_points = {}         # Dict[str, Tuple[x, y, z]]
        self._custom_points_index = {}   # Dict[str, int]
        self._register_custom_points()

    def _register_custom_points(self):
        """
        Scans the current class for methods decorated with @point("NAME"),
        calls each method to compute the landmark, adds it to the internal list,
        and registers its index.

        This method must be called after initialization to populate
        `_custom_points` and `_custom_points_index`.
        """
        for attr_name in dir(self):
            method = getattr(self, attr_name)
            if callable(method) and getattr(method, "_is_custom_landmark", False):
                name = method._landmark_name
                point = method()
                index = self._add_landmark(point)
                self._custom_points[name] = point
                self._custom_points_index[name] = index
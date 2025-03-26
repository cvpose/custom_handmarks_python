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

class LandmarkRef:
    """
    Wrapper class for a custom landmark point.

    This class allows access to both the 3D point (x, y, z) and its corresponding
    index in the landmark list using a `.value` property. It behaves like a tuple,
    supporting iteration and indexing, and is intended to replicate the behavior of
    MediaPipe landmarks like `PoseLandmark.LEFT_SHOULDER.value`.

    Attributes:
        value (int): The index of the point in the final landmark list.
    """

    def __init__(self, get_point, get_index):
        """
        Initializes the LandmarkRef.

        Args:
            get_point (Callable[[], Tuple[float, float, float]]): Function to retrieve the landmark point (x, y, z).
            get_index (Callable[[], int]): Function to retrieve the index of the point.
        """
        self._get_point = get_point
        self._get_index = get_index

    @property
    def value(self):
        """
        Returns the index of the landmark in the full landmark list.

        Returns:
            int: Index of the point.
        """
        return self._get_index()

    def __iter__(self):
        """
        Allows unpacking or iteration over the point (x, y, z).

        Returns:
            Iterator[float]: Iterator over x, y, z.
        """
        return iter(self._get_point())

    def __getitem__(self, index):
        """
        Enables tuple-style access to the point.

        Args:
            index (int): Index of coordinate (0 = x, 1 = y, 2 = z).

        Returns:
            float: Coordinate value at given index.
        """
        return self._get_point()[index]

    def __repr__(self):
        """
        String representation of the landmark point.

        Returns:
            str: String like "(x, y, z)".
        """
        return repr(self._get_point())
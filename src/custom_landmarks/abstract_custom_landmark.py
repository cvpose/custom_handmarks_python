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

import abc
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2


class AbstractCustomLandmark(abc.ABC):
    """
    Abstract class that encapsulates MediaPipe pose landmarks and allows
    adding virtual (custom) landmarks while maintaining compatibility with 
    MediaPipe's landmark list structure.

    This class supports iteration, indexing, and conversion to MediaPipe's
    `NormalizedLandmarkList`. It is designed to be extended by subclasses
    that compute and register additional landmarks dynamically.

    Attributes:
        _plm (PoseLandmark): Shortcut to MediaPipe's PoseLandmark enum.
        _landmarks (List[NormalizedLandmark]): Original list of landmarks.
        landmark_list (NormalizedLandmarkList): Combined list of original and added landmarks.
    """

    def __init__(self, landmarks):
        """
        Initializes the class with a copy of the original MediaPipe landmarks.

        Args:
            landmarks (List[NormalizedLandmark]): List of landmarks from MediaPipe's pose estimation.
        """
        self._plm = mp.solutions.pose.PoseLandmark
        self._landmarks = landmarks
        self.landmark_list = landmark_pb2.NormalizedLandmarkList()
        self.landmark_list.landmark.extend(landmarks)

    def _add_landmark(self, point):
        """
        Adds a new virtual landmark to the landmark list.

        Args:
            point (Union[tuple, list, np.ndarray]): A normalized 3D point (x, y, z), 
                where each value is typically between 0 and 1.

        Returns:
            int: Index of the newly added landmark in the full landmark list.

        Raises:
            ValueError: If the input point is not a 3D coordinate.
        """
        if not isinstance(point, (list, tuple, np.ndarray)) or len(point) < 3:
            raise ValueError("point must be a 3D tuple/list/np.ndarray")

        lm = landmark_pb2.NormalizedLandmark()
        lm.x, lm.y, lm.z = float(point[0]), float(point[1]), float(point[2])
        lm.visibility = 1.0
        self.landmark_list.landmark.append(lm)

        return len(self.landmark_list.landmark) - 1

    def as_landmark_list(self):
        """
        Returns the complete landmark list in the MediaPipe format.

        Returns:
            NormalizedLandmarkList: Combined list of original and custom landmarks.
        """
        return self.landmark_list

    def __getitem__(self, idx):
        """
        Access a landmark by index.

        Args:
            idx (int): Index of the landmark.

        Returns:
            NormalizedLandmark: Landmark at the given index.
        """
        return self.landmark_list.landmark[idx]

    def __len__(self):
        """
        Returns the total number of landmarks.

        Returns:
            int: Count of all landmarks (original + custom).
        """
        return len(self.landmark_list.landmark)

    def __iter__(self):
        """
        Iterates over the complete landmark list.

        Returns:
            Iterator[NormalizedLandmark]: An iterator over all landmarks.
        """
        return iter(self.landmark_list.landmark)

    # def __getattr__(self, name):
    #     """
    #     Fallback attribute access to delegate to the internal landmark list.
    #     Only called if the attribute wasn't found by normal lookup.

    #     Args:
    #         name (str): Attribute name.

    #     Returns:
    #         Any: Attribute from the internal `landmark_list`.

    #     Raises:
    #         AttributeError: If the attribute does not exist.
    #     """
    #     # Evita chamada recursiva se o atributo não estiver definido
    #     if name in self.__dict__:
    #         return self.__dict__[name]
    #     cls_attr = getattr(type(self), name, None)
    #     if cls_attr is not None:
    #         return cls_attr.__get__(self, type(self))  # Suporte a @property
    #     try:
    #         return getattr(self.landmark_list, name)
    #     except AttributeError:
    #         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

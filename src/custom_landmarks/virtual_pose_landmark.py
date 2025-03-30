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

PoseLandmark = mp.solutions.pose.PoseLandmark

class VirtualPoseLandmark(dict):
    """
    Simulates an enum that contains all MediaPipe landmarks and dynamically added custom ones.
    Allows both name-based and index-based access.

    Example:
        vpm = VirtualPoseLandmark()
        vpm["NECK"]  # -> 33
        vpm.NECK     # -> 33
        vpm[33]      # -> "NECK"
    """

    def __init__(self):
        super().__init__()
        self._reverse = {}  # index -> name
        self._load_builtin_landmarks()

        # Also make them available as attributes
        for name in self:
            setattr(self, name, self[name])

    def _load_builtin_landmarks(self):
        """
        Loads the built-in MediaPipe PoseLandmark values into the enum simulation.
        """
        for landmark in PoseLandmark:
            self[landmark.name] = landmark.value
            self._reverse[landmark.value] = landmark.name

    def add(self, name: str, index: int):
        """
        Adds a new virtual landmark to the map.

        Args:
            name (str): Name of the landmark (must be a valid identifier).
            index (int): Index to associate with the landmark.
        """
        if not isinstance(name, str) or not name.isidentifier():
            raise ValueError("Custom landmark name must be a valid identifier string.")
        if name in self:
            raise ValueError(f"Landmark '{name}' is already defined.")
        if index in self._reverse:
            raise ValueError(f"Index {index} is already used by landmark '{self._reverse[index]}'.")

        self[name] = index
        self._reverse[index] = name
        setattr(self, name, index)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._reverse[key]
        return super().__getitem__(key)

    def __contains__(self, item):
        if isinstance(item, int):
            return item in self._reverse
        return super().__contains__(item)

    def __repr__(self):
        return f"<VirtualPoseLandmark {dict(self)}>"

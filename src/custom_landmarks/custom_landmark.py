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
from custom_landmarks.virtual_landmark import VirtualLandmark


class CustomLandmark(AbstractCustomLandmark):
    """
    Implementation base class for custom landmark systems.

    This class combines the landmark management capabilities from
    `AbstractCustomLandmark` with dynamic point registration. It scans all
    methods decorated with @landmark("NAME") and registers their results
    as virtual landmarks. Optional connections can also be declared between
    landmarks.

    The resulting object supports access to landmarks via:
    - `self.LANDMARK_NAME.value` → index in the landmark list
    - `self[self.LANDMARK_NAME.value]` → landmark data (NormalizedLandmark)
    - `self.virtual_connections` → list of tuple(index, index)
    - `self.themes[name]` → "left", "right" or "center" based on x-position
    """

    def __init__(self, landmarks):
        super().__init__(landmarks)
        self._custom_points = {}
        self._custom_points_index = {}
        self._themes = {}
        self._pending_connections = set()
        self._connections = set()
        self._deferred_landmark_methods = []

        self._collect_landmark_methods()
        self._compute_landmark_points()
        self._validate_and_finalize_connections()

    def _collect_landmark_methods(self):
        for attr_name in dir(self):
            try:
                method = getattr(self, attr_name)
            except AttributeError:
                continue
            if callable(method) and getattr(method, "_is_custom_landmark", False):
                self._deferred_landmark_methods.append(method)

    def _compute_landmark_points(self):
        for method in self._deferred_landmark_methods:
            name = method._landmark_name
            point = method()
            index = len(self.landmark_list.landmark)

            # Cria um VirtualLandmark e adiciona à lista
            virtual = VirtualLandmark(x=point[0], y=point[1], z=point[2], index=index)
            # self.landmark_list.landmark.append(virtual)
            self.landmark_list.landmark.append(virtual.to_protobuf())

            # Armazena referências
            self._custom_points[name] = virtual
            self._custom_points_index[name] = index
            setattr(self, name, virtual)

            # Atribui tema automaticamente com base em x
            x = point[0]
            if x < 0.45:
                theme = "left"
            elif x > 0.55:
                theme = "right"
            else:
                theme = "center"
            self._themes[name] = theme

            # Coleta conexões pendentes para validação posterior
            for target_name in method._landmark_connections:
                connection = tuple(sorted([name, target_name]))
                self._pending_connections.add(connection)

    def _validate_and_finalize_connections(self):
        defined_names = set(self._custom_points_index.keys()) | set(self._plm.__members__.keys())
        missing = {
            a if a not in defined_names else b
            for a, b in self._pending_connections
            if a not in defined_names or b not in defined_names
        }
        if missing:
            raise ValueError(f"Connection refers to undefined landmark(s): {sorted(missing)}")
        self._connections = self._pending_connections

    def get_custom_connections(self):
        return [
            (getattr(self, a).value, getattr(self, b).value)
            for a, b in self._connections
        ]
        
    def __getattr__(self, name):
        return getattr(self.landmark_list, name)
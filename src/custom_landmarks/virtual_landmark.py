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

from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmark


class VirtualLandmark:
    """
    Wrapper para NormalizedLandmark com suporte a .value (índice) e acesso direto a x, y, z.

    Esse objeto funciona como um landmark normal (x, y, z, visibility),
    mas adiciona o atributo `.value` para uso como enum dinâmico.
    """

    def __init__(self, x: float, y: float, z: float, index: int):
        self._landmark = NormalizedLandmark(x=x, y=y, z=z, visibility=1.0)
        self.value = index

    @property
    def x(self): return self._landmark.x
    @property
    def y(self): return self._landmark.y
    @property
    def z(self): return self._landmark.z
    @property
    def visibility(self): return self._landmark.visibility

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]

    def __repr__(self):
        return f"<VirtualLandmark value={self.value}, x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f}>"

    def to_protobuf(self):
        """Retorna a instância real de NormalizedLandmark."""
        return self._landmark
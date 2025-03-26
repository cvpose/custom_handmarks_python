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

from custom_landmarks.custom_landmark import CustomLandmark
from custom_landmarks.decorator import point


class DefaultCustomLandmark(CustomLandmark):
    @point("LEFT_RIB")
    def l_rib(self):
        return self._middle(
            self._landmarks[self._plm.LEFT_HIP.value],
            self._landmarks[self._plm.LEFT_SHOULDER.value],
        )

    @point("RIGHT_RIB")
    def r_rib(self):
        return self._middle(
            self._landmarks[self._plm.RIGHT_HIP.value],
            self._landmarks[self._plm.RIGHT_SHOULDER.value],
        )

    @point("MIDDLE_HIP")
    def m_hip(self):
        return self._middle(
            self._landmarks[self._plm.LEFT_HIP.value],
            self._landmarks[self._plm.RIGHT_HIP.value],
        )

    @point("MIDDLE_SHOULDER")
    def m_shoulder(self):
        return self._middle(
            self._landmarks[self._plm.LEFT_SHOULDER.value],
            self._landmarks[self._plm.RIGHT_SHOULDER.value],
        )

    @point("NECK")
    def neck(self):
        return self._middle(
            self._landmarks[self._plm.NOSE.value], tuple(self.MIDDLE_SHOULDER)
        )

    @point("THORAX")
    def thorax(self):
        return self._middle(self.MIDDLE_HIP, self.MIDDLE_SHOULDER)

    def _middle(self, p1, p2):
        def to_array(p):
            if hasattr(p, "x"):
                return np.array([p.x, p.y, p.z])
            elif isinstance(p, (tuple, list, np.ndarray)):
                return np.array(p)
            else:
                return np.array(list(p))  # fallback: LandmarkRef (iterable)

        p1 = to_array(p1)
        p2 = to_array(p2)
        return tuple((p1 + p2) / 2)

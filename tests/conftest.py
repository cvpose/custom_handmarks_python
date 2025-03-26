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
import os
import sys
import pytest
from unittest.mock import MagicMock
from mediapipe.framework.formats import landmark_pb2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

@pytest.fixture
def fake_landmark():
    def _lm(x, y, z):
        lm = landmark_pb2.NormalizedLandmark()
        lm.x = x
        lm.y = y
        lm.z = z
        lm.visibility = 1.0
        return lm
    return _lm

@pytest.fixture
def fake_landmarks(fake_landmark):
    return [fake_landmark(x/10, x/10, x/10) for x in range(33)]

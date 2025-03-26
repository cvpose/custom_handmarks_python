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


class DummyLandmark(AbstractCustomLandmark):
    pass


def test_add_landmark(fake_landmarks):
    obj = DummyLandmark(fake_landmarks)
    idx = obj._add_landmark((0.5, 0.5, 0.5))
    assert isinstance(obj[idx], type(obj.landmark_list.landmark[0]))
    assert idx == len(fake_landmarks)

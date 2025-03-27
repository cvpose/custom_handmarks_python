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
import pytest
from mediapipe.framework.formats import landmark_pb2
from custom_landmarks.abstract_custom_landmark import AbstractCustomLandmark


class DummyLandmark(AbstractCustomLandmark):
    pass


def test_add_landmark(fake_landmarks):
    obj = DummyLandmark(fake_landmarks)
    idx = obj._add_landmark((0.5, 0.5, 0.5))
    assert isinstance(obj[idx], type(obj.landmark_list.landmark[0]))
    assert idx == len(fake_landmarks)


def test_as_landmark_list(fake_landmarks):
    obj = DummyLandmark(fake_landmarks)
    landmark_list = obj.as_landmark_list()

    assert isinstance(landmark_list, landmark_pb2.NormalizedLandmarkList)
    assert len(landmark_list.landmark) == 33

    # Confirma se os valores batem com os originais
    for i, lm in enumerate(fake_landmarks):
        assert landmark_list.landmark[i].x == lm.x
        assert landmark_list.landmark[i].y == lm.y
        assert landmark_list.landmark[i].z == lm.z

def test___iter__(fake_landmarks):
    obj = DummyLandmark(fake_landmarks)
    iterated = list(iter(obj))
    assert len(iterated) == len(fake_landmarks)
    for orig, from_iter in zip(fake_landmarks, iterated):
        assert from_iter.x == orig.x
        assert from_iter.y == orig.y
        assert from_iter.z == orig.z

def test___getattr__(fake_landmarks):
    obj = DummyLandmark(fake_landmarks)
    result = obj.landmark

    # Confirma que é uma coleção indexável e iterável
    assert hasattr(obj, '__getitem__')
    assert hasattr(obj, '__iter__')

@pytest.mark.parametrize("invalid_point", [
    None,
    42,
    "invalid",
    [0.1],             # too short
    [0.1, 0.2],        # still too short
    {"x": 0.1, "y": 0.2, "z": 0.3},  # not a list/tuple/ndarray
])
def test_add_landmark_invalid_input_raises(fake_landmarks, invalid_point):
    obj = DummyLandmark(fake_landmarks)
    with pytest.raises(ValueError, match="point must be a 3D tuple/list/np.ndarray"):
        obj._add_landmark(invalid_point)
        
def test_len_returns_total_landmarks(fake_landmarks):
    obj = DummyLandmark(fake_landmarks)
    assert len(obj) == 33  # Apenas os landmarks originais
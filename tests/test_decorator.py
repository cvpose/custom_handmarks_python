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
from custom_landmarks.decorator import landmark

def test_point_decorator_adds_metadata():
    @landmark("MY_POINT")
    def calc():
        return (0.5, 0.5, 0.0)

    assert hasattr(calc, "_is_custom_landmark")
    assert hasattr(calc, "_landmark_name")
    assert calc._landmark_name == "MY_POINT"
    
@pytest.mark.parametrize("invalid_name", [
    None,
    123,
    "123invalid",
    "with space",
    "special-char!",
    "",
])
def test_point_decorator_invalid_name_raises(invalid_name):
    with pytest.raises(ValueError, match="Landmark name must be a valid identifier string."):
        @landmark(invalid_name)
        def fake_fn():
            pass
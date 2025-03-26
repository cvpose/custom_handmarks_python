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

from .landmark_ref import LandmarkRef


class CustomLandmarkBase:
    """
    Base class that dynamically registers custom landmarks defined with @point decorators.

    When a subclass is created, this class inspects all methods decorated with @point("NAME")
    and registers them as properties that return `LandmarkRef` objects. Each `LandmarkRef`
    allows access to both the 3D coordinates and the index (`.value`) in the landmark list.

    The actual computation and registration of landmark values must be handled by the subclass
    (typically in a method like `_register_custom_points()`).

    Usage:
        class MyCustomLandmark(CustomLandmarkBase):
            @point("MY_POINT")
            def my_point(self):
                return (x, y, z)

        obj.MY_POINT          # → (x, y, z)
        obj.MY_POINT.value    # → index in landmark list
    """

    def __init_subclass__(cls, **kwargs):
        """
        Automatically registers properties for each method decorated with @point("NAME").
        Each property returns a `LandmarkRef`, allowing access to the computed 3D point and its index.
        """
        super().__init_subclass__(**kwargs)

        # Create a copy of the class dictionary to avoid mutation during iteration
        for attr_name, attr in list(vars(cls).items()):
            if callable(attr) and getattr(attr, "_is_custom_landmark", False):
                name = attr._landmark_name

                # Define a property that returns a LandmarkRef with dynamic access
                def make_property(key):
                    return property(lambda self: LandmarkRef(
                        lambda: self._custom_points[key],
                        lambda: self._custom_points_index[key]
                    ))

                # Register the property dynamically with the name provided in the decorator
                setattr(cls, name, make_property(name))
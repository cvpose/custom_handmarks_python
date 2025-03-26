def point(name: str):
    """
    Decorator to register a method as a virtual landmark generator.

    When applied to a method, this decorator marks it as a custom landmark
    associated with the given name. During class initialization, all methods
    decorated with @point(...) will be automatically executed, and their
    results will be added to the landmark list.

    The generated landmark will also be accessible via:
        - `instance.NAME` → returns LandmarkRef with (x, y, z)
        - `instance.NAME.value` → index in the landmark list

    Args:
        name (str): Unique name/key to associate with the custom landmark.

    Returns:
        Callable: The original function, tagged with metadata for discovery.

    Example:
        @point("NECK")
        def calc_neck(self):
            return self._middle(
                self._landmarks[self._plm.LEFT_SHOULDER.value],
                self._landmarks[self._plm.RIGHT_SHOULDER.value]
            )
    """
    if not isinstance(name, str) or not name.isidentifier():
        raise ValueError("Landmark name must be a valid identifier string.")

    def wrapper(fn):
        fn._is_custom_landmark = True
        fn._landmark_name = name
        return fn

    return wrapper

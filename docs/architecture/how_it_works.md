---
title: How It Works
nav_order: 1
parent: Architecture
---

# How It Works

The virtual landmark system is composed of three well-defined phases, enabling the creation, discovery, and usage of custom landmarks in conjunction with MediaPipe. This modular architecture provides flexibility for researchers and developers working with pose estimation, while maintaining full compatibility with MediaPipe’s tools and rendering.

---

## 1. Definition Phase

In this initial phase, developers define virtual landmarks by implementing methods within a custom class that inherits from `VirtualLandmark`. Each method must be decorated with `@landmark`, and should return a new 3D point calculated from one or more existing landmarks.

This phase is where you define *how* new landmarks should be computed based on geometric logic such as midpoints, offsets, or projected vectors.

### Example

```python
from virtual_landmark import VirtualLandmark, landmark
import virtual_landmark.calculus as calc

class CustomLandmarks(VirtualLandmark):

    @landmark("NECK", connection=["LEFT_SHOULDER", "RIGHT_SHOULDER"])
    def _neck(self):
        return calc.middle(self.LEFT_SHOULDER, self.RIGHT_SHOULDER)

    @landmark("THORAX", connection=["NECK", "MIDDLE_HIP"])
    def _thorax(self):
        return calc.middle(self.NECK, self.MIDDLE_HIP)
```

This example defines a class `CustomLandmarks` that extends `VirtualLandmark`. It uses `@landmark` to annotate methods that describe how to compute the virtual point. The `connection` argument defines edges between landmarks, used later for visualization.

To use this system, simply create an instance by passing existing landmarks (e.g., from MediaPipe):

```python
custom = CustomLandmarks(mp_pose_landmarks)
```

---

## 2. Discovery Phase

Once the custom class is instantiated, the system automatically begins the discovery process using Python’s reflection capabilities. During this phase, the system:

1. **Scans the class for methods decorated with `@landmark`.**
   - These are identified through attributes injected by the decorator.

2. **Executes each decorated method.**
   - Methods are passed access to the existing landmarks (e.g., `self.LEFT_SHOULDER`) and must return a valid 3D point (typically a NumPy array).

3. **Appends the computed point to the internal list.**
   - Each new point is automatically assigned a unique index, extending the existing landmark list.

4. **Validates and registers all connections.**
   - Connections declared in the decorator are stored and later merged with MediaPipe’s standard pose edges.

5. **Ensures error handling.**
   - If a referenced landmark has not been defined or is invalid, an error is raised to prevent malformed geometry.

This process occurs within the internal method `_process_virtual_landmarks()`, and ensures that all virtual landmarks are computed in a consistent and predictable order.

---

## 3. Access & Visualization Phase

After discovery and computation, all virtual landmarks are seamlessly integrated into the output. They can be accessed and visualized just like MediaPipe’s built-in landmarks.

### Accessing Landmarks

You can access a virtual landmark in multiple ways:

- **By name:**
  ```python
  custom.NECK  # Returns VirtualPoseLandmark instance
  ```

- **By index (for compatibility with MediaPipe arrays):**
  ```python
  all_landmarks = custom.as_landmark_list()
  all_landmarks[custom.NECK.value]
  ```

These access patterns enable developers to plug the output directly into visualization or inference pipelines.

### Visualization

All connections defined in the decorators are merged with the default `POSE_CONNECTIONS` from MediaPipe:

```python
mp_drawing.draw_landmarks(
    image=img,
    landmark_list=custom.as_landmark_list(),
    connections=custom.custom_connections,
    landmark_drawing_spec=style_points,
    connection_drawing_spec=style_edges,
)
```

The virtual system ensures compatibility with:

- `NormalizedLandmarkList` and MediaPipe APIs
- OpenCV-based rendering
- External pose analysis tools

This design allows you to extend pose data dynamically with minimal friction, while retaining full interoperability with the broader MediaPipe ecosystem.

---

---
title: Create Virtual Landmarks
nav_order: 1
parent: Guide
---
# Create Your Own Virtual Landmarks

This section shows how to define **custom pose points** using the `@landmark` decorator provided by `virtual_landmark_python`.

Virtual landmarks are calculated dynamically at runtime based on geometric operations (e.g. midpoint, projection, bisector). These points are added to the existing MediaPipe pose data and can be used like native landmarks.

---

## Step-by-Step Example

Let's say you want to define a new point called `NECK`, which is the midpoint between the left and right shoulders.

### Create a subclass of `VirtualLandmark`

```python
from virtual_landmark import VirtualLandmark, landmark, calculus as calc

class MyCustomLandmarks(VirtualLandmark):

    @landmark("NECK")
    def _neck(self):
        return calc.middle(
            self[self.virtual_landmark.LEFT_SHOULDER],
            self[self.virtual_landmark.RIGHT_SHOULDER],
        )
```

- The `@landmark("NECK")` decorator registers this method as a virtual landmark.
- The method returns a new point (a `NormalizedLandmark`).

---

## Accessing the Virtual Point

After calling `MyCustomLandmarks` with the original pose landmarks:

```python
landmarks = MyCustomLandmarks(results.pose_landmarks.landmark)

# Access index
idx = landmarks.virtual_landmark.NECK.value

# Get the 3D point
neck_point = landmarks[idx]
```

You can use this point in angle calculations, visualizations, or further geometric derivations.

---

## Common Geometric Helpers

All helper functions live in the `calculus` module:

| Function         | Description                             |
|------------------|-----------------------------------------|
| `middle(p1, p2)` | Midpoint between two points             |
| `projection(p1, p2, target)` | Orthogonal projection of `target` onto line `(p1, p2)` |
| `centroid(*points)` | Center of multiple points            |
| `bisector(p1, pivot, p2)` | Angle bisector from pivot       |
| `extend(p1, p2, factor)` | Extends vector `p1 → p2`         |


Go to [calculus module](calculus.md) to now more about the build in calculators

---

## Tips

- You can define as many virtual landmarks as you want inside a single class.
- Landmark names must be valid Python identifiers (e.g., `LEFT_HIP_LINE`, not `left-hip-line`).
- Connections are optional but recommended for visual feedback.
- All generated landmarks are fully compatible with `MediaPipe`, including drawing and exporting.

---

Ready to define your own? Try it inside your project and plug it into the MediaPipe rendering pipeline!

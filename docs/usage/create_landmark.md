---
title: Create Landmark
nav_order: 2
parent: Usage
---

# Create Landmark

This guide explains how to define your own virtual landmarks using the `@landmark` decorator and geometric utilities from the `calculus` module.

---

## 1. Create a Custom Class

To define virtual landmarks, you must subclass `VirtualLandmark` and annotate methods using `@landmark`.

Each method should return a 3D coordinate (as a NumPy array), calculated using one or more existing landmarks.

### Example: `hello_world.py`

```python
from virtual_landmark import VirtualLandmark, landmark, calculus as calc

class HelloWorld(VirtualLandmark):

    @landmark("MIDDLE_SHOULDER", connection=["RIGHT_SHOULDER", "LEFT_SHOULDER", "NECK"])
    def _middle_shoulder(self):
        return calc.middle(
            self[self.virtual_landmark.RIGHT_SHOULDER],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

    @landmark("NECK", connection=["MIDDLE_SHOULDER", "NOSE"])
    def _neck(self):
        return calc.middle(
            self[self.virtual_landmark.NOSE],
            self[self.virtual_landmark.MIDDLE_SHOULDER],
        )

    @landmark("PROJECTION")
    def _norm(self):
        return calc.projection(
            self[self.virtual_landmark.LEFT_HIP],
            self[self.virtual_landmark.LEFT_KNEE],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )
```

---

## 2. Anatomy of a Virtual Landmark

Below is a breakdown of each key element used to define virtual landmarks:

- **`@landmark(name, connection=[...])`**  
  A decorator that marks the method as a virtual landmark.  
  - The `name` parameter assigns a unique identifier to the virtual point, which becomes accessible via `self.virtual_landmark.NAME`.
  - The optional `connection` parameter defines topological edges to other landmarks. These connections are used for visual rendering and may also assist in graph-based analyses or pose structure tracing.
  - This mechanism enables automatic discovery and processing of custom landmarks without manual registration.

- **`calc.middle(p1, p2)`**  
  A geometric utility function that returns the midpoint between two 3D landmarks.  
  - Frequently used to compute symmetrical anatomical references, such as the center between shoulders or hips.
  - Accepts two 3D NumPy arrays and returns a new point equally spaced between them.

  _Example use case_: Compute `"MIDDLE_SHOULDER"` from `"LEFT_SHOULDER"` and `"RIGHT_SHOULDER"`.  
  [See more functions in the `calculus` module →](./calculus.md)

- **`calc.projection(p1, p2, target)`**  
  Projects the `target` point orthogonally onto the line formed by `p1` and `p2`.  
  - Useful when building landmarks aligned with body axes, such as projecting the shoulder onto the leg’s vertical axis.
  - Helps simulate anatomical references based on alignment rather than physical joints.

  _Mathematically_, this corresponds to a vector projection:
  \[
  	ext{proj}_{v}(u) = p1 + \frac{(u \cdot v)}{(v \cdot v)} \cdot v
  \]

- **`self[self.virtual_landmark.X]`**  
  Retrieves a landmark by name using dynamic indexing.  
  - Works for both MediaPipe’s original landmarks and the virtual ones defined via decorators.
  - Ensures consistency by enabling unified access to all landmarks, regardless of their origin.

  _Example_:  
  ```python
  self[self.virtual_landmark.LEFT_HIP]
  ```
  Returns the 3D coordinates of the `LEFT_HIP` landmark.

---

## 3. Tips for Defining Landmarks

- Always return a NumPy array with shape `(3,)`.
- Use descriptive names like `"MIDDLE_SHOULDER"` or `"NECK"` to improve readability.
- Use the `connection` argument to link virtual landmarks to others for drawing.
- Complex operations can be composed using multiple helper functions from `calculus`.

---

## 4. Next Steps

- To see how this class is used at runtime, continue to the [Run Guide](./run.md).
- For detailed documentation of available geometric functions, check [Calulus Reference](./calculus.md).

---

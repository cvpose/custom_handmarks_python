---
title: Components
nav_order: 3
parent: Architecture
---

# Components

This section provides a detailed overview of the key components in the `virtual_landmark` package. Each module is responsible for a specific concern in the pipeline, from landmark creation to rendering.

---

## 1. `abstract_landmark.py`

**Class:** `AbstractLandmark`

### Purpose
Provides the foundational data structure for managing both original and virtual landmarks. It exposes a clean, iterable interface and supports conversion to MediaPipe-compatible formats.

### Responsibilities
- Stores landmarks with index-based access.
- Adds new landmarks and defines interconnections.
- Converts the internal structure to `NormalizedLandmarkList`.

### Key Methods
- `__getitem__`, `__iter__`, `__len__`
- `_add_landmark(name, point)`
- `_add_connection(name, targets)`
- `as_landmark_list()`

---

## 2. `virtual_landmark.py`

**Class:** `VirtualLandmark`

### Purpose
Concrete subclass of `AbstractLandmark` responsible for discovering and executing all methods decorated with `@landmark`.

### Inherits
- `AbstractLandmark`

### Responsibilities
- Uses Python introspection to locate decorated methods.
- Computes and registers virtual landmarks.
- Builds custom topologies via connection metadata.
- Merges virtual landmarks with existing landmark sets.

### Key Method
- `_process_virtual_landmarks()`

---

## 3. `decorator.py`

**Function:** `@landmark(name, connection=[])`

### Purpose
Decorator that marks a method as a virtual landmark provider, enabling its discovery and execution during the landmark processing phase.

### What It Does
- Attaches `_landmark_name` and `_landmark_connections` metadata to methods.
- Enables automated indexing and connection registration.

### Example
```python
@landmark("NECK", connection=["LEFT_SHOULDER", "RIGHT_SHOULDER"])
def _neck(self):
    return calc.middle(self.LEFT_SHOULDER, self.RIGHT_SHOULDER)
```

---

## 4. `virtual_pose_landmark.py`

**Class:** `VirtualPoseLandmark`

### Purpose
An enum-like registry used to dynamically manage and retrieve landmark indices by name. It supports both programmatic and attribute-style access.

### Responsibilities
- Stores associations between landmark names and their indices.
- Provides flexible access patterns via `.NAME`, `["NAME"]`, or `.NAME.value`.

### Key Methods
- `add(name, index)`
- `__getitem__`, `__getattr__`, `__contains__`

---

## 5. `calculus.py`

**Module:** `calculus`

### Purpose
Provides a set of reusable geometric utilities to calculate custom landmarks. These functions abstract common operations like midpoint, projection, and vector rotation.

### Key Functions
- `middle(p1, p2)`
- `centroid(*points)`
- `projection(p1, p2, target)`
- `extend(p1, p2, factor)`
- `normalize(p1, p2)`
- `rotate(p, axis_p1, axis_p2, angle)`
- ...and others

---

## 6. `drawing_utils/connections.py`

**Class:** `Connections`

### Purpose
Defines and aggregates landmark connections, combining MediaPipe defaults with dynamically registered virtual edges.

### Constants
- `CUSTOM_CONNECTION`
- `POSE_CONNECTIONS`
- `ALL_CONNECTIONS`

---

## 7. `drawing_utils/style.py`

**Class:** `Style`

### Purpose
Defines visual styles for landmarks and connections to be used with MediaPipe’s drawing utilities.

### Key Method
- `get_extended_pose_landmarks_style(landmarks)` — returns a style configuration that supports both native and custom landmarks.

---

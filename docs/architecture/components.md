---
title: Components
nav_order: 1
parent: Architecture
---
## Components

## 1. `abstract_landmark.py`

**Class:** `AbstractLandmark`

### Purpose:
Base class responsible for managing and storing both original and virtual landmarks, providing iterable access and landmark list conversion.

#### Responsibilities:
- Index-based and iterable access to landmarks.
- Addition of virtual landmarks via `_add_landmark`.
- Connection definition support via `_add_connection`.
- Export to `NormalizedLandmarkList`.

### Key Methods:
- `__getitem__`, `__iter__`, `__len__`
- `_add_landmark(name, point)`
- `_add_connection(name, targets)`
- `as_landmark_list()`

---

## 2. `virtual_landmark.py`

**Class:** `VirtualLandmark`

### Purpose:
Concrete implementation that detects and executes all `@landmark`-decorated methods.

### Inherits:
- `AbstractLandmark`

### Responsibilities:
- Scans and processes decorated methods.
- Registers virtual landmarks and their connections dynamically.
- Exposes `virtual_landmark` accessor object for consistent indexing.

### Key Method:
- `_process_virtual_landmarks()`

---

## 3. `decorator.py`

**Function:** `@landmark(name, connection=[])`

### Purpose:
Decorator that registers a method as a virtual landmark generator.

### What it does:
- Tags the method with `_landmark_name` and `_landmark_connections`.
- Enables later introspection by `VirtualLandmark`.

### Example:
```python
@landmark("NECK", connection=["LEFT_SHOULDER", "RIGHT_SHOULDER"])
def _neck(self):
    return calc.middle(self.LEFT_SHOULDER, self.RIGHT_SHOULDER)
```

---

## 4. `virtual_pose_landmark.py`

**Class:** `VirtualPoseLandmark`

### Purpose:
Enum-like interface for accessing all original and custom landmark indices by name.

### Responsibilities:
- `add(name, index)` registers new landmarks.
- Supports access via `.NAME`, `["NAME"]`, and `.NAME.value`.

### Key Methods:
- `__getitem__`, `__getattr__`, `__contains__`, `add()`

---

## 5. `calculus.py`

**Module:** `calculus`

### Purpose:
Contains reusable geometric computations used in virtual landmark generation.

### Functions:
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

### Constants:
- `CUSTOM_CONNECTION`
- `POSE_CONNECTIONS`
- `ALL_CONNECTIONS`

### Purpose:
Combines default MediaPipe and custom connections for use in visualization.

---

## 7. `drawing_utils/style.py`

**Class:** `Style`

### Method:
- `get_extended_pose_landmarks_style(landmarks)`

### Purpose:
Returns drawing styles for default and custom landmarks.

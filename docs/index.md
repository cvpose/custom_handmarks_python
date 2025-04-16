---
title: Home
nav_order: 1
---
# Welcome to virtual_landmark_python

**virtual_landmark_python** is a Python module for extending [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html) with **custom virtual landmarks**. It allows you to define new body points geometrically (e.g., midpoints, projections, bisectors) and integrate them seamlessly into the MediaPipe pipeline.

---

## What This Library Does

- 🧩 Dynamically generate new pose landmarks
- 🔗 Connect virtual points to the original pose structure
- 🧠 Access all landmarks with intuitive names
- 🛠 Integrate with MediaPipe’s rendering and data export
- 🧪 Build pose-based logic using clean and extendable interfaces

---

## Documentation Structure

You’ll find detailed documentation on:

- ✅ [How the system works](./landmark_architecture.md)
- 📐 [How to create your own virtual points](create_virtual_landmarks.md)
- 🔄 [How to register connections](how_to_register_connections.md)
- 📊 [How to access landmarks](how_to_access_landmarks.md)

---

## Quick Start

Install MediaPipe:

```bash
pip install mediapipe
```
Then run your custom virtual landmark logic:

```python
@landmark("NECK", connection=["LEFT_SHOULDER", "RIGHT_SHOULDER"])
def _neck(self):
    return calc.middle(
        self[self.virtual_landmark.LEFT_SHOULDER],
        self[self.virtual_landmark.RIGHT_SHOULDER],
    )
```

---
title: Home
layout: home
nav_order: 1
description: "The virtual landmark definition for Mediapipe Pose"
permalink: /
---
# Virtual Landmark
{: .fs-9 }

Extend [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html) enabling virtual landmarks through geometrically calculated 3D points and their edges
{: .fs-6 .fw-300 }

[Get started now](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub][https://github.com/cvpose/virtual_landmark_python]{: .btn .fs-5 .mb-4 .mb-md-0 }
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

## Getting started

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

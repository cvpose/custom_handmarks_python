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
[View it on GitHub](https://github.com/cvpose/virtual_landmark_python){: .btn .fs-5 .mb-4 .mb-md-0 }

---

The virtual_landmark_python system enables the dynamic generation of new pose landmarks derived from geometric relationships within the human body. These virtual points are seamlessly integrated into the existing MediaPipe pose structure, allowing developers to expand the landmark topology without altering the base model. This integration supports both spatial reasoning and high-level abstraction by embedding custom points—such as midpoints, projections, or anatomical estimates—directly into the landmark list.

In addition to structural expansion, the library provides an intuitive interface for accessing both original and extended landmarks by name, promoting clarity and consistency in code. These landmarks are fully compatible with MediaPipe’s native rendering tools and export workflows, allowing for immediate visualization and deployment. Furthermore, the framework supports the development of modular, pose-driven logic through a clean, extensible API that encourages reuse, experimentation, and integration with machine learning pipelines.

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

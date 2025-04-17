---
title: Project Structure
nav_order: 2
parent: Architecture
---

# Project Structure

The `virtual_landmark` package is modular by design, organized around clear responsibilities such as geometry, introspection, and rendering. Below is an overview of the project's file hierarchy and their roles:

```bash
virtual_landmark
├── abstract_landmark.py           # Base class for managing and storing all landmark data (virtual + MediaPipe)
├── calculus.py                    # Core geometric and vector operations used to compute custom landmarks
├── decorator.py                   # Defines the @landmark decorator for registering virtual points and connections
├── drawing_utils
│   ├── connections.py             # Utility to manage and merge landmark connections (edges)
│   └── style.py                   # Styling rules for drawing landmarks and connections with MediaPipe
├── virtual_landmark.py            # Main processing pipeline for discovering and executing virtual landmarks
└── virtual_pose_landmark.py       # Dynamic enum-like system for accessing landmarks by name or index
```

Each component is self-contained but designed to interact fluidly within the system, following clean separation of concerns. For example:

- `abstract_landmark.py` provides the foundation for reading/writing landmark data.
- `virtual_landmark.py` builds on that to identify virtual landmarks via decorators.
- `drawing_utils/` handles visual output, independent from computation logic.

---

## Class Diagram

The following diagram summarizes the relationships between key classes:

![Class Diagram](./diagrams/class.png)

It highlights inheritance (e.g., `VirtualLandmark` → `AbstractLandmark`) and key collaboration patterns used to manage landmark definitions and rendering.

---

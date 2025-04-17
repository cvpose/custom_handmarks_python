---
title: Getting Started
nav_order: 1
parent: Usage
---

# Getting Started

This guide walks you through setting up the project and running your first example using virtual landmarks.

---

## 1. Installation

Before using the virtual landmark system, make sure you have Python 3.8+ installed. Then, install the required libraries:

```bash
pip install mediapipe opencv-python numpy
```

---

## 2. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/virtual_landmark_python.git
cd virtual_landmark_python
```

If you're using this inside a larger project, ensure the `virtual_landmark/` folder is in your Python path.

---

## 3. Run the Hello World Example

To verify your installation, run the Hello World example:

```bash
PYTHONPATH=src python examples/hello_world.py
```

Make sure the image file `image-2.jpeg` exists in the path:

```
examples/images/image-2.jpeg
```

If not, you can place any human photo in that directory. The image should contain a visible person for pose estimation to work properly.

---

## 4. What Happens in This Example?

- A static image is loaded and processed by MediaPipe.
- Custom landmarks (e.g., `NECK`, `MIDDLE_SHOULDER`) are calculated using geometry.
- Both built-in and virtual landmarks are rendered on top of the image using OpenCV.

You should see a window pop up with the landmarks and connections drawn over the image.

---

## 5. Next Steps

Continue with the [Create Landmark](./create_landmark.md) guide to learn how to define your own virtual landmarks.

---

---
title: Run
nav_order: 3
parent: Usage
---

# Run

This guide explains how to execute the virtual landmark system with MediaPipe and OpenCV, using a pre-defined class that computes custom landmarks.

We’ll walk through each part of the `main.py` script used in the Hello World example.

---

## 1. Import Dependencies

```python
import os
import cv2
import mediapipe as mp

from hello_world import HelloWorld
from virtual_landmark import Connections, get_extended_pose_landmarks_style
```

- `cv2` and `mediapipe` are required to process images and estimate body poses.
- `HelloWorld` is the class where virtual landmarks are defined.
- `Connections` builds the merged list of pose connections.
- `get_extended_pose_landmarks_style()` generates visual style settings.

---

## 2. Load and Process an Image

```python
image_name = 'image-2.jpeg'
image_path = os.path.join(os.getcwd(), "examples", "images", image_name)
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

- Loads the input image and converts it to RGB (required by MediaPipe).
- You can replace the image with any photo containing a full human body.

---

## 3. Run MediaPipe Pose Detection

```python
with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=2) as pose:
    results = pose.process(image_rgb)
```

- Initializes MediaPipe’s pose model.
- Processes the RGB image and stores results in `results.pose_landmarks`.

---

## 4. Create Virtual Landmark Object

```python
landmarks = HelloWorld(results.pose_landmarks.landmark)
```

- Instantiates the custom class `HelloWorld`, passing the landmarks from MediaPipe.
- Internally computes all virtual landmarks defined by `@landmark`.

---

## 5. Configure Styles and Connections

```python
extended_style = get_extended_pose_landmarks_style(landmarks)
connections = Connections(landmarks)
```

- Prepares a visual style for all landmarks.
- Merges MediaPipe’s default and virtual connections into one structure.

---

## 6. Draw and Display the Output

```python
mp_drawing.draw_landmarks(
    image=img_copy,
    landmark_list=landmarks.as_landmark_list(),
    connections=connections.ALL_CONNECTIONS,
    landmark_drawing_spec=extended_style,
    connection_drawing_spec=mp_drawing.DrawingSpec(
        color=(255, 255, 255), thickness=1
    ),
)
```

- Uses MediaPipe's drawing utilities to overlay the landmarks and connections onto the image.
- `as_landmark_list()` converts all landmarks to the MediaPipe format.

```python
cv2.imshow("Extended Landmarks", img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

- Displays the annotated image and waits for a key press to close.

---

## 7. Summary

- MediaPipe is used to detect pose landmarks.
- Custom landmarks are added with the `HelloWorld` class.
- All landmarks and connections are rendered using MediaPipe’s drawing API.

To define your own landmarks, refer to the [Create Landmark](./create_landmark.md) guide.

---

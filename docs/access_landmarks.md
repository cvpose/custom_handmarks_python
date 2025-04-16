---
title: Access Landmarks
nav_order: 2
parent: Guide
---
# Access Landmarks

Once you've defined and registered virtual landmarks using `virtual_landmark_python`, you can access them similarly to MediaPipe landmarks—either by **name** (via a registered string) or by **index** (to access the actual 3D point).

---

## Access by Name → Get the Index

Use the `virtual_landmark` object to get the index of a virtual point by its name:

```python
neck_index = landmarks.virtual_landmark.NECK
```

You can also use string-based dynamic access:

```python
neck_index = landmarks.virtual_landmark["NECK"]
```

---

## Access the 3D Point

Once you have the index, you can retrieve the actual landmark from the list:

```python
neck_point = landmarks[neck_index]

print(f"NECK: x={neck_point.x:.2f}, y={neck_point.y:.2f}, z={neck_point.z:.2f}")
```

---

## Example (Combined)

```python
# Get the index from the named registry
idx = landmarks.virtual_landmark.MIDDLE_SHOULDER

# Retrieve the landmark point
point = landmarks[idx]
print(f"MIDDLE_SHOULDER coordinates: x={point.x:.3f}, y={point.y:.3f}, z={point.z:.3f}")
```

---

## Summary

| Method                                | Returns              | Use case                         |
|---------------------------------------|-----------------------|----------------------------------|
| `landmarks.virtual_landmark.NAME`     | `int` (index)         | Look up index of virtual point   |
| `landmarks.virtual_landmark["NAME"]`  | `int` (index)         | Dynamic lookup by string         |
| `landmarks[idx]`                      | `NormalizedLandmark`  | Access actual point coordinates  |



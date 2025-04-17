---
title: Calculus
nav_order: 4
parent: Usage
---

{% include mathjax.html %}

# Calculus Reference

The `calculus` module provides a set of reusable geometric functions designed to support the definition of virtual landmarks. These operations work directly with 3D points and enable the construction of complex anatomical references, symmetry lines, extrapolated joints, and more.

Each function accepts either `NormalizedLandmark` objects (from MediaPipe) or equivalent 3D NumPy arrays, and returns a new NumPy array representing a point in space.

---

## `middle(p1, p2)`

**Description**:  
Calculates the midpoint between two points in 3D space. This is useful for identifying the center of symmetry between body parts, such as the midpoint between the shoulders or hips.

**Mathematical Formula**:

\begin{aligned}
\text{middle} = \frac{p_1 + p_2}{2}
\end{aligned}


This formula adds the coordinates of `p1` and `p2` component-wise, then divides each result by 2. The resulting point lies exactly halfway between them in 3D space.

**Example**:
```python
middle_shoulder = middle(left_shoulder, right_shoulder)
```

---

## `centroid(*points)`

**Description**:  
Computes the centroid (or geometric center) of an arbitrary number of 3D points. This is commonly used to find the average location of a region, such as a torso or limb cluster.

**Mathematical Formula**:

\begin{aligned}
\text{centroid} = \frac{1}{n} \sum_{i=1}^{n} p_i
\end{aligned}

Each coordinate (x, y, z) is averaged independently over all input points. This results in a new point that represents the average spatial location of the entire group.

**Example**:
```python
center = centroid(p1, p2, p3, p4)
```

---

## `projection(p1, p2, target)`

**Description**:  
Projects a point (`target`) orthogonally onto the line defined by two other points (`p1` and `p2`). This is especially useful for anatomical references that must be aligned along limbs or axes.

**Mathematical Formula**:


\begin{aligned}
v &= p_2 - p_1 \\n
u &= \text{target} - p_1 \\n
\text{proj} &= p_1 + \frac{u \cdot v}{v \cdot v} \cdot v
\end{aligned}



- `v` is the direction vector of the line.
- `u` is the vector from the base of the line (`p1`) to the target point.
- The dot product of `u` and `v` gives the magnitude of projection along the line.
- Dividing by `v ⋅ v` normalizes the result to the line length.
- Multiplying and adding back to `p1` gives the projected point on the line.

**Example**:
```python
projected = projection(hip, knee, shoulder)
```

---

## `extend(p1, p2, factor)`

**Description**:  
Extends a point beyond another along the same direction vector. This can be used to simulate additional joints or extrapolated features such as extending from the neck toward the head.

**Mathematical Formula**:

\[
\text{extended} = p_1 + f \cdot (p_2 - p_1)
\]


The expression `(p2 - p1)` computes a directional vector. By multiplying it with `factor`, we scale the movement. Adding this to `p1` moves the new point along that direction.

**Example**:
```python
extrapolated_point = extend(neck, head, 1.5)
```

---

## `normalize(p1, p2)`

**Description**:  
Calculates the unit vector (direction with magnitude 1) pointing from `p1` to `p2`. This is useful when you need only the direction between two points.

**Mathematical Formula**:

\[
\text{unit} = \frac{p_2 - p_1}{\|p_2 - p_1\|}
\]


The numerator computes the direction vector. The denominator is its Euclidean norm. The division gives a vector with the same direction but length equal to 1.

**Example**:
```python
unit_vec = normalize(left_shoulder, right_shoulder)
```

---

## `rotate(p, axis_p1, axis_p2, angle)`

**Description**:  
Rotates a point `p` around an arbitrary 3D axis defined by two points: `axis_p1` and `axis_p2`, using a given angle in radians.

This is useful to simulate joint articulation (e.g., rotating the wrist around the forearm) or to reposition a landmark relative to a rotated frame of reference.

### Parameters

- `p`: The point to be rotated (as a NumPy array).
- `axis_p1`, `axis_p2`: Two points that define the axis of rotation.
- `angle`: The rotation angle in **radians**.

### Mathematical Concept – Rodrigues' Rotation Formula

Rodrigues' formula is a method for rotating a vector in 3D space around an arbitrary axis.

#### Step-by-step

1. Compute the **unit vector** along the rotation axis:

\[
k = \frac{axis\_p2 - axis\_p1}{\|axis\_p2 - axis\_p1\|}
\]

2. Translate the point `p` relative to the axis origin:

\[
v = p - axis\_p1
\]

3. Apply Rodrigues' rotation formula:

\[
p_{\text{rotated}} = v \cos(\theta) + (k \times v) \sin(\theta) + k(k \cdot v)(1 - \cos(\theta))
\]

4. Translate the result back to the global coordinate system:

\[
p_{\text{final}} = axis\_p1 + p_{\text{rotated}}
\]

### Visual Intuition

Imagine holding a pen between your fingers:
- The pen represents the axis `axis_p1 → axis_p2`.
- You rotate a marble around the pen — that’s your point `p` being rotated.
- The `angle` determines how far the marble spins around the pen.

---
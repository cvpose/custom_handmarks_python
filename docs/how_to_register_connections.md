
# How to Register Custom Connections

Once you've defined your own virtual landmarks, you may want to **visually connect** them to existing pose landmarks (or to each other). This allows you to extend MediaPipe's pose skeleton with meaningful new edges.

---

## what Are "Connections"?

A *connection* is simply a line between two landmarks, represented as a tuple of their **indexes**:

```python
(LEFT_SHOULDER.value, NECK.value)
```

MediaPipe internally uses `POSE_CONNECTIONS` to define the body skeleton. We can extend this list with custom edges using the `connection` parameter in the `@landmark` decorator.

---

## Defining Connections with @landmark

You can specify connections directly when declaring a virtual point:

```python
@landmark("NECK", connection=["LEFT_SHOULDER", "RIGHT_SHOULDER"])
def _neck(self):
    return calc.middle(
        self[self.virtual_landmark.LEFT_SHOULDER],
        self[self.virtual_landmark.RIGHT_SHOULDER],
    )
```

This will:

- Automatically connect `NECK` to `LEFT_SHOULDER` and `RIGHT_SHOULDER`
- Avoid duplicating edges (undirected)
- Appear visually when using the drawing function with `Connections(landmarks).ALL_CONNECTIONS`

---

## What Happens Internally?

The system will:

1. Call the decorated method to generate the virtual point.
2. Register the point in the landmark list.
3. Resolve each name in `connection` to its index (virtual or original).
4. Store the undirected connection as a tuple: `(min(idx1, idx2), max(idx1, idx2))`

All connections are available through:

```python
connections = Connections(landmarks)
all_edges = connections.ALL_CONNECTIONS
```

---

## Visual Example

If you define:

```python
@landmark("MIDDLE_HIP", connection=["LEFT_HIP", "RIGHT_HIP"])
def _middle_hip(self):
    return calc.middle(
        self[self.virtual_landmark.LEFT_HIP],
        self[self.virtual_landmark.RIGHT_HIP],
    )
```

The resulting visual skeleton will include a horizontal line between the hips through `MIDDLE_HIP`.

---

## Best Practices

- Avoid connecting the same pair in both directions. The system deduplicates automatically.
- You can connect to virtual and MediaPipe landmarks alike.
- Use expressive names like `MIDDLE_SHOULDER`, `NECK`, `THORAX` to clarify visual topology.

---

With connections, your custom skeleton becomes more meaningful and supports pose symmetry analysis, debugging, and visualization.

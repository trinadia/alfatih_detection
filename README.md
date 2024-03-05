```
for *xyxy, conf, cls in det:
                # Get coordinates of the detected box
                x1, y1, x2, y2 = map(int, xyxy)
                print(f"Object {i+1}: Class {int(cls)}, Confidence: {conf}, Coordinates: ({x1}, {y1}), ({x2}, {y2})")
```

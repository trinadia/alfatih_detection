```
for *xyxy, conf, cls in det:
                # Get coordinates of the detected box
                x1, y1, x2, y2 = map(int, xyxy)
                print(f"Object {i+1}: Class {int(cls)}, Confidence: {conf}, Coordinates: ({x1}, {y1}), ({x2}, {y2})")
```
### Notes
- setting delay time after detecting the target, due to robot's legs movement duration
- deactivate the live preview

---
### Temporary output of `detect.py`

```
0: 480x640 1 real, 1210.8ms
Object 1: Class 1, Confidence: 0.8163043856620789, Coordinates: (183, 146), (384, 380)
(283, 263)

Error: (43, -57)

0: 480x640 1 real, 1152.6ms
Object 1: Class 1, Confidence: 0.7908230423927307, Coordinates: (179, 152), (383, 377)
(281, 264)

Error: (41, -56)
0: 480x640 1 dummy, 1 real, 1357.6ms
```

### Changing passkey
`ssh-keygen -p -f /path/to/your/private/key`

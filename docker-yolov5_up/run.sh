#!/bin/bash
# export PYTHONPATH=/weights:$PYTHONPATH
xhost +local:
sudo docker run \
       -it \
       --rm \
       --runtime nvidia \
       --network host \
       --device /dev/video0:/dev/video0:mrw \
       -e DISPLAY=$DISPLAY \
       -e LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1 \
       -v /tmp/.X11-unix/:/tmp/.X11-unix \
       -v /home/alfatih/docker-yolov5:/weights \
       yolov5 python3.8 detect_display.py --source 0 --weights /weights/best_new_640.pt

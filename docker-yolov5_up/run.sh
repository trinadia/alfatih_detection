xhost +local:
/usr/bin/sudo /usr/bin/docker run \
       -i \
       --rm \
       --runtime nvidia \
       --network host \
       --device /dev/ttyACM0:/dev/ttyACM0 \
       --device /dev/video0:/dev/video0:mrw \
       -e DISPLAY=$DISPLAY \
       -e LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1 \
       -v /tmp/.X11-unix/:/tmp/.X11-unix \
       -v /home/alfatih/docker-yolov5:/weights \
       yolov5 python3.8 detect_ACM0.py --source 0 --weights /weights/best_new_640.pt

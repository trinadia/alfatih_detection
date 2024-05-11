Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1
source myenv/bin/activate
cd yolov5
python detect.py --weights best_new_640.pt --source 0

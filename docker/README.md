sudo docker run -it --rm --runtime nvidia --network host nvcr.io/nvidia/l4t-tensorflow:r32.7.1-tf2.7-py3

1. build: `docker build -t alfatih_tf .`
2. run: `docker run -it -v /home/alfatih/alfatih-tf:/tensorflow/models alfatih_tf`

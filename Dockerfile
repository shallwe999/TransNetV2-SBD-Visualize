FROM tensorflow/tensorflow:2.1.1-gpu

RUN pip3 --no-cache-dir install \
    opencv-python \    
    Pillow \
    ffmpeg-python

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    python-tk

COPY setup.py /tmp
COPY inference /tmp/inference

RUN cd /tmp && python3 setup.py install && rm -r *

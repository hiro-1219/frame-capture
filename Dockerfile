FROM python:3.9-slim

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

WORKDIR /app

#ENV LIB="libswscale-dev \
#  libtbb2 \
#  libtbb-dev \
#  libjpeg-dev \
#  libpng-dev \
#  libtiff-dev \
#  libglib2.0-0 \
#  libsm6 \
#  libxext6 \
#  libavformat-dev \
#  libpq-dev"
#RUN apt install -y libgl1-mesa-dev
#RUN apt install -y libopencv-dev

RUN apt update \
  && apt -y upgrade \
  && apt install --no-install-recommends -qy libswscale-dev \
  libgl1-mesa-dev libglib2.0-0 tk \
  libtbbmalloc2 \
  libtbb-dev \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libglib2.0-0 \
  libsm6 \
  libxext6 \
  libavformat-dev \
  libpq-dev \
  && apt-get clean \
  && apt-get autoclean \
  && apt-get autoremove \
  && rm -rf /tmp/* /var/tmp/* \
  && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install -r requirements.txt

CMD ["/app/main.py"]
ENTRYPOINT ["python3"]

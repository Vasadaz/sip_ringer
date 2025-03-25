FROM ubuntu:24.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    iputils-ping \
    net-tools \
    curl \
    git \
    wget \
    nano \
    libasound2-dev \
    libssl-dev \
    libv4l-dev \
    libsdl2-dev \
    libsdl2-gfx-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-net-dev \
    libsdl2-ttf-dev \
    libx264-dev \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev  \
    libavutil-dev \
    libavcodec-extra \
    libopus-dev \
    libopencore-amrwb-dev \
    libopencore-amrnb-dev \
    libvo-amrwbenc-dev \
    subversion \
    swig


RUN mkdir -p /home/sip_ringer/pjproject
WORKDIR /home/sip_ringer/pjproject

RUN wget https://github.com/pjsip/pjproject/archive/refs/tags/2.15.1.tar.gz && \
    tar -xzvf *.tar.gz && \
    mv ./pjproject*/* ./ && \
    rm -r ./pjproject* && \
    rm *.tar.gz

RUN ./configure CFLAGS="-fPIC"
RUN make dep
RUN make
RUN make install

WORKDIR /home/sip_ringer/pjproject/pjsip-apps/src/swig/python

RUN make
RUN make install

WORKDIR /home/sip_ringer

COPY ./requirements.txt .
COPY ./hw.py .
COPY ./.env .


RUN pip install -r requirements.txt --break-system-packages --ignore-installed --no-cache-dir

EXPOSE 5060/udp

CMD ["/bin/bash"]

# docker build -t pj -f pj.dockerfile .
# docker run -it --rm --name pj_c --network net -p 5060:5060/udp pj
# docker run --name=asterisk_test --hostname=asterisk_new --net=MacVlanNetwork -- ip=172.16.3.196 pj

# docker build -t pjsip -f dockerfiles/py.dockerfile.debian . && docker run -it --rm --network net --add-host=host.docker.internal:host-gateway pjsip
# docker build -t pjsip -f dockerfiles/py.dockerfile.debian
# docker run -it --rm --network net --add-host=host.docker.internal:host-gateway pjsip
# docker run -it --rm --network net --add-host=host.docker.internal:host-gateway -v ${pwd}:/home/THE-PJPROJECT pjsip


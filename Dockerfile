FROM gcr.io/tensorflow/tensorflow:latest-gpu-py3

COPY requirements.txt .

RUN pip --no-cache-dir install --upgrade pip && \
    pip --no-cache-dir install -r requirements.txt && \
    pip --no-cache-dir install nipype SimpleITK

RUN apt-get update && apt-get install -y --no-install-recommends \
      cmake \
      git \
      && \
   apt-get clean && \
   rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install git+https://www.github.com/farizrahman4u/keras-contrib.git

WORKDIR /code
RUN git clone https://github.com/stnava/ANTs.git && \
    mkdir /ants && \
    cd /ants && \
    cmake /code/ANTs && \
    make -j 4 

ENV ANTSPATH=/ants/bin
ENV PATH="${ANTSPATH}:${PATH}"

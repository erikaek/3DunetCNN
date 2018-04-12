FROM gcr.io/tensorflow/tensorflow:latest-gpu-py3

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y --no-install-recommends \
      cmake \
      git \
      wget \
      libopenmpi-dev \
      && \
   apt-get clean && \
   pip --no-cache-dir install --upgrade pip && \
   rm -rf /var/lib/apt/lists/*

WORKDIR /code
RUN wget --no-http-keep-alive --output-document=hdf5-1.10.2.tar.gz "https://www.hdfgroup.org/package/source-gzip-2/?wpdmdl=11810&refresh=5ace0c6e959611523453038" && \
    tar -xzvf hdf5-1.10.2.tar.gz && \
    cd hdf5-1.10.2 && \
    ./configure --enable-threadsafe --enable-cxx --enable-unsupported && \
    make -j4 && \
    make install && \
    cd .. 

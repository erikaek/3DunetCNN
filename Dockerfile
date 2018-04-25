FROM gcr.io/tensorflow/tensorflow:latest-gpu-py3

RUN mkdir /req

COPY requirements.txt /req

RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y --no-install-recommends \
      cmake \
      git \
      wget \
      libopenmpi-dev \
      gdb python3-all-dbg \
      && \
   apt-get clean && \
   pip --no-cache-dir install --upgrade pip && \
   rm -rf /var/lib/apt/lists/*


# WORKDIR /code
# RUN wget --no-http-keep-alive --output-document=hdf5-1.10.2.tar.gz "https://www.hdfgroup.org/package/source-gzip-2/?wpdmdl=11810&refresh=5ace0c6e959611523453038" && \
#    tar -xzvf hdf5-1.10.2.tar.gz && \
#    cd hdf5-1.10.2 && \
#    ./configure --enable-threadsafe --enable-cxx --enable-unsupported && \
#    make -j4 && \
#    make install && \
#    cd .. && \
#    pip uninstall -y h5py && \
#    git clone https://github.com/h5py/h5py.git && \
#    cd h5py/ && \
#    python3 setup.py configure --hdf5=/code/hdf5-1.10.2/hdf5 && \
#    python3 setup.py build && \
#    python3 setup.py install && \
#    cd ..

WORKDIR /req
RUN pip --no-cache-dir install -r requirements.txt && \
    pip --no-cache-dir install nipype SimpleITK

RUN pip --no-cache-dir install git+https://www.github.com/farizrahman4u/keras-contrib.git

WORKDIR /code
RUN git clone https://github.com/stnava/ANTs.git && \
    mkdir /ants && \
    cd /ants && \
    cmake /code/ANTs && \
    make -j 4 

ENV ANTSPATH=/ants/bin
ENV PATH="${ANTSPATH}:${PATH}"

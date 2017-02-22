FROM tensorflow/tensorflow

WORKDIR /DeepOSM

# install python-gdal
RUN add-apt-repository ppa:ubuntugis/ppa && \
    apt-get update && \
    apt-get install -y python-gdal

# install other required packages
RUN apt-get update && \
    apt-get install -y \
    	    libjpeg-dev \
    	    git cmake build-essential \
	    libboost-all-dev libbz2-dev

# install libosmium and pyosmium bindings
RUN git clone https://github.com/osmcode/libosmium.git /libosmium && \
    cd /libosmium && mkdir build && cd build && cmake .. && make && \
    git clone https://github.com/osmcode/pyosmium.git /pyosmium && \
    cd /pyosmium && pwd && python setup.py install

# install other python packages using pip
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /DeepOSM

CMD /bin/bash

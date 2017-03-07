#!/bin/bash -e

USE_GPU=0
if [ "$1" == "cpu" ]; then
    USE_GPU=0
    shift 1
elif [ "$1" == "gpu" ]; then
    USE_GPU=1
    shift 1
fi

if [ $USE_GPU == 1 ]; then
    echo "(Using GPU)"
    IMAGE_NAME=deeposm:latest-gpu
    DOCKER=nvidia-docker
else
    echo "(Using CPU)"
    IMAGE_NAME=deeposm:latest
    DOCKER=docker
fi

$DOCKER run \
    -v $(pwd):/DeepOSM \
    -w /DeepOSM \
    -e CPLUS_INCLUDE_PATH=/usr/include/gdal \
    -e C_INCLUDE_PATH=/usr/include/gdal \
    -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    -it ${IMAGE_NAME} "$@"


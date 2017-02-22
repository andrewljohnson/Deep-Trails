#!/bin/bash -e

export IMAGE_NAME=deeposm-gpu

if "$1" = "true"; then
    CMD="python bin/update_deeposmorg.py"
else
    CMD="$@"
fi

nvidia-docker run \
    -v $(pwd):/DeepOSM \
    -w /DeepOSM \
    -e CPLUS_INCLUDE_PATH=/usr/include/gdal \
    -e C_INCLUDE_PATH=/usr/include/gdal \
    -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    -t ${IMAGE_NAME} $CMD


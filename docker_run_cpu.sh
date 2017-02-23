#!/bin/bash -e

IMAGE_NAME=deeposm

docker run -v $(pwd):/DeepOSM \
       -w /DeepOSM \
       -e CPLUS_INCLUDE_PATH=/usr/include/gdal \
       -e C_INCLUDE_PATH=/usr/include/gdal \
       -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
       -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
       -it ${IMAGE_NAME}:latest "$@"

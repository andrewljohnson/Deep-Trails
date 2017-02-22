# Usage:
#    make dev              build and run /bin/bash in container.
#    make notebook         build and run jupyter notebook server.

.PHONY: dev notebook build

help:
	@echo 'Makefile for DeepOSM'
	@echo ''
	@echo 'make dev             build and run /bin/bash'
	@echo 'make notebook        build and run jupyter notebook server'

IMAGE_NAME = deeposm

build: 
	docker build -t $(IMAGE_NAME) .

dev: build
	./docker_run_cpu.sh

dev-gpu: 
	docker build -f Dockerfile.devel-gpu -t $(IMAGE_NAME) .
	./docker_run_gpu.sh false

update-deeposmorg: 
	docker build -f Dockerfile.devel-gpu -t $(IMAGE_NAME) .
	./docker_run_gpu.sh true

notebook: build
	docker run -p 8888:8888 \
               -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
               -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
               -v `pwd`:/DeepOSM \
               -it $(IMAGE_NAME) /run_jupyter.sh

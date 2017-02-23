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

Dockerfile.cpu: Dockerfile.base
	cp $< $@ 

build-cpu: Dockerfile.cpu
	docker build -f $< -t $(IMAGE_NAME):latest .

Dockerfile.gpu: Dockerfile.base
	sed 's|^FROM tensorflow/tensorflow:latest|FROM tensorflow/tensorflow:latest-gpu|' $< > $@

build-gpu: Dockerfile.gpu
	docker build -f $< -t $(IMAGE_NAME):latest-gpu .

build: build-cpu

dev-cpu: build-cpu
	./docker_run_cpu.sh

dev: dev-cpu

dev-gpu: build-gpu
	./docker_run_gpu.sh

test: build-cpu
	./docker_run_cpu.sh python -m unittest discover

update-deeposmorg: build-gpu
	./docker_run_gpu.sh python bin/update_deeposm.org

notebook: build
	docker run -p 8888:8888 \
               -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
               -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
               -v `pwd`:/DeepOSM \
               -it $(IMAGE_NAME) /run_jupyter.sh

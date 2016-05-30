# Usage:
#    make dev              build and run /bin/bash in container.

.PHONY: dev notebook build

help:
	@echo 'Makefile for deeposm.org'
	@echo ''
	@echo 'make dev             build and run /bin/bash'

IMAGE_NAME = deeposm.org

build:
	docker build -t $(IMAGE_NAME) .

dev: build
	docker run -v `pwd`:/deeposm.org \
               -w /deeposm.org \
               -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
               -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
               -it $(IMAGE_NAME) /bin/bash
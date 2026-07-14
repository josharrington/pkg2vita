IMAGE_NAME := pkg2vita
ENGINE ?= docker

.PHONY: build run

build:
	$(ENGINE) build -t $(IMAGE_NAME) .

run:
	@ifeq ($(ZIPDIR),)
	$(error Usage: make run ZIPDIR=/path/to/zip/directory)
	@endif
	$(ENGINE) run --rm -v $(ZIPDIR):/zip $(IMAGE_NAME)

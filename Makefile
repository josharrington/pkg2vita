IMAGE_NAME := pkg2vita
ENGINE ?= docker

.PHONY: build run

build:
	$(ENGINE) build -t $(IMAGE_NAME) .

run:
	@if [ -z "$(ZIPDIR)" ]; then echo "Usage: make run ZIPDIR=/path/to/zip/directory"; exit 1; fi
	@$(ENGINE) run --rm -v $(ZIPDIR):/zip $(IMAGE_NAME)

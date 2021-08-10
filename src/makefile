.PHONY: clean

NAME 	   	:= Influencia del Suavizado por Difusión Anisotrópica en Imágenes de Ultrasonido
VERSION		:= 2.0
DEVELOPERS	:= Reinaldo Barrera, Juan Carlos Esquivel, Ariel Plasencia
COPYRIGHT  	:= Copyright © 2021: $(DEVELOPERS)

main: ## Compiling the project :)
	@echo "Compiling the project :)"

info: ## Display project description
	@echo "$(NAME) v$(VERSION)"
	@echo "$(COPYRIGHT)"

version: ## Show the project version
	@echo "$(NAME) v$(VERSION)"

install: ## Install the project dependencies
	pip3 install json
	pip3 install numpy
	pip3 install Pillow
	pip3 install pathlib
	pip3 install pylab-sdk
	pip3 install python-time
	pip3 install python-sympy
	pip3 install python-scipy
	pip3 install python-skimage
	pip3 install python-matplotlib

clean: ## Remove temporary files
	rm -rf output/logs/*
	rm -rf output/results/*
	rm -rf output/noisy/*
	rm -rf output/slic/*
	rm -rf __pycache__/

run: ## Run the project
	python3 Experimentacion.py

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

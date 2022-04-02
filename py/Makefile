.PHONY: requirements upgrade

# set the venv path for commands to not require sourcing the env
VENV = .env
export VIRTUAL_ENV := $(abspath ${VENV})
export PATH := ${VIRTUAL_ENV}/bin:${PATH}

$(VENV):
	python3 -m venv $@
	. $(VENV)/bin/activate; pip install -r requirements/pip.txt

requirements:
	pip install -r requirements/requirements.txt

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade:
	# Install pip-tools first so that the subsequent commands can work
	pip install -r requirements/tools.txt

	# Then upgrade packages. Order matters with the below. They should be upgraded in the order of dependencies.
	pip-compile --upgrade requirements/tools.in
	pip-compile --upgrade requirements/requirements.in
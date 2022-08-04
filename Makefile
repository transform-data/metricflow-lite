#
# Local Env/Dev Setup
#

# Python venv helpers
VENV_NAME?=venv

.PHONY: venv
venv:
	python3 -m venv $(VENV_NAME) && echo "To activate your new virtual environment, run:\nsource $(VENV_NAME)/bin/activate"

.PHONY: remove_venv
remove_venv:
	rm -rf $(VENV_NAME) && echo "If $(VENV_NAME) was active when you ran this command you will need to run deactivate"

# Install metricflow for development work.
.PHONY: install
install:
	poetry install

# Testing and linting
.PHONY: test
test:
	poetry run pytest metricflow_lite/test/

.PHONY: lint
lint:
	pre-commit run --all-files

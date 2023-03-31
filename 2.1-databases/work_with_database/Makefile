# Define variables
PYTHON=python
PIP=pip
MANAGE=python manage.py

# Define targets
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  help         - Display this help message"
	@echo "  install      - Install requirements"
	@echo "  migrate      - Apply database migrations"
	@echo "  runserver    - Start the development server"
	@echo "  shell        - Open a Python shell"
	@echo "  test         - Run the test suite"

.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: migrate
migrate:
	$(MANAGE) migrate

.PHONY: runserver
runserver:
	$(MANAGE) runserver

.PHONY: shell
shell:
	$(MANAGE) shell

.PHONY: test
test:
	$(MANAGE) test

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

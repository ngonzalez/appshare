# The documentation: translate the English pages, upload them to the
# Appshare account (the showcase's documentation reads them there).
#   make docs        translate the changed pages, then upload them all
#   make translate   only translate (needs ANTHROPIC_API_KEY, or `ant auth login`)
#   make upload      only upload (needs `client-app login`)

CLIENT_APP ?= $(shell command -v client-app 2>/dev/null || echo $(HOME)/Dev/client-app/.build/release/client-app)
VENV = .venv

.DEFAULT_GOAL := help

help: ## List the targets
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/' | expand -t 12 | sed 's/^/  /'
.PHONY: help

$(VENV)/bin/python:
	@python3 -m venv $(VENV) && $(VENV)/bin/pip install -q "anthropic==2.4.0"

translate: $(VENV)/bin/python ## Translate the pages changed since their last translation (fr, de, es)
	@$(VENV)/bin/python scripts/translate_docs.py
.PHONY: translate

upload: ## Upload "Appshare Documentation" to the account (same file names: updated in place)
	@"$(CLIENT_APP)" upload "Appshare Documentation"
.PHONY: upload

docs: translate upload ## Translate, then upload
.PHONY: docs

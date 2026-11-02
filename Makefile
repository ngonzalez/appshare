# The documentation: translate the English pages, upload them to the
# Appshare account (the showcase's documentation reads them there).
#   make docs        translate the changed pages, then upload them all
#   make translate   only translate (needs AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION)
#   make upload      only upload (needs `client-app login`)

CLIENT_APP ?= $(shell command -v client-app 2>/dev/null || echo $(HOME)/Dev/client-app/.build/release/client-app)

.DEFAULT_GOAL := help

help: ## List the targets
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/' | expand -t 12 | sed 's/^/  /'
.PHONY: help

translate: ## Translate the pages changed since their last translation (fr, de, es), with Azure AI Translator
	@python3 scripts/translate_docs.py
.PHONY: translate

upload: ## Upload "Appshare Documentation" to the account (same file names: updated in place)
	@"$(CLIENT_APP)" upload "Appshare Documentation"
.PHONY: upload

docs: translate upload ## Translate, then upload
.PHONY: docs

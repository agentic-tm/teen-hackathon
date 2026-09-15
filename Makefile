# Nokia sponsorship proposal: HTML + PDF from docs/nokia-sponsorship-map/build.py
PDF = docs/nokia-sponsorship-map.pdf
PREVIEW_DIR ?= /tmp/nokia-sponsorship-map-preview

.PHONY: pdf preview open

pdf:
	python3 docs/nokia-sponsorship-map/build.py

# One PNG per page, for a quick visual check without opening a viewer
preview: pdf
	mkdir -p $(PREVIEW_DIR)
	pdftoppm -r 70 -png $(PDF) $(PREVIEW_DIR)/page
	@ls $(PREVIEW_DIR)

open: pdf
	open $(PDF)

SKILL_NAME := bagakit-skill-maker
BAGAKIT_HOME ?= $(HOME)/.bagakit
SKILL_DIR := $(BAGAKIT_HOME)/skills/$(SKILL_NAME)
DIST_DIR ?= dist
PACKAGE := $(DIST_DIR)/$(SKILL_NAME).skill

.PHONY: install-skill package-skill test clean

install-skill:
	rm -rf "$(SKILL_DIR)"
	mkdir -p "$(SKILL_DIR)"
	cp -R SKILL.md SKILL_PAYLOAD.json agents reference scripts gate "$(SKILL_DIR)/"
	find "$(SKILL_DIR)/scripts" -type f -name "*.sh" -exec chmod +x {} +
	find "$(SKILL_DIR)/scripts" -type f -name "*.py" -exec chmod +x {} +
	@echo "installed: $(SKILL_DIR)"

package-skill: clean
	mkdir -p "$(DIST_DIR)"
	zip -r "$(PACKAGE)" SKILL.md SKILL_PAYLOAD.json agents reference scripts gate >/dev/null
	@echo "packaged: $(PACKAGE)"

test:
	./scripts_dev/test.sh

clean:
	rm -rf "$(DIST_DIR)"

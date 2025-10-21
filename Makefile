# Makefile for Formule in Movimento
# Usage:
#   make <animation_name>         - Build animation
#   make all                      - Build all animations
#   make clean                    - Remove all generated videos
#   make help                     - Show this help

.PHONY: all clean help list setup check-deps force

# Python virtual environment (shared across all Manim projects)
VENV = $(HOME)/.virtualenvs/manim
MANIM = $(VENV)/bin/manim
PYTHON = python3

# Default quality (can override: make <animation> QUALITY=qh)
QUALITY ?= ql

# Optional class filter (can override: make <animation> CLASS=RisolvereEquazione)
CLASS ?=

# List scenes flag (use: make <animation> LIST=true)
LIST ?=

# Quality flags (VERTICAL 9:16 format)
# ql = low (480x854)    - fast preview
# qm = medium (720x1280)
# qh = high (1080x1920)  - production quality
# qk = 4k (2160x3840)

# Map quality to manim output directory (vertical format - based on height)
# Manim names dirs by resolution height: 480x854 -> 854p15
QUALITY_DIR_ql = 854p15
QUALITY_DIR_qm = 1280p30
QUALITY_DIR_qh = 1920p60
QUALITY_DIR_qk = 3840p60
QUALITY_DIR = $(QUALITY_DIR_$(QUALITY))

# Resolution and frame rate by quality
RESOLUTION_ql = 480,854
RESOLUTION_qm = 720,1280
RESOLUTION_qh = 1080,1920
RESOLUTION_qk = 2160,3840
FRAMERATE_ql = 15
FRAMERATE_qm = 30
FRAMERATE_qh = 60
FRAMERATE_qk = 60

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Project root for absolute paths
PROJECT_ROOT := $(shell pwd)

# Centralized media directory
MEDIA_DIR := $(PROJECT_ROOT)/media

# ============================================================================
# AUTO-DISCOVER ANIMATIONS
# ============================================================================

# Find all animation directories (directories containing .py files)
# Format: animations/matematica/topic_name or animations/fisica/topic_name
MATEMATICA_DIRS := $(shell find animations/matematica -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
FISICA_DIRS := $(shell find animations/fisica -mindepth 1 -maxdepth 1 -type d 2>/dev/null)

# Extract animation names (basename of directory)
MATEMATICA_ANIMATIONS := $(notdir $(MATEMATICA_DIRS))
FISICA_ANIMATIONS := $(notdir $(FISICA_DIRS))

# All animations
ALL_ANIMATIONS := $(MATEMATICA_ANIMATIONS) $(FISICA_ANIMATIONS)

# Create a map: animation_name -> discipline/animation_name
# This allows us to find the path from the animation name
$(foreach anim,$(MATEMATICA_ANIMATIONS),$(eval ANIM_PATH_$(anim) = matematica/$(anim)))
$(foreach anim,$(FISICA_ANIMATIONS),$(eval ANIM_PATH_$(anim) = fisica/$(anim)))

# Create a map: animation_name -> discipline
$(foreach anim,$(MATEMATICA_ANIMATIONS),$(eval ANIM_DISCIPLINE_$(anim) = matematica))
$(foreach anim,$(FISICA_ANIMATIONS),$(eval ANIM_DISCIPLINE_$(anim) = fisica))

# ============================================================================
# MAIN TARGETS
# ============================================================================

# Default target
all: $(ALL_ANIMATIONS)

# Check if virtualenv exists
$(MANIM):
	@echo "$(RED)Error: Shared virtual environment not found at $(VENV)$(NC)"
	@echo "$(YELLOW)Please create it by running: python3 -m venv ~/.virtualenvs/manim$(NC)"
	@echo "$(YELLOW)Then install dependencies: source ~/.virtualenvs/manim/bin/activate && pip install manim$(NC)"
	@exit 1

# Help target
help:
	@echo "$(GREEN)Formule in Movimento - Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)Targets:$(NC)"
	@echo "  make <animation>              Build all scenes in animation"
	@echo "  make all                      Build all animations"
	@echo "  make list                     List all animations"
	@echo "  make clean                    Remove all generated videos"
	@echo "  make clean-cache              Remove Python cache files"
	@echo "  make setup                    Verify setup and install dependencies"
	@echo "  make check-deps               Check dependencies (LaTeX, Manim)"
	@echo ""
	@echo "$(YELLOW)Animation Building:$(NC)"
	@echo "  make build-dev                Build all animations (low quality, dev)"
	@echo "  make build-prod               Build all animations (high quality, prod)"
	@echo "  make build-animation-prod     Build specific animation for prod (ANIM=name)"
	@echo ""
	@echo "$(YELLOW)Frontend & Deployment:$(NC)"
	@echo "  make frontend-install         Install frontend dependencies"
	@echo "  make frontend-build           Build frontend for production"
	@echo "  make frontend-dev             Start frontend dev server"
	@echo ""
	@echo "$(YELLOW)Production Deployment:$(NC)"
	@echo "  make deploy                   Deploy frontend only"
	@echo "  make deploy-animations        Deploy animations only (rsync media/)"
	@echo "  make deploy-full              Deploy frontend + animations (full site)"
	@echo ""
	@echo "$(YELLOW)Local Testing (Standalone):$(NC)"
	@echo "  make deploy-podman-local      Deploy with Podman Compose (localhost:8080)"
	@echo "  make deploy-docker-local      Deploy with Docker Compose (localhost:8080)"
	@echo "  make stop-podman-local        Stop local Podman deployment"
	@echo "  make stop-docker-local        Stop local Docker deployment"
	@echo ""
	@echo "$(YELLOW)Production Deployment (via nginx-proxy):$(NC)"
	@echo "  make deploy-production        Deploy to production (with auto proxy start)"
	@echo "  make status-production        Check production status"
	@echo "  make logs-production          View production logs"
	@echo ""
	@echo "$(YELLOW)Variables:$(NC)"
	@echo "  QUALITY=<ql|qm|qh|qk>         Set quality (default: ql)"
	@echo "  CLASS=<ClassName>             Build specific class only"
	@echo "  LIST=true                     List all classes in animation"
	@echo "  ANIM=<animation_name>         Animation name for build-animation-prod"
	@echo ""
	@echo "$(YELLOW)Examples (Development):$(NC)"
	@echo "  make gas_perfetto                                # Build all scenes (low quality)"
	@echo "  make gas_perfetto LIST=true                      # List all classes"
	@echo "  make build-dev                                   # Build all for development"
	@echo "  make frontend-dev                                # Start dev server"
	@echo ""
	@echo "$(YELLOW)Examples (Production):$(NC)"
	@echo "  make gas_perfetto QUALITY=qh                     # Build gas_perfetto (high quality)"
	@echo "  make build-animation-prod ANIM=gas_perfetto      # Build for production"
	@echo "  make build-prod                                  # Build all for production"
	@echo "  make deploy-full                                 # Deploy everything"
	@echo "  make deploy-animations                           # Deploy only animations"
	@echo ""
	@echo "$(YELLOW)Available animations (auto-discovered):$(NC)"
	@echo "  $(YELLOW)Matematica ($(words $(MATEMATICA_ANIMATIONS))):$(NC) $(MATEMATICA_ANIMATIONS)"
	@echo "  $(YELLOW)Fisica ($(words $(FISICA_ANIMATIONS))):$(NC) $(FISICA_ANIMATIONS)"

# List available animations
list:
	@echo "$(GREEN)Available animations (auto-discovered):$(NC)"
	@echo ""
	@echo "$(YELLOW)Matematica ($(words $(MATEMATICA_ANIMATIONS)) animations):$(NC)"
	@if [ -z "$(MATEMATICA_ANIMATIONS)" ]; then \
		echo "  (none found)"; \
	else \
		for anim in $(MATEMATICA_ANIMATIONS); do echo "  - $$anim"; done; \
	fi
	@echo ""
	@echo "$(YELLOW)Fisica ($(words $(FISICA_ANIMATIONS)) animations):$(NC)"
	@if [ -z "$(FISICA_ANIMATIONS)" ]; then \
		echo "  (none found)"; \
	else \
		for anim in $(FISICA_ANIMATIONS); do echo "  - $$anim"; done; \
	fi

# Setup target
setup:
	@echo "$(GREEN)Verifica virtual environment condiviso...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(RED)Errore: Virtual environment non trovato in $(VENV)$(NC)"; \
		echo "$(YELLOW)Crea prima l'ambiente condiviso con:$(NC)"; \
		echo "  python3 -m venv ~/.virtualenvs/manim"; \
		echo "  source ~/.virtualenvs/manim/bin/activate"; \
		echo "  pip install manim"; \
		exit 1; \
	fi
	@echo "$(GREEN)Virtual environment trovato!$(NC)"
	@echo "$(GREEN)Verifica installazione Manim...$(NC)"
	@$(VENV)/bin/python -c "import manim; print('$(GREEN)✓ Manim versione:', manim.__version__, '$(NC)')" || \
		(echo "$(RED)✗ Manim non installato$(NC)" && exit 1)
	@echo "$(GREEN)Setup OK!$(NC)"

# Check dependencies
check-deps:
	@echo "$(GREEN)Verifica dipendenze...$(NC)"
	@echo ""
	@echo "$(YELLOW)Python:$(NC)"
	@$(PYTHON) --version || echo "$(RED)✗ Python non trovato$(NC)"
	@echo ""
	@echo "$(YELLOW)Virtual Environment:$(NC)"
	@if [ -d "$(VENV)" ]; then echo "$(GREEN)✓ Trovato in $(VENV)$(NC)"; else echo "$(RED)✗ Non trovato$(NC)"; fi
	@echo ""
	@echo "$(YELLOW)Manim:$(NC)"
	@$(VENV)/bin/python -c "import manim; print('$(GREEN)✓ Manim versione:', manim.__version__, '$(NC)')" 2>/dev/null || echo "$(RED)✗ Manim non installato$(NC)"
	@echo ""
	@echo "$(YELLOW)LaTeX:$(NC)"
	@which latex > /dev/null 2>&1 && echo "$(GREEN)✓ LaTeX installato$(NC)" || echo "$(RED)✗ LaTeX non trovato$(NC)"
	@which pdflatex > /dev/null 2>&1 && echo "$(GREEN)✓ pdflatex installato$(NC)" || echo "$(RED)✗ pdflatex non trovato$(NC)"

# ============================================================================
# GENERIC ANIMATION BUILD RULES
# ============================================================================

# Python one-liner to list Scene classes from a file
define LIST_SCENES
import ast
import sys
try:
    tree = ast.parse(open('$(1).py').read())
    scenes = [node.name for node in ast.walk(tree)
              if isinstance(node, ast.ClassDef)
              and any(base.id == 'Scene' if isinstance(base, ast.Name) else False
                     for base in node.bases if hasattr(base, 'id'))]
    if scenes:
        for s in scenes:
            print(f'  - {s}')
    else:
        print('  (no Scene classes found)')
except FileNotFoundError:
    print(f'  Error: {$(1)}.py not found', file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f'  Error parsing file: {e}', file=sys.stderr)
    sys.exit(1)
endef

# Generic function to build an animation
# Usage: $(call build_animation,animation_name,discipline,animation_path)
define build_animation
$(1): | $(MANIM)
ifeq ($$(LIST),true)
	@echo "$$(GREEN)Available scenes in $(1):$$(NC)"
	@if [ ! -f "animations/$(3)/$(1).py" ]; then \
		echo "$$(RED)Error: animations/$(3)/$(1).py not found$$(NC)"; \
		exit 1; \
	fi
	@cd animations/$(3) && $(PYTHON) -c '$$(call LIST_SCENES,$(1))'
else
	$$(MAKE) media/$(3)/videos/$$(QUALITY_DIR)/.built ANIM_NAME=$(1) ANIM_PATH=$(3) ANIM_DISCIPLINE=$(2)
endif

# Build rule for $(1)
media/$(3)/videos/$$(QUALITY_DIR)/.built: animations/$(3)/$(1).py | $$(MANIM)
	@if [ ! -f "animations/$(3)/$(1).py" ]; then \
		echo "$$(RED)Error: animations/$(3)/$(1).py not found$$(NC)"; \
		exit 1; \
	fi
	@mkdir -p media/$(3)/videos/$$(QUALITY_DIR)
	@MEDIA_OUTPUT=$(MEDIA_DIR)/$(2); \
	if [ -n "$$(CLASS)" ]; then \
		echo "$$(GREEN)Building $(1) class $$(CLASS) with quality=$$(QUALITY) (vertical)...$$(NC)"; \
		echo "$$(YELLOW)Output: $$$$MEDIA_OUTPUT/videos/$(1)/$$(QUALITY_DIR)/$$(NC)"; \
		cd animations/$(3) && $$(MANIM) --media_dir $$$$MEDIA_OUTPUT \
			--resolution $$(RESOLUTION_$$(QUALITY)) \
			--frame_rate $$(FRAMERATE_$$(QUALITY)) \
			$(1).py $$(CLASS); \
	else \
		echo "$$(GREEN)Building all $(1) scenes with quality=$$(QUALITY) (vertical)...$$(NC)"; \
		echo "$$(YELLOW)Output: $$$$MEDIA_OUTPUT/videos/$(1)/$$(QUALITY_DIR)/$$(NC)"; \
		cd animations/$(3) && $$(MANIM) --media_dir $$$$MEDIA_OUTPUT \
			--resolution $$(RESOLUTION_$$(QUALITY)) \
			--frame_rate $$(FRAMERATE_$$(QUALITY)) \
			-a $(1).py; \
	fi
	@touch $$@

.PHONY: $(1)
endef

# Generate targets for all animations
$(foreach anim,$(MATEMATICA_ANIMATIONS),$(eval $(call build_animation,$(anim),matematica,matematica/$(anim))))
$(foreach anim,$(FISICA_ANIMATIONS),$(eval $(call build_animation,$(anim),fisica,fisica/$(anim))))

# ============================================================================
# CLEANUP TARGETS
# ============================================================================

# Clean all generated videos (from centralized media directory)
clean:
	@echo "$(YELLOW)Removing all generated videos from centralized media directory...$(NC)"
	rm -rf media/
	@echo "$(GREEN)Clean complete!$(NC)"

# Clean Python cache
clean-cache:
	@echo "$(YELLOW)Rimozione cache Python...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Cache rimossa!$(NC)"

# Clean everything including .built markers
clean-all: clean clean-cache
	@echo "$(YELLOW)Removing build markers...$(NC)"
	find media -name ".built" -delete 2>/dev/null || true
	@echo "$(GREEN)Complete cleanup done!$(NC)"

# Force rebuild (ignore timestamps)
force:
	@echo "$(YELLOW)Removing build markers to force rebuild...$(NC)"
	find media -name ".built" -delete 2>/dev/null || true
	@echo "$(GREEN)Now run 'make all' or 'make <animation>' to rebuild$(NC)"

# ============================================================================
# INFO AND UTILITIES
# ============================================================================

# Info about project
info:
	@echo "$(GREEN)Formule in Movimento - Informazioni Progetto$(NC)"
	@echo ""
	@echo "$(YELLOW)Python:$(NC) $$($(PYTHON) --version 2>&1)"
	@echo "$(YELLOW)Virtual Environment (condiviso):$(NC) $(VENV)"
	@echo "$(YELLOW)Repository:$(NC) $$(git remote get-url origin 2>/dev/null || echo 'Non un repository git')"
	@echo "$(YELLOW)Branch:$(NC) $$(git branch --show-current 2>/dev/null || echo 'N/A')"
	@echo ""
	@echo "$(YELLOW)Animazioni (auto-discovered):$(NC)"
	@echo "  Matematica: $(words $(MATEMATICA_ANIMATIONS)) animazioni"
	@echo "  Fisica: $(words $(FISICA_ANIMATIONS)) animazioni"
	@echo "  Totale: $(words $(ALL_ANIMATIONS)) animazioni"
	@echo ""
	@echo "$(YELLOW)File Python:$(NC)"
	@echo "  Totale: $$(find animations -name '*.py' -not -path '*/__pycache__/*' 2>/dev/null | wc -l) file"

# Create new animation template
new-animation:
	@if [ -z "$(TOPIC)" ] || [ -z "$(DISCIPLINE)" ]; then \
		echo "$(RED)Errore: specifica DISCIPLINE (matematica/fisica) e TOPIC$(NC)"; \
		echo "Esempio: make new-animation DISCIPLINE=matematica TOPIC=derivate"; \
		exit 1; \
	fi
	@echo "$(GREEN)Creazione nuova animazione: $(DISCIPLINE)/$(TOPIC)$(NC)"
	@mkdir -p animations/$(DISCIPLINE)/$(TOPIC)
	@echo "from manim import *" > animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "class IntroScene(Scene):" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "    \"\"\"" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "    Scena introduttiva per $(TOPIC)" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "    \"\"\"" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "    def construct(self):" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "        # Sfondo bianco per tema chiaro" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "        self.camera.background_color = WHITE" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "        # Titolo" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "        title = Text(\"Titolo\", font_size=56, color=BLACK, weight=BOLD)" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "        title.to_edge(UP, buff=0.5)" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "        self.play(Write(title))" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "        self.wait(2)" >> animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py
	@echo "[CLI]" > animations/$(DISCIPLINE)/$(TOPIC)/manim.cfg
	@echo "media_dir = ../../../media/$(DISCIPLINE)" >> animations/$(DISCIPLINE)/$(TOPIC)/manim.cfg
	@echo "$(GREEN)Directory creata: animations/$(DISCIPLINE)/$(TOPIC)$(NC)"
	@echo "$(GREEN)Template file creato: animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py$(NC)"
	@echo "$(GREEN)Config file creato: animations/$(DISCIPLINE)/$(TOPIC)/manim.cfg$(NC)"
	@# Create Astro template page
	@mkdir -p frontend/src/pages/$(DISCIPLINE)
	@TOPIC_TITLE=$$(echo "$(TOPIC)" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g'); \
	TOPIC_URL=$$(echo "$(TOPIC)" | sed 's/_/-/g'); \
	DISCIPLINE_LABEL=$$(if [ "$(DISCIPLINE)" = "matematica" ]; then echo "Matematica"; else echo "Fisica"; fi); \
	echo "---" > frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "import LessonLayout from '../../layouts/LessonLayout.astro';" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "import VideoPlayer from '../../components/VideoPlayer.astro';" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "---" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "<LessonLayout" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  title=\"$$TOPIC_TITLE\"" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  subtitle=\"[Aggiungi un sottotitolo descrittivo]\"" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  description=\"$$TOPIC_TITLE - [Descrizione per SEO] | Formule in Movimento\"" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  theme=\"$(DISCIPLINE)\"" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  breadcrumbs={[" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    { label: 'Home', href: '/' }," >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    { label: '$$DISCIPLINE_LABEL', href: '/$(DISCIPLINE)' }," >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    { label: '$$TOPIC_TITLE' }" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  ]}" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo ">" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  <div class=\"intro-section\">" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    <h2 style=\"margin-top: 0;\">[Titolo Introduzione]</h2>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    <p>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "      [Aggiungi qui una descrizione introduttiva del concetto.]" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    </p>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    <div class=\"key-concept\">" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "      <strong>Concetto Chiave:</strong>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "      <p style=\"margin-top: 10px;\">" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "        [Spiega il concetto principale in modo chiaro e accessibile]" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "      </p>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    </div>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  </div>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  <h2>Introduzione</h2>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  <div class=\"video-container\">" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    <VideoPlayer src=\"/media/$(DISCIPLINE)/videos/$(TOPIC)/IntroScene.mp4\" />" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    <div class=\"description\">" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "      <strong>Descrizione:</strong> [Descrivi cosa mostra questa animazione]" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    </div>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  </div>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  <h2>Riepilogo</h2>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  <div class=\"intro-section\">" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    <p>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "      [Riassumi i punti chiave della lezione]" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "    </p>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "  </div>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro; \
	echo "</LessonLayout>" >> frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro
	@TOPIC_URL=$$(echo "$(TOPIC)" | sed 's/_/-/g'); \
	echo "$(GREEN)Pagina Astro creata: frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro$(NC)"
	@echo ""
	@echo "$(YELLOW)L'animazione è stata auto-discovered! Prova:$(NC)"
	@echo "  make list                    # Verifica che $(TOPIC) sia nella lista"
	@echo "  make $(TOPIC) LIST=true      # Lista le scene"
	@echo "  make $(TOPIC) QUALITY=ql     # Renderizza (bassa qualità)"
	@echo "  make $(TOPIC) QUALITY=qh     # Renderizza (alta qualità)"
	@echo ""
	@echo "$(YELLOW)Prossimi passi:$(NC)"
	@echo "  1. Modifica: animations/$(DISCIPLINE)/$(TOPIC)/$(TOPIC).py"
	@echo "  2. Testa con: make $(TOPIC) QUALITY=ql"
	@TOPIC_URL=$$(echo "$(TOPIC)" | sed 's/_/-/g'); \
	echo "  3. Modifica: frontend/src/pages/$(DISCIPLINE)/$$TOPIC_URL.astro"; \
	echo "  4. Aggiorna: frontend/src/pages/$(DISCIPLINE)/index.astro"; \
	echo "  5. Test frontend: make frontend-dev"; \
	echo "  6. Deploy: make deploy-full"

# ============================================================================
# FRONTEND AND DEPLOYMENT
# ============================================================================

.PHONY: frontend-install frontend-build frontend-dev deploy-podman-local deploy-docker-local stop-podman-local stop-docker-local restart-podman-local restart-docker-local deploy-podman deploy-docker stop-podman stop-docker restart-podman restart-docker deploy-production status-production logs-production build-dev build-prod build-animation-prod deploy-animations deploy-full deploy

# Install frontend dependencies
frontend-install:
	@echo "$(GREEN)Installing frontend dependencies...$(NC)"
	cd frontend && npm install
	@echo "$(GREEN)Frontend dependencies installed!$(NC)"

# Build frontend for production
frontend-build:
	@echo "$(GREEN)Building frontend for production...$(NC)"
	cd frontend && npm run build
	@echo "$(GREEN)Frontend built to frontend/dist/$(NC)"

# Start frontend development server
frontend-dev:
	@echo "$(GREEN)Starting frontend development server...$(NC)"
	@echo "$(YELLOW)Access at http://localhost:4321$(NC)"
	cd frontend && npm run dev

# ============================================================================
# LOCAL TESTING DEPLOYMENT (Standalone)
# ============================================================================

# Deploy with Podman Compose (LOCAL TESTING ONLY)
deploy-podman-local: frontend-build
	@echo "$(GREEN)Deploying LOCAL TEST server with Podman Compose...$(NC)"
	@echo "$(YELLOW)⚠️  This is for LOCAL TESTING ONLY, not production!$(NC)"
	@echo "$(YELLOW)⚠️  For production, use: make deploy-production$(NC)"
	podman-compose -f docker-compose.local.yml up -d --build
	@echo "$(GREEN)Local deployment complete!$(NC)"
	@echo "$(YELLOW)Access at http://localhost:8080$(NC)"
	@echo ""
	@echo "$(YELLOW)Useful commands:$(NC)"
	@echo "  make stop-podman-local    # Stop the container"
	@echo "  podman ps                 # List running containers"
	@echo "  podman logs -f formule-in-movimento  # View logs"

# Deploy with Docker Compose (LOCAL TESTING ONLY)
deploy-docker-local: frontend-build
	@echo "$(GREEN)Deploying LOCAL TEST server with Docker Compose...$(NC)"
	@echo "$(YELLOW)⚠️  This is for LOCAL TESTING ONLY, not production!$(NC)"
	@echo "$(YELLOW)⚠️  For production, use: make deploy-production$(NC)"
	docker-compose -f docker-compose.local.yml up -d --build
	@echo "$(GREEN)Local deployment complete!$(NC)"
	@echo "$(YELLOW)Access at http://localhost:8080$(NC)"
	@echo ""
	@echo "$(YELLOW)Useful commands:$(NC)"
	@echo "  make stop-docker-local    # Stop the container"
	@echo "  docker ps                 # List running containers"
	@echo "  docker logs -f formule-in-movimento  # View logs"

# Stop Podman local deployment
stop-podman-local:
	@echo "$(YELLOW)Stopping local Podman deployment...$(NC)"
	podman-compose -f docker-compose.local.yml down
	@echo "$(GREEN)Stopped!$(NC)"

# Stop Docker local deployment
stop-docker-local:
	@echo "$(YELLOW)Stopping local Docker deployment...$(NC)"
	docker-compose -f docker-compose.local.yml down
	@echo "$(GREEN)Stopped!$(NC)"

# Restart Podman local deployment (after changes)
restart-podman-local: frontend-build
	@echo "$(YELLOW)Restarting local Podman deployment...$(NC)"
	podman-compose -f docker-compose.local.yml restart
	@echo "$(GREEN)Restarted!$(NC)"

# Restart Docker local deployment (after changes)
restart-docker-local: frontend-build
	@echo "$(YELLOW)Restarting local Docker deployment...$(NC)"
	docker-compose -f docker-compose.local.yml restart
	@echo "$(GREEN)Restarted!$(NC)"

# Legacy aliases (kept for backward compatibility, but show warnings)
deploy-podman: deploy-podman-local
deploy-docker: deploy-docker-local
stop-podman: stop-podman-local
stop-docker: stop-docker-local
restart-podman: restart-podman-local
restart-docker: restart-docker-local

# ============================================================================
# PRODUCTION DEPLOYMENT (via nginx-proxy)
# ============================================================================

# Deploy to production (uses /home/gu/sites/ architecture)
deploy-production: frontend-build
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)  PRODUCTION DEPLOYMENT$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Step 1: Checking proxy stack...$(NC)"
	@if ! podman ps | grep -q nginx-proxy; then \
		echo "$(RED)⚠️  nginx-proxy is not running!$(NC)"; \
		echo "$(YELLOW)Starting proxy stack...$(NC)"; \
		cd /home/gu/sites/proxy && podman-compose up -d; \
		echo "$(GREEN)✓ Proxy stack started$(NC)"; \
		sleep 3; \
	else \
		echo "$(GREEN)✓ Proxy stack is running$(NC)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Step 2: Deploying site via proxy...$(NC)"
	@cd /home/gu/sites && ./deploy.sh formule deploy
	@echo ""
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)  PRODUCTION DEPLOYMENT COMPLETE!$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Site URL:$(NC) https://$$(grep DOMAIN /home/gu/sites/formule-in-movimento/.env | cut -d= -f2)"
	@echo ""
	@echo "$(YELLOW)Check status:$(NC)"
	@echo "  cd /home/gu/sites && ./deploy.sh status"
	@echo ""
	@echo "$(YELLOW)View logs:$(NC)"
	@echo "  cd /home/gu/sites && ./deploy.sh logs formule"
	@echo "  cd /home/gu/sites && ./deploy.sh logs proxy"
	@echo "  cd /home/gu/sites && ./deploy.sh logs acme"

# Check production deployment status
status-production:
	@echo "$(GREEN)Production Deployment Status$(NC)"
	@echo ""
	@cd /home/gu/sites && ./deploy.sh status

# View production logs
logs-production:
	@echo "$(GREEN)Viewing production logs...$(NC)"
	@cd /home/gu/sites && ./deploy.sh logs formule

# ============================================================================
# ANIMATION DEPLOYMENT
# ============================================================================

# Build animations for development (low quality)
build-dev:
	@echo "$(GREEN)Building all animations for DEVELOPMENT (low quality)...$(NC)"
	$(MAKE) all QUALITY=ql
	@echo "$(GREEN)Development build complete!$(NC)"

# Build animations for production (high quality)
build-prod:
	@echo "$(GREEN)Building all animations for PRODUCTION (high quality)...$(NC)"
	$(MAKE) all QUALITY=qh
	@echo "$(GREEN)Production build complete!$(NC)"

# Build specific animation for production
build-animation-prod:
	@if [ -z "$(ANIM)" ]; then \
		echo "$(RED)Error: specify ANIM=<animation_name>$(NC)"; \
		echo "Example: make build-animation-prod ANIM=gas_perfetto"; \
		exit 1; \
	fi
	@echo "$(GREEN)Building $(ANIM) for PRODUCTION (high quality)...$(NC)"
	$(MAKE) $(ANIM) QUALITY=qh
	@echo "$(GREEN)Production build of $(ANIM) complete!$(NC)"

# Deploy ONLY animations (media files) to production
deploy-animations:
	@echo "$(GREEN)Deploying animations to production server...$(NC)"
	@if [ ! -f /home/gu/sites/deploy.sh ]; then \
		echo "$(RED)Error: deploy.sh not found at /home/gu/sites/deploy.sh$(NC)"; \
		exit 1; \
	fi
	@if [ ! -d media ]; then \
		echo "$(RED)Error: media directory not found. Run 'make build-prod' first.$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Syncing media directory to production...$(NC)"
	rsync -avz --progress media/ /home/gu/sites/formule-in-movimento/media/
	@echo "$(GREEN)Animation deployment complete!$(NC)"

# Deploy frontend AND animations to production
deploy-full: build-prod frontend-build
	@echo "$(GREEN)Deploying FULL site to production (frontend + animations)...$(NC)"
	@if [ ! -f /home/gu/sites/deploy.sh ]; then \
		echo "$(RED)Error: deploy.sh not found at /home/gu/sites/deploy.sh$(NC)"; \
		exit 1; \
	fi
	/home/gu/sites/deploy.sh
	@echo "$(YELLOW)Syncing media directory to production...$(NC)"
	rsync -avz --progress media/ /home/gu/sites/formule-in-movimento/media/
	@echo "$(GREEN)Full deployment complete!$(NC)"

# Deploy to production server (frontend only, using deploy.sh script)
deploy: frontend-build
	@echo "$(GREEN)Deploying FRONTEND to production server...$(NC)"
	@if [ ! -f /home/gu/sites/deploy.sh ]; then \
		echo "$(RED)Error: deploy.sh not found at /home/gu/sites/deploy.sh$(NC)"; \
		exit 1; \
	fi
	/home/gu/sites/deploy.sh
	@echo "$(GREEN)Frontend deployment complete!$(NC)"
	@echo "$(YELLOW)Note: To deploy animations, run 'make deploy-animations' or 'make deploy-full'$(NC)"

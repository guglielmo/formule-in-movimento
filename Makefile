.PHONY: help setup install clean clean-media clean-cache render-all list-animations test-render

# Default Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip
VENV := .venv
VENV_BIN := $(VENV)/bin

# Manim quality flags
QUALITY_LOW := -ql
QUALITY_MED := -qm
QUALITY_HIGH := -qh
QUALITY_4K := -qk

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "$(GREEN)Formule in Movimento - Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)Setup e Installazione:$(NC)"
	@echo "  make setup          - Crea virtual environment e installa dipendenze"
	@echo "  make install        - Installa/aggiorna dipendenze"
	@echo ""
	@echo "$(YELLOW)Sviluppo:$(NC)"
	@echo "  make list           - Elenca tutte le animazioni nel progetto"
	@echo "  make test-render    - Renderizza tutte le animazioni in bassa qualità (test)"
	@echo ""
	@echo "$(YELLOW)Rendering (richiede FILE e SCENE):$(NC)"
	@echo "  make preview FILE=path/to/file.py SCENE=SceneName"
	@echo "                      - Preview veloce (480p, 15fps)"
	@echo "  make render FILE=path/to/file.py SCENE=SceneName"
	@echo "                      - Rendering alta qualità (1080p, 60fps)"
	@echo "  make render-vertical FILE=path/to/file.py SCENE=SceneName"
	@echo "                      - Rendering verticale 9:16 per social media"
	@echo "  make render-4k FILE=path/to/file.py SCENE=SceneName"
	@echo "                      - Rendering 4K (2160p, 60fps)"
	@echo ""
	@echo "$(YELLOW)Pulizia:$(NC)"
	@echo "  make clean          - Rimuove file temporanei e cache"
	@echo "  make clean-media    - Rimuove tutti i video renderizzati"
	@echo "  make clean-all      - Pulizia completa (media + cache + venv)"
	@echo ""
	@echo "$(YELLOW)Esempi:$(NC)"
	@echo "  cd animations/matematica/equazioni_lineari"
	@echo "  make preview FILE=equazioni_lineari.py SCENE=RisolvereEquazione"
	@echo "  make render FILE=equazioni_lineari.py SCENE=RisolvereEquazione"

setup:
	@echo "$(GREEN)Creazione virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)Installazione dipendenze...$(NC)"
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	@echo "$(GREEN)Setup completato!$(NC)"
	@echo "$(YELLOW)Attiva l'ambiente con: source $(VENV)/bin/activate$(NC)"

install:
	@echo "$(GREEN)Installazione/aggiornamento dipendenze...$(NC)"
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	@echo "$(GREEN)Dipendenze installate!$(NC)"

list:
	@echo "$(GREEN)Animazioni disponibili:$(NC)"
	@echo ""
	@echo "$(YELLOW)Matematica:$(NC)"
	@find animations/matematica -name "*.py" -not -path "*/\.*" -not -path "*/__pycache__/*" | sed 's|animations/matematica/||' | sort
	@echo ""
	@echo "$(YELLOW)Fisica:$(NC)"
	@find animations/fisica -name "*.py" -not -path "*/\.*" -not -path "*/__pycache__/*" | sed 's|animations/fisica/||' | sort

list-scenes:
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)Errore: specifica FILE=path/to/file.py$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Scene disponibili in $(FILE):$(NC)"
	@$(VENV_BIN)/manim $(FILE) --list

preview:
	@if [ -z "$(FILE)" ] || [ -z "$(SCENE)" ]; then \
		echo "$(RED)Errore: specifica FILE e SCENE$(NC)"; \
		echo "Esempio: make preview FILE=animations/matematica/equazioni_lineari/equazioni_lineari.py SCENE=RisolvereEquazione"; \
		exit 1; \
	fi
	@echo "$(GREEN)Rendering preview: $(FILE) - $(SCENE)$(NC)"
	$(VENV_BIN)/manim -pql $(FILE) $(SCENE)

render:
	@if [ -z "$(FILE)" ] || [ -z "$(SCENE)" ]; then \
		echo "$(RED)Errore: specifica FILE e SCENE$(NC)"; \
		echo "Esempio: make render FILE=animations/matematica/equazioni_lineari/equazioni_lineari.py SCENE=RisolvereEquazione"; \
		exit 1; \
	fi
	@echo "$(GREEN)Rendering alta qualità: $(FILE) - $(SCENE)$(NC)"
	$(VENV_BIN)/manim -pqh $(FILE) $(SCENE)

render-vertical:
	@if [ -z "$(FILE)" ] || [ -z "$(SCENE)" ]; then \
		echo "$(RED)Errore: specifica FILE e SCENE$(NC)"; \
		echo "Esempio: make render-vertical FILE=animations/matematica/equazioni_lineari/equazioni_lineari.py SCENE=RisolvereEquazione"; \
		exit 1; \
	fi
	@echo "$(GREEN)Rendering verticale 9:16: $(FILE) - $(SCENE)$(NC)"
	$(VENV_BIN)/manim -pqh --resolution 1080,1920 $(FILE) $(SCENE)

render-4k:
	@if [ -z "$(FILE)" ] || [ -z "$(SCENE)" ]; then \
		echo "$(RED)Errore: specifica FILE e SCENE$(NC)"; \
		echo "Esempio: make render-4k FILE=animations/matematica/equazioni_lineari/equazioni_lineari.py SCENE=RisolvereEquazione"; \
		exit 1; \
	fi
	@echo "$(GREEN)Rendering 4K: $(FILE) - $(SCENE)$(NC)"
	$(VENV_BIN)/manim -pqk $(FILE) $(SCENE)

render-all-scenes:
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)Errore: specifica FILE=path/to/file.py$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Rendering di tutte le scene in $(FILE)$(NC)"
	$(VENV_BIN)/manim -pqh $(FILE)

test-render:
	@echo "$(GREEN)Test rendering di tutte le animazioni (bassa qualità)...$(NC)"
	@for file in $$(find animations -name "*.py" -not -path "*/\.*" -not -path "*/__pycache__/*"); do \
		echo "$(YELLOW)Testing: $$file$(NC)"; \
		$(VENV_BIN)/manim -ql $$file 2>&1 | grep -E "(Scene|ERROR|CRITICAL)" || true; \
	done
	@echo "$(GREEN)Test completato!$(NC)"

clean-cache:
	@echo "$(YELLOW)Rimozione cache Python...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Cache rimossa!$(NC)"

clean-media:
	@echo "$(RED)ATTENZIONE: Questo rimuoverà tutti i video renderizzati!$(NC)"
	@echo "Premi Ctrl+C per annullare, Enter per continuare..."
	@read confirm
	@echo "$(YELLOW)Rimozione media files...$(NC)"
	find animations -type d -name "media" -exec rm -rf {} + 2>/dev/null || true
	find animations -type d -name "Tex" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Media files rimossi!$(NC)"

clean: clean-cache
	@echo "$(GREEN)Pulizia completata!$(NC)"

clean-all: clean-cache clean-media
	@echo "$(YELLOW)Rimozione virtual environment...$(NC)"
	rm -rf $(VENV)
	@echo "$(GREEN)Pulizia completa terminata!$(NC)"

# Helper per navigare nelle directory delle animazioni
cd-matematica:
	@echo "cd animations/matematica"

cd-fisica:
	@echo "cd animations/fisica"

# Verifica che LaTeX sia installato
check-latex:
	@echo "$(GREEN)Verifica installazione LaTeX...$(NC)"
	@which latex > /dev/null 2>&1 && echo "$(GREEN)✓ LaTeX installato$(NC)" || echo "$(RED)✗ LaTeX non trovato$(NC)"
	@which pdflatex > /dev/null 2>&1 && echo "$(GREEN)✓ pdflatex installato$(NC)" || echo "$(RED)✗ pdflatex non trovato$(NC)"

# Verifica dipendenze del progetto
check-deps: check-latex
	@echo "$(GREEN)Verifica dipendenze Python...$(NC)"
	@$(VENV_BIN)/python -c "import manim; print('$(GREEN)✓ Manim versione:', manim.__version__, '$(NC)')" 2>/dev/null || echo "$(RED)✗ Manim non installato$(NC)"

# Crea una nuova animazione con template
new-animation:
	@if [ -z "$(TOPIC)" ] || [ -z "$(DISCIPLINE)" ]; then \
		echo "$(RED)Errore: specifica DISCIPLINE (matematica/fisica) e TOPIC$(NC)"; \
		echo "Esempio: make new-animation DISCIPLINE=matematica TOPIC=derivate"; \
		exit 1; \
	fi
	@echo "$(GREEN)Creazione nuova animazione: $(DISCIPLINE)/$(TOPIC)$(NC)"
	mkdir -p animations/$(DISCIPLINE)/$(TOPIC)
	@echo "$(GREEN)Directory creata: animations/$(DISCIPLINE)/$(TOPIC)$(NC)"
	@echo "$(YELLOW)Prossimi passi:$(NC)"
	@echo "  1. Crea il file Python con le scene Manim"
	@echo "  2. cd animations/$(DISCIPLINE)/$(TOPIC)"
	@echo "  3. make preview FILE=$(TOPIC).py SCENE=NomeScena"
	@echo "  4. Crea index.html per la pagina web"
	@echo "  5. Aggiorna index.html principale"

# Info sul progetto
info:
	@echo "$(GREEN)Formule in Movimento - Informazioni Progetto$(NC)"
	@echo ""
	@echo "$(YELLOW)Python:$(NC) $$($(PYTHON) --version 2>&1)"
	@echo "$(YELLOW)Virtual Environment:$(NC) $(VENV)"
	@echo "$(YELLOW)Repository:$(NC) $$(git remote get-url origin 2>/dev/null || echo 'Non un repository git')"
	@echo "$(YELLOW)Branch:$(NC) $$(git branch --show-current 2>/dev/null || echo 'N/A')"
	@echo ""
	@echo "$(YELLOW)Struttura:$(NC)"
	@echo "  Animazioni Matematica: $$(find animations/matematica -name '*.py' 2>/dev/null | wc -l) file"
	@echo "  Animazioni Fisica: $$(find animations/fisica -name '*.py' 2>/dev/null | wc -l) file"
	@echo "  Pagine HTML: $$(find animations -name 'index.html' 2>/dev/null | wc -l) pagine"

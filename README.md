# Formule in Movimento

**Animazioni matematiche e fisiche per studenti - Contenuti educativi per mobile e social media**

## Il Progetto

**Formule in Movimento** è una collezione di video animati che rendono i concetti di matematica e fisica accessibili, visivi e condivisibili. Il nome racchiude due significati:

1. **Animazioni dinamiche** - Formule, espressioni ed esperimenti che prendono vita attraverso visualizzazioni in movimento create con Manim. Non si tratta di contenuti statici, ma di video dove ogni elemento si muove, si trasforma e si anima per spiegare i concetti
2. **Contenuti mobile** - Video ottimizzati per essere fruiti "in movimento", sui dispositivi mobili e condivisi sulle piattaforme social che gli studenti usano quotidianamente

## Perché "Formule" e non "Equazioni"?

Abbiamo scelto deliberatamente "formule" invece di "equazioni" perché:
- È un termine più **accessibile** e meno intimidatorio per gli studenti
- Ha un **scope più ampio**: include formule matematiche, fisiche, chimiche
- Non evoca immediatamente ansia da compiti o verifiche
- Suona più **familiare** e meno accademico

## Caratteristiche Chiave

### 📱 Mobile-First
- **Design responsive**: Pagine web ottimizzate per smartphone e tablet
- **Video verticali**: Supporto per formati 9:16 (Stories, Reels, Shorts)
- **Caricamento veloce**: Animazioni ottimizzate per reti mobili
- **Touch-friendly**: Interfaccia pensata per l'interazione touch

### 🔗 Facile Condivisione
- **Embed semplice**: Codice incorporabile per blog e siti scolastici
- **Link diretti**: URL permanenti per ogni animazione
- **Social-ready**: Formati compatibili con TikTok, Instagram, YouTube Shorts
- **Download facilitato**: Opzioni per scaricare video per uso offline

### 🎓 Contenuti Educativi
- **Matematica**: Algebra (equazioni lineari, sistemi lineari), geometria, trigonometria, analisi, calcolo
- **Fisica**: Principalmente termodinamica (focus di quest'anno), con altri argomenti di fisica generale
- **Italiano**: Tutti i contenuti, testi e narrazione in lingua italiana
- **Progressivi**: Dal livello base a concetti più avanzati

### 🎨 Design Visivo
- **Tema chiaro**: Sfondo bianco per massima leggibilità su mobile
- **Colori contrastati**: Palette scura per testi e grafici (ottima visibilità)
- **Animazioni fluide**: Transizioni smooth create con Manim
- **Tipografia chiara**: LaTeX per formule matematiche perfettamente renderizzate

## Struttura del Progetto

```
formule-in-movimento/
├── frontend/                           # Applicazione Astro frontend
│   ├── src/
│   │   ├── pages/                     # Pagine Astro (routes)
│   │   │   ├── index.astro           # Homepage
│   │   │   ├── 404.astro             # Pagina errore
│   │   │   ├── matematica/           # Sezione matematica
│   │   │   │   ├── index.astro       # Landing sezione matematica
│   │   │   │   └── equazioni-lineari.astro  # Pagina lezione
│   │   │   └── fisica/               # Sezione fisica
│   │   │       ├── index.astro       # Landing sezione fisica
│   │   │       ├── gas-perfetto.astro  # Pagina lezione
│   │   │       ├── onde.astro        # Pagina lezione
│   │   │       └── diffrazione.astro # Pagina lezione
│   │   ├── components/               # Componenti Vue/Astro riutilizzabili
│   │   ├── layouts/                  # Layout pagine
│   │   └── styles/                   # Fogli di stile CSS
│   ├── public/                       # Asset statici (favicon, etc.)
│   │   └── media -> ../../media      # Symlink ai file video
│   ├── dist/                         # Build output (generato da npm run build)
│   └── package.json
├── animations/                        # File sorgente Python Manim
│   ├── matematica/                    # Animazioni matematica
│   │   └── [argomento]/
│   │       ├── [nome].py             # Definizioni scene Manim
│   │       └── manim.cfg             # Configurazione Manim
│   └── fisica/                        # Animazioni fisica
│       └── [argomento]/
│           ├── [nome].py
│           └── manim.cfg
├── media/                             # Directory centralizzata output video
│   ├── matematica/                    # Video organizzati per disciplina
│   │   └── [argomento]/
│   │       └── videos/
│   │           └── [quality]/        # es. 854p15, 1920p60
│   │               └── [Scene].mp4
│   └── fisica/
│       └── [argomento]/
│           └── videos/
│               └── [quality]/
│                   └── [Scene].mp4
├── docs/                              # Documentazione
│   ├── ARCHITECTURE.md               # Architettura del progetto
│   ├── DEPLOY-MODES.md               # Modalità deployment
│   └── PODMAN.md                     # Guida Podman
├── Makefile                           # Comando centrale per tutte le operazioni
├── Dockerfile                         # Build Docker per produzione
├── docker-compose.local.yml          # Config Docker/Podman per test locale
├── nginx.conf                         # Config nginx per deployment diretto
├── .python-version                    # Versione Python (3.12)
├── .github/workflows/                 # GitHub Actions (genera animazioni + deploy Vercel)
├── CLAUDE.md                          # Linee guida per lo sviluppo
├── CONTRIBUTING.md                    # Linee guida contributi
└── CHANGELOG.md                       # Storico delle modifiche

Virtual environment condiviso: ~/.virtualenvs/manim
```

## Setup Rapido

### Prerequisiti
- Python 3.12+
- LaTeX (TeX Live su Linux, MiKTeX su Windows, MacTeX su macOS)
- Browser moderno per preview

### Installazione

```bash
# Crea virtual environment condiviso (una sola volta per tutti i progetti Manim)
python3 -m venv ~/.virtualenvs/manim

# Attiva l'ambiente
source ~/.virtualenvs/manim/bin/activate  # Linux/Mac
# oppure
%USERPROFILE%\.virtualenvs\manim\Scripts\activate  # Windows

# Installa dipendenze
pip install manim

# Oppure usa il Makefile
cd formule-in-movimento
make setup
```

**Nota**: Il virtual environment è condiviso tra tutti i progetti Manim per risparmiare spazio disco (~500MB per progetto).

## Getting Started: Creare la Tua Prima Animazione

**Workflow completo in 5 passi:**

1. **Crea l'animazione** con il Makefile (genera automaticamente tutto):
   ```bash
   make new-animation DISCIPLINE=fisica TOPIC=entropia
   ```
   Questo crea:
   - `animations/fisica/entropia/entropia.py` (template Python)
   - `animations/fisica/entropia/manim.cfg` (configurazione)
   - `frontend/src/pages/fisica/entropia.astro` (template pagina web)

2. **Modifica il file Python** per aggiungere le tue scene Manim:
   - Apri `animations/fisica/entropia/entropia.py`
   - Aggiungi le tue animazioni (segui convenzioni in CLAUDE.md)
   - Usa sempre tema chiaro e testo in italiano

3. **Modifica la pagina Astro** per descrivere la lezione:
   - Apri `frontend/src/pages/fisica/entropia.astro`
   - Sostituisci i placeholder con descrizioni in italiano
   - Aggiungi sezioni per ogni video/animazione

4. **Testa tutto localmente**:
   ```bash
   # Testa l'animazione (bassa qualità, veloce)
   make entropia QUALITY=ql

   # Testa il frontend con hot reload
   make frontend-dev
   # Naviga a http://localhost:4321/fisica/entropia
   ```

5. **Deploy in produzione**:
   ```bash
   make deploy-full
   ```
   Questo compila le animazioni in alta qualità e deploya tutto automaticamente.

**Fatto! Non serve mai toccare il Makefile - tutto è auto-discovered.**

## Contenuti Disponibili

### Matematica

- **Equazioni Lineari** (`equazioni_lineari`) - Risoluzione di equazioni di primo grado con metodo grafico e algebrico
- **Sistemi di Equazioni Lineari** (`sistemi_lineari`) - Quattro metodi per risolvere sistemi 2×2: sostituzione, confronto, riduzione e Cramer

### Fisica

- **Gas Perfetto** (`gas_perfetto`) - Equazione di stato, legge dei gas perfetti, trasformazioni termodinamiche
- **Le Onde** (`onde`) - Onde trasversali e longitudinali, ampiezza e frequenza, corde/suono/terremoti, onde periodiche, impulsive e complesse, equazione dell'onda e calcolo della fase
- **Interferenza e Diffrazione** (`diffrazione`) - Principio di sovrapposizione, effetto della fase, interferenza costruttiva e distruttiva, diffrazione (Huygens) e doppia fenditura di Young

## Makefile: Il Centro di Comando del Progetto

**Tutte le operazioni passano attraverso il Makefile.** Non è necessario usare comandi Manim o npm direttamente - il Makefile gestisce tutto.

### Comandi Principali

```bash
make help              # Mostra tutti i comandi disponibili
make list              # Elenca tutte le animazioni (auto-discovered)
make <animation>       # Renderizza un'animazione specifica
make build-dev         # Compila tutte le animazioni (dev, bassa qualità)
make build-prod        # Compila tutte le animazioni (prod, alta qualità)
make frontend-dev      # Avvia server di sviluppo frontend
make deploy-full       # Deploy completo su produzione
```

### Creare una Nuova Animazione

**Usa sempre il Makefile per creare nuove animazioni:**

```bash
# Crea automaticamente struttura + template
make new-animation DISCIPLINE=matematica TOPIC=derivate

# Questo crea:
# - animations/matematica/derivate/
# - animations/matematica/derivate/derivate.py (con template)
# - animations/matematica/derivate/manim.cfg (configurato)
# - Auto-discovered! Subito disponibile

# Verifica che sia stata scoperta
make list

# Lista le scene nel file
make derivate LIST=true

# Testa l'animazione (bassa qualità, veloce)
make derivate QUALITY=ql

# Pronta per produzione (alta qualità)
make build-animation-prod ANIM=derivate
```

**Non serve mai modificare il Makefile!** Tutte le animazioni sono auto-discovered.

## Development vs Production

The project distinguishes between **development** (fast iteration) and **production** (high quality):

### Development Workflow

```bash
# Build animations for local testing (low quality, fast)
make build-dev

# Or build specific animation
make gas_perfetto QUALITY=ql

# Start frontend dev server
make frontend-dev
# Access at http://localhost:4321
```

### Production Workflow

```bash
# Build animations for production (high quality)
make build-prod                        # All animations
make build-animation-prod ANIM=gas_perfetto  # Specific animation

# Build frontend
make frontend-build

# Deploy to production
make deploy-full                       # Deploy frontend + animations
make deploy                            # Deploy frontend only
make deploy-animations                 # Deploy animations only
```

## Deployment

### Deploy to Production

The project uses a custom deployment script at `/home/gu/sites/deploy.sh` and rsync for media files:

**Full deployment (recommended):**
```bash
# Builds high-quality animations + frontend, then deploys everything
make deploy-full
```

**Partial deployments:**
```bash
# Deploy only frontend (code/HTML changes)
make deploy

# Deploy only animations (new/updated videos)
make deploy-animations
```

**Note**: The `deploy.sh` script must be present at `/home/gu/sites/deploy.sh` and the production path `/home/gu/sites/formule-in-movimento/media/` must exist for deployment to work.

### Local Testing with Docker/Podman

**IMPORTANTE: Solo per test locale, non per produzione.**

For local testing with containers:

```bash
# Using Podman (recommended)
make deploy-podman-local    # Build and start local test container
make stop-podman-local      # Stop local test container
make restart-podman-local   # Restart after changes

# Using Docker
make deploy-docker-local    # Build and start local test container
make stop-docker-local      # Stop local test container
make restart-docker-local   # Restart after changes
```

The site will be available at `http://localhost:8080`.

**For production deployment, use:**
```bash
make deploy-production      # Deploy to production via nginx-proxy
```

### Frontend Development

For rapid iteration during development:

```bash
# Start development server with hot reload
make frontend-dev
# Access at http://localhost:4321

# Build for production (without deploying)
make frontend-build
```

## Generazione automatica e Deploy su Vercel (CI/CD)

Oltre al deploy manuale, il progetto include un workflow **GitHub Actions**
(`.github/workflows/genera-animazioni.yml`) che genera le animazioni e pubblica
il sito su **Vercel**.

**Come funziona:**

1. **Discover** - scopre automaticamente le animazioni (come il Makefile).
2. **Build** (una in parallelo per ogni animazione) - usa una cache basata
   sull'hash dei sorgenti: un'animazione viene rigenerata **solo quando non è
   già stata generata** per quel contenuto. Manim/LaTeX vengono installati solo
   in caso di cache-miss, poi gira `make <animazione>`.
3. **Deploy** - costruisce il frontend, include i video e pubblica il sito
   statico su Vercel tramite Vercel CLI.

**Avvio:** è manuale, da *Actions → "Genera animazioni e deploy Vercel" →
Run workflow* (si può scegliere la qualità, default `qm`).

**Secret richiesti** (Settings → Secrets and variables → Actions):
`VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`.

> Nota: il deploy **non** usa l'integrazione Git di Vercel ma la CLI, perché
> Vercel non può eseguire Manim/LaTeX: i video vengono prebuildati in CI e poi
> caricati già pronti.

## Comandi Comuni (tutti via Makefile)

### Gestione Animazioni

```bash
# Crea nuova animazione
make new-animation DISCIPLINE=fisica TOPIC=entropia

# Elenca tutte le animazioni disponibili
make list

# Lista scene in un'animazione
make gas_perfetto LIST=true

# Renderizza animazione (sviluppo - veloce)
make gas_perfetto QUALITY=ql

# Renderizza animazione (produzione - alta qualità)
make gas_perfetto QUALITY=qh

# Renderizza classe specifica
make gas_perfetto CLASS=TrasformazioneIsoterma QUALITY=ql

# Compila tutte le animazioni
make build-dev        # Sviluppo (veloce)
make build-prod       # Produzione (alta qualità)
```

### Frontend

```bash
# Server di sviluppo con hot reload
make frontend-dev

# Build per produzione
make frontend-build
```

### Deployment

```bash
# Deploy completo (frontend + animazioni)
make deploy-full

# Deploy solo frontend
make deploy

# Deploy solo animazioni
make deploy-animations
```

### Qualità Disponibili
- `QUALITY=ql`: 480x854, 15fps (preview veloce)
- `QUALITY=qm`: 720x1280, 30fps (media qualità)
- `QUALITY=qh`: 1080x1920, 60fps (alta qualità, consigliata per produzione)
- `QUALITY=qk`: 2160x3840, 60fps (4K)

## Tecnologie Utilizzate

- **Manim Community Edition**: Libreria Python per animazioni matematiche
- **Python 3.12**: Linguaggio di programmazione
- **LaTeX**: Rendering di formule matematiche
- **HTML5/CSS3**: Pagine web responsive
- **Git**: Version control

## Changelog

Lo storico delle modifiche è in [CHANGELOG.md](CHANGELOG.md). Versione corrente: **0.4.0**.

## Contribuire

Contributi di ogni tipo sono benvenuti! Consulta [CONTRIBUTING.md](CONTRIBUTING.md) per le linee guida su come contribuire al progetto.

Per dettagli tecnici sullo sviluppo, vedi [CLAUDE.md](CLAUDE.md).

## Licenza

Questo progetto è rilasciato sotto [Apache License 2.0](LICENSE).

Copyright 2025–2026 Guglielmo Celata

## Contatti

[Da definire]

---

**Formule in Movimento** - Porta la matematica e la fisica nel palmo della mano degli studenti.

# Changelog

Tutte le modifiche rilevanti a questo progetto sono documentate in questo file.

Il formato si ispira a [Keep a Changelog](https://keepachangelog.com/it/1.1.0/)
e il progetto adotta il [Versionamento Semantico](https://semver.org/lang/it/).

## [Non rilasciato]

### Aggiunto
- **Deploy automatico per evento:** push/merge su `main` → **produzione** in
  qualità `qh` (aggiorna `formule-in-movimento.celata.com`); push su un altro
  branch → **preview** a qualità `ql`, con URL temporaneo nel riepilogo della
  run. L'avvio manuale resta disponibile con input `quality` e `target`
  (`production`/`preview`).
- **Anteprima a URL stabile:** i preview vengono aliasati a
  `anteprima.formule-in-movimento.celata.com`, così l'ultima anteprima è sempre
  allo stesso indirizzo (richiede di aggiungere il dominio su Vercel + record
  CNAME; lo step è non bloccante finché non è configurato). I domini sono ora
  assegnati con alias espliciti e la produzione usa `--skip-domain`, così i
  deploy di produzione non "rubano" l'alias dell'anteprima (di conseguenza il
  dominio `*.vercel.app` di default non si auto-aggiorna: l'indirizzo canonico
  di produzione è `formule-in-movimento.celata.com`).
- **Immagine CI con Manim + LaTeX preinstallati** (`docker/Dockerfile.ci`):
  in cache-miss il rendering gira dentro l'immagine, senza reinstallare apt/pip
  a ogni run. L'immagine è costruita e pubblicata su GHCR dal job `ci-image`
  dello stesso workflow (auto-bootstrap, tag = hash di Dockerfile+requirements).

### Modificato
- **Documentazione di deploy allineata al processo reale (GitHub Actions → Vercel).**
  `CLAUDE.md`, `README.md` e `docs/ARCHITECTURE.md` ora descrivono solo questo
  flusso; nuova guida operativa `DEPLOYMENT.md` con secret, dominio custom
  (`formule-in-movimento.celata.com`, HTTPS via Vercel) e procedure di cleanup
  (deployment Vercel, cache GitHub Actions, branch mergiati).

### Rimosso
- File e target del vecchio deploy self-hosted, non più usati: `Dockerfile`,
  `docker-compose.local.yml`, `nginx.conf`, `nginx-docker.conf`, `404.html`,
  `docs/PODMAN.md`, `docs/DEPLOY-MODES.md` e i target `make deploy*`
  (podman/docker/nginx-proxy, `/home/gu/sites`).

## [0.4.0] - 2026-06-29

### Modificato
- Il capitolo "Interferenza e Rifrazione" è stato sostituito con **"Interferenza e Diffrazione"**:
  l'arco didattico (sovrapposizione → fase → interferenza) porta naturalmente alla diffrazione,
  non alla rifrazione.

### Aggiunto
- **Animazione di fisica "Interferenza e Diffrazione"** (`animations/fisica/diffrazione/`) —
  5 scene verticali: somma di onde, effetto della fase, interferenza costruttiva e distruttiva,
  diffrazione (principio di Huygens) e doppia fenditura di Young (frange, `d sin θ = m λ`).
  - Pagina lezione `frontend/src/pages/fisica/diffrazione.astro` e card nell'indice di fisica.
- **Tool interattivo "distanze reali"** (`CalcolatoreDiffrazione.vue`): si sceglie il colore
  (lunghezza d'onda) e, a fenditure fisse, si vede come varia la distanza dello schermo necessaria
  per osservare le frange (Δy = λL/d), con doppia lettura (trova L / trova Δy), verdetto pratico e
  anteprima delle frange su righello in scala reale (mm).
- Header di licenza Apache-2.0 nei file sorgente (Python e Vue); copyright aggiornato a 2025–2026.

### Rimosso
- Animazione `rifrazione` (sostituita da `diffrazione`).

## [0.3.0] - 2026-06-29

### Aggiunto
- **Animazione di fisica "Interferenza e Rifrazione"** (`animations/fisica/rifrazione/`) —
  5 scene verticali: somma di onde (principio di sovrapposizione), effetto della fase,
  interferenza costruttiva e distruttiva, fronti d'onda e raggi, rifrazione (legge di Snell).
  - Pagina lezione `frontend/src/pages/fisica/rifrazione.astro` e card nell'indice di fisica.

## [0.2.0] - 2026-06-29

### Aggiunto
- **Pipeline CI/CD con GitHub Actions** (`.github/workflows/genera-animazioni.yml`):
  workflow manuale (`workflow_dispatch`) che genera le animazioni con `make` e
  pubblica il sito su Vercel.
  - Auto-discovery delle animazioni e build in parallelo (una matrice per animazione).
  - Cache per-animazione basata sull'hash dei sorgenti: un'animazione viene
    rigenerata **solo quando non è già stata generata** per quel contenuto.
  - Installazione di Manim/LaTeX/ffmpeg solo in caso di cache-miss.
  - Deploy del sito statico (frontend + video) su Vercel tramite Vercel CLI.
- **Configurazione Vercel** (`frontend/vercel.json`) con URL puliti (`cleanUrls`).
- **Animazione di fisica "Le Onde"** (`animations/fisica/onde/`) — 9 scene verticali:
  introduzione, onde trasversali e longitudinali, ampiezza/lunghezza d'onda/frequenza,
  esempi reali (corde, suono, terremoti), onde periodiche e impulsive, onde complesse,
  equazione dell'onda e calcolo della fase, la fase nel tempo, la fase come angolo.
  - Pagina lezione `frontend/src/pages/fisica/onde.astro` e card nell'indice di fisica.

### Modificato
- **Helper `make new-animation`** più robusto: il template Python usa la root del
  progetto calcolata dinamicamente (niente path hardcoded) e il `manim.cfg` generato
  include le dimensioni del formato verticale 9:16 (`frame_width`/`frame_height`).

### Corretto
- **`gas_perfetto`**: rimosso il path assoluto hardcoded che causava
  `No module named animations` durante il rendering in CI.

## [0.1.0] - 2025

### Aggiunto
- Architettura modernizzata con frontend **Astro** (+ componenti Vue) e
  **Makefile** come interfaccia unica per tutte le operazioni (build, frontend, deploy).
- Auto-discovery delle animazioni e separazione sviluppo/produzione.
- Animazioni di matematica: **Equazioni Lineari**, **Sistemi di Equazioni Lineari**.
- Animazione di fisica: **Gas Perfetto**.
- Componente `VideoPlayer` con selezione automatica della qualità disponibile.

## [0.0.1] - 2025

### Aggiunto
- Commit iniziale del progetto **Formule in Movimento**.

[Non rilasciato]: https://github.com/guglielmo/formule-in-movimento/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.4.0
[0.3.0]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.3.0
[0.2.0]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.2.0
[0.1.0]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.1.0
[0.0.1]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.0.1

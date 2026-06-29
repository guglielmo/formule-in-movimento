# Changelog

Tutte le modifiche rilevanti a questo progetto sono documentate in questo file.

Il formato si ispira a [Keep a Changelog](https://keepachangelog.com/it/1.1.0/)
e il progetto adotta il [Versionamento Semantico](https://semver.org/lang/it/).

## [Non rilasciato]

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

[Non rilasciato]: https://github.com/guglielmo/formule-in-movimento/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.3.0
[0.2.0]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.2.0
[0.1.0]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.1.0
[0.0.1]: https://github.com/guglielmo/formule-in-movimento/releases/tag/v0.0.1

# Architettura & Deploy

Questo documento descrive com'è strutturato **Formule in Movimento** e come
arriva online.

## Componenti

```
┌──────────────────────┐     make <topic>      ┌──────────────────────┐
│  animations/          │ ───────────────────▶ │  media/               │
│  (sorgenti Manim .py) │   (Manim + LaTeX)     │  (video .mp4)         │
└──────────────────────┘                        └──────────┬───────────┘
                                                            │ symlink
                                                            │ frontend/public/media
                                                            ▼
                       make frontend-build       ┌──────────────────────┐
                       (Astro)                    │  frontend/dist/       │
                                                  │  (sito statico+video) │
                                                  └──────────┬───────────┘
                                                             │
                                                             ▼
                                                  ┌──────────────────────┐
                                                  │  Vercel (CDN + HTTPS) │
                                                  └──────────────────────┘
```

- **`animations/`** — sorgenti Python Manim, organizzati in `matematica/` e
  `fisica/`. Ogni argomento ha la sua cartella con `<topic>.py` e `manim.cfg`.
- **`media/`** — output video generati da Manim (non versionato, vedi
  `.gitignore`). Organizzato per `<disciplina>/<topic>/videos/<quality>/`.
- **`frontend/`** — applicazione [Astro](https://astro.build) (con componenti
  Vue) che genera un sito statico. I video sono raggiungibili tramite il symlink
  `frontend/public/media -> ../../media`.
- **`Makefile`** — interfaccia unica per tutte le operazioni (build animazioni,
  build/dev frontend). Vedi `CLAUDE.md` e `README.md`.

## Deploy: GitHub Actions → Vercel

Il sito è **statico** e viene pubblicato su **Vercel**. Manim e LaTeX non sono
disponibili sui runtime di Vercel, quindi i video vengono **prebuildati in CI**
(GitHub Actions) e caricati su Vercel già pronti — il deploy usa la **Vercel
CLI**, non l'integrazione Git nativa di Vercel.

Il workflow `.github/workflows/genera-animazioni.yml` esegue tre fasi:

1. **discover** — scopre le animazioni (stessa auto-discovery del Makefile).
2. **build** — una matrice per animazione, con cache basata sull'hash dei
   sorgenti: un'animazione viene rigenerata **solo se il suo contenuto è
   cambiato**. In caso di cache-miss installa Manim/LaTeX ed esegue
   `make <topic>`.
3. **deploy** — raccoglie tutti i media, esegue `make frontend-build`, include i
   video nella `dist/` e pubblica su Vercel.

Avvio: **GitHub → Actions → "Genera animazioni e deploy Vercel" → Run workflow**
(si può scegliere la qualità, default `qm`).

HTTPS e certificati sono gestiti automaticamente da Vercel (Let's Encrypt),
anche sul dominio custom.

Per la guida operativa completa (secret, dominio custom, manutenzione) vedi
**[../DEPLOYMENT.md](../DEPLOYMENT.md)**.

## Sviluppo locale

Per iterare in locale non serve Vercel:

```bash
# Genera un'animazione in bassa qualità (veloce)
make <topic> QUALITY=ql

# Avvia il frontend con hot reload (http://localhost:4321)
make frontend-dev
```

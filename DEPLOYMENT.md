# Deploy & Manutenzione

Il sito **Formule in Movimento** è statico e viene pubblicato su **Vercel**
tramite **GitHub Actions**. Questo è l'unico processo di deploy supportato.

> Perché non l'integrazione Git nativa di Vercel? Perché Vercel non può eseguire
> Manim/LaTeX per generare i video. I video vengono quindi prebuildati in CI e
> caricati su Vercel già pronti, usando la Vercel CLI.

## 1. Come fare un deploy

Il workflow `.github/workflows/genera-animazioni.yml` gira in due modi:

- **Automatico a ogni push** (qualsiasi branch) → **deploy di preview** con un
  URL temporaneo, a qualità `ql` (render veloce). La produzione **non** viene
  toccata. L'URL del deploy è nel riepilogo della run (*Actions → run → Summary*).
- **Manuale** (*Actions → "Genera animazioni e deploy Vercel" → Run workflow*) →
  scegli `quality` (`ql`/`qm`/`qh`/`qk`) e `target`:
  - `production` → pubblica in produzione (`vercel deploy --prod`);
  - `preview` → solo anteprima.

Fasi del workflow:

1. **setup** — determina qualità e ambiente in base all'evento.
2. **discover** — scopre le animazioni (auto-discovery, come il Makefile).
3. **build** — genera ogni animazione con `make <topic>`. Usa una cache basata
   sull'hash dei sorgenti: rigenera **solo** ciò che è cambiato; in cache-hit
   non rirenderizza e non scarica nemmeno l'immagine. In cache-miss il rendering
   gira **dentro l'immagine CI** con Manim/LaTeX preinstallati (vedi §2.2).
4. **deploy** — `make frontend-build`, include i video nella `dist/` e pubblica
   su Vercel.

HTTPS e certificati sono gestiti automaticamente da Vercel.

> **Nota sui preview Vercel:** ogni push crea un deployment di anteprima che si
> accumula nello storico. Ripuliscili periodicamente (vedi §4).

## 2. Configurazione una tantum

### 2.1 Secret GitHub (Settings → Secrets and variables → Actions)

| Secret              | Dove trovarlo                                            |
|---------------------|---------------------------------------------------------|
| `VERCEL_TOKEN`      | Vercel → Account Settings → Tokens                      |
| `VERCEL_ORG_ID`     | file `.vercel/project.json` (campo `orgId`) dopo `vercel link`, oppure Vercel → Team Settings |
| `VERCEL_PROJECT_ID` | file `.vercel/project.json` (campo `projectId`)         |

Per ottenere `orgId`/`projectId` la prima volta:

```bash
cd frontend
npx vercel link        # collega la cartella al progetto Vercel
cat .vercel/project.json
```

(`.vercel/` è in `.gitignore` e non va committato.)

### 2.2 Immagine CI con Manim + LaTeX

Per non reinstallare apt/pip a ogni rendering, le animazioni vengono generate
dentro un'immagine Docker con Manim e LaTeX preinstallati, pubblicata su **GHCR**
come `ghcr.io/guglielmo/formule-in-movimento-ci:latest`.

- Definizione: `docker/Dockerfile.ci`.
- Build/push: workflow **`.github/workflows/build-ci-image.yml`**, che gira
  automaticamente quando cambiano `docker/Dockerfile.ci` o `requirements.txt`
  (oppure a mano da *Actions → "Build immagine CI" → Run workflow*).

> **Bootstrap (prima volta):** l'immagine deve esistere **prima** che il
> workflow di deploy provi a renderizzare. Dopo aver mergiato in `main`, il push
> crea `docker/Dockerfile.ci` e fa partire "Build immagine CI"; attendi che
> finisca prima di affidarti ai render. Se un primo run di preview parte prima
> che l'immagine sia pronta, basta rilanciarlo.

Il workflow usa l'immagine solo in **cache-miss**: se i sorgenti di
un'animazione non cambiano, non viene renderizzata e l'immagine non viene
nemmeno scaricata.

## 3. Dominio custom: formule-in-movimento.celata.com (HTTPS)

Il sito è servito sul dominio custom **`formule-in-movimento.celata.com`**, con
HTTPS automatico (Let's Encrypt gestito da Vercel).

### Passi (una tantum)

1. **Aggiungi il dominio al progetto Vercel**
   - Vercel → progetto → **Settings → Domains → Add**
   - Inserisci `formule-in-movimento.celata.com`
   - In alternativa via CLI: `npx vercel domains add formule-in-movimento.celata.com`

2. **Crea il record DNS su `celata.com`** (presso il gestore DNS del dominio).
   Per un sottodominio, Vercel chiede un record **CNAME**:

   | Tipo  | Nome (host)            | Valore                  |
   |-------|------------------------|-------------------------|
   | CNAME | `formule-in-movimento` | `cname.vercel-dns.com.` |

   > Vercel mostra il valore esatto da usare nella schermata "Add Domain":
   > usa quello indicato lì se differisce (di norma è `cname.vercel-dns.com`).

3. **Attendi la verifica.** Vercel rileva il record, verifica il dominio ed
   emette automaticamente il certificato TLS. Da quel momento il sito è
   raggiungibile su `https://formule-in-movimento.celata.com`.

## 4. Manutenzione / Cleanup

Nel tempo si accumulano artefatti che conviene ripulire periodicamente.

### Deployment Vercel

Ogni run del workflow crea un nuovo deployment. Solo l'ultimo è in produzione;
i precedenti restano come storico/preview.

- **Dashboard**: progetto → **Deployments** → menu `…` su un deployment →
  **Delete**.
- **CLI** (rimuove i deployment più vecchi mantenendo quello in produzione):

  ```bash
  cd frontend
  npx vercel ls                       # elenca i deployment
  npx vercel remove <nome-progetto> --safe --yes
  # --safe non rimuove i deployment associati ad alias/produzione
  ```

### Artifact e cache di GitHub Actions

- Gli **artifact** del workflow hanno già `retention-days: 1` e scadono da soli.
- Le **cache** `media-*` possono accumularsi (una per animazione × qualità). Da
  **Actions → Caches** si possono eliminare quelle vecchie, oppure via GitHub
  CLI:

  ```bash
  gh cache list
  gh cache delete <id>        # oppure: gh cache delete --all
  ```

  Eliminare una cache forza solo una rigenerazione al prossimo run (più lento,
  nessun altro effetto).

### Branch git già mergiati

Dopo il merge di una PR, il relativo branch può essere cancellato:

```bash
# Singolo branch remoto
git push origin --delete <nome-branch>

# Pota i riferimenti locali a branch remoti ormai assenti
git fetch --prune
```

In alternativa, dalla pagina della PR su GitHub c'è il pulsante
**"Delete branch"**, e in *Settings → General* si può attivare
**"Automatically delete head branches"** per cancellarli in automatico al merge.

## 5. Sviluppo locale (senza deploy)

```bash
make <topic> QUALITY=ql     # genera un'animazione in bassa qualità (veloce)
make frontend-dev           # frontend con hot reload su http://localhost:4321
make frontend-build         # build statica in frontend/dist/
```

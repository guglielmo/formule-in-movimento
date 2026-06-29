# Deploy & Manutenzione

Il sito **Formule in Movimento** è statico e viene pubblicato su **Vercel**
tramite **GitHub Actions**. Questo è l'unico processo di deploy supportato.

> Perché non l'integrazione Git nativa di Vercel? Perché Vercel non può eseguire
> Manim/LaTeX per generare i video. I video vengono quindi prebuildati in CI e
> caricati su Vercel già pronti, usando la Vercel CLI.

## 1. Come fare un deploy

Il workflow `.github/workflows/genera-animazioni.yml` decide cosa fare in base
all'evento:

| Evento | Deploy | Qualità |
|---|---|---|
| **push/merge su `main`** | **produzione** (`vercel deploy --prod`, aggiorna `formule-in-movimento.celata.com`) | `qh` |
| **push su un altro branch** | **preview**, raggiungibile sull'alias stabile `anteprima.formule-in-movimento.celata.com` (oltre all'URL temporaneo) | `ql` |
| **avvio manuale** (*Actions → Run workflow*) | a scelta via input `target` | a scelta via input `quality` |

In breve: si lavora su un branch (ogni push genera una **preview** da riguardare
sempre allo stesso indirizzo, vedi §3.1; l'URL è anche nel *Summary* della run);
quando si **mergia in `main`** il sito va in **produzione** in qualità di
pubblicazione `qh`.

Fasi del workflow:

1. **setup** — determina qualità e ambiente in base all'evento.
2. **discover** — scopre le animazioni (auto-discovery, come il Makefile).
3. **build** — genera ogni animazione con `make <topic>`. Usa una cache basata
   sull'hash dei sorgenti: rigenera **solo** ciò che è cambiato; in cache-hit
   non rirenderizza e non scarica nemmeno l'immagine. In cache-miss il rendering
   gira **dentro l'immagine CI** con Manim/LaTeX preinstallati (vedi §2.2).
4. **deploy** — `make frontend-build`, include i video nella `dist/` e pubblica
   su Vercel. I domini sono assegnati con **alias espliciti** (`vercel alias
   set`) e l'assegnazione automatica è disattivata (`--skip-domain` in
   produzione), così produzione e anteprima non si contendono i domini
   (vedi §3 e §3.1).

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
come `ghcr.io/guglielmo/formule-in-movimento-ci:<hash>` (definizione in
`docker/Dockerfile.ci`).

L'immagine è gestita dal job **`ci-image`** dentro lo stesso workflow di deploy,
in modo **auto-bootstrap**:

- il tag è l'hash di `docker/Dockerfile.ci` + `requirements.txt`;
- a ogni run il job controlla se l'immagine per quell'hash esiste già su GHCR:
  se sì la riusa, se no la costruisce e la pubblica (succede solo la prima volta
  o quando cambiano Dockerfile/requirements);
- i job di build dipendono da `ci-image`, quindi non serve nessun passo manuale
  e non c'è rischio che renderizzino prima che l'immagine sia pronta.

Il rendering usa l'immagine solo in **cache-miss**: se i sorgenti di
un'animazione non cambiano, non viene renderizzata.

> Le vecchie immagini taggate per hash si accumulano su GHCR: ogni tanto si
> possono eliminare le versioni non più usate dalla pagina *Packages* del repo.

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

> **Come viene assegnato il dominio.** Il workflow deploya la produzione con
> `vercel deploy --prod --skip-domain` e poi assegna il dominio esplicitamente
> con `vercel alias set`. Questo serve a non far "rubare" l'alias dell'anteprima
> dai deploy di produzione (vedi §3.1). Effetto collaterale: il dominio di
> default `*.vercel.app` di produzione **non** si auto-aggiorna; l'indirizzo
> canonico di produzione è `formule-in-movimento.celata.com`.

### 3.1 Anteprima stabile: anteprima.formule-in-movimento.celata.com

I deploy di **preview** (push su un branch ≠ `main`) ricevono un URL temporaneo
diverso a ogni run; per avere **sempre lo stesso indirizzo** il workflow assegna
all'ultimo preview l'alias `anteprima.formule-in-movimento.celata.com`
(`vercel alias set …`). Vale "**l'ultimo preview vince**": con più branch aperti
contemporaneamente, l'alias punta all'anteprima deployata più di recente (gli
altri restano raggiungibili al loro URL con hash).

Poiché la produzione usa `--skip-domain` (vedi §3), un merge in `main` **non**
ri-aggancia questo dominio alla produzione: l'anteprima resta puntata all'ultimo
preview.

Configurazione **una tantum**, identica alla produzione:

1. Aggiungi il dominio al progetto Vercel: **Settings → Domains → Add** →
   `anteprima.formule-in-movimento.celata.com` (o
   `npx vercel domains add anteprima.formule-in-movimento.celata.com`).
2. Crea il record DNS su `celata.com` (usa il valore mostrato da Vercel):

   | Tipo  | Nome (host)                       | Valore                  |
   |-------|-----------------------------------|-------------------------|
   | CNAME | `anteprima.formule-in-movimento`  | `cname.vercel-dns.com.` |

3. Attendi la verifica: HTTPS automatico, e da lì lo step `vercel alias set` del
   workflow potrà puntarci i preview.

> Finché il dominio non è aggiunto/verificato su Vercel, lo step `vercel alias
> set` non riesce ad assegnare l'alias, ma **non fa fallire** il workflow (emette
> solo un warning) e il preview resta raggiungibile al suo URL temporaneo. Una
> volta configurato il dominio, l'alias inizia a funzionare da solo.

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

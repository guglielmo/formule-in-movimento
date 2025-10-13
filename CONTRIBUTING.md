# Contributing to Formule in Movimento

Grazie per il tuo interesse nel contribuire a **Formule in Movimento**! Questo progetto mira a rendere la matematica e la fisica più accessibili agli studenti attraverso animazioni educative ottimizzate per dispositivi mobili.

## Come Contribuire

### Tipi di Contributi

Accettiamo diversi tipi di contributi:

- **Nuove animazioni**: Crea animazioni per nuovi concetti matematici o fisici
- **Miglioramenti alle animazioni esistenti**: Ottimizza la qualità, la chiarezza o la durata
- **Correzioni di bug**: Risolvi errori nel codice o nelle animazioni
- **Documentazione**: Migliora README, guide o commenti nel codice
- **Traduzioni**: Attualmente il progetto è solo in italiano (non accettiamo traduzioni in altre lingue per mantenere la coerenza del target)
- **Design web**: Migliora le pagine HTML e il design responsive

### Prima di Iniziare

1. **Leggi il README.md** per comprendere gli obiettivi del progetto
2. **Leggi il CLAUDE.md** per le convenzioni tecniche e lo stile di sviluppo
3. **Esplora le animazioni esistenti** in `animations/matematica/` e `animations/fisica/`
4. **Controlla le Issues** su GitHub per vedere se qualcuno sta già lavorando su qualcosa di simile

## Linee Guida per le Animazioni

### Requisiti Tecnici

Tutte le animazioni devono rispettare questi requisiti:

- **Tema chiaro obbligatorio**: `self.camera.background_color = WHITE`
- **Colori scuri**: Usa `BLACK`, `DARK_BLUE`, `RED_D`, `GREEN_D`, `BLUE_D`, `DARK_GRAY`
- **Lingua italiana**: Tutti i testi, etichette e titoli devono essere in italiano
- **Durata**: 30-90 secondi ideali per i social media (max 2 minuti)
- **Font leggibili**: Dimensioni adeguate per la visualizzazione su mobile (min 28pt per testi secondari, 44pt+ per titoli)

### Qualità dei Contenuti

- **Accuratezza**: Le informazioni devono essere matematicamente/fisicamente corrette
- **Chiarezza**: Usa un linguaggio semplice e accessibile agli studenti
- **Progressività**: Costruisci i concetti passo dopo passo
- **Intuizione visiva**: Privilegia la comprensione visiva rispetto alle dimostrazioni formali
- **Transizioni fluide**: Usa animazioni morbide e graduali

### Struttura delle Cartelle

Quando crei una nuova animazione:

```
animations/
└── [disciplina]/          # matematica/ o fisica/
    └── [argomento]/        # es: derivate/, termodinamica/
        ├── [nome].py       # File Python con le scene Manim
        ├── index.html      # Pagina web per l'animazione
        └── media/          # Generato automaticamente da Manim
```

## Processo di Contribuzione

### 1. Fork e Clone

```bash
# Fork il repository su GitHub, poi:
git clone https://github.com/TUO_USERNAME/formule-in-movimento.git
cd formule-in-movimento
```

### 2. Setup Ambiente

```bash
# Crea virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# oppure
.venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt
```

### 3. Crea un Branch

```bash
# Usa un nome descrittivo
git checkout -b matematica/derivate-funzioni
# oppure
git checkout -b fix/colore-sfondo-errore
```

### 4. Sviluppa la Tua Animazione

```bash
# Crea la directory
mkdir -p animations/matematica/nuovo_argomento
cd animations/matematica/nuovo_argomento

# Crea il file Python
# [scrivi il codice seguendo le convenzioni]

# Testa con preview veloce
manim -pql tuo_file.py TuaScena

# Quando sei soddisfatto, renderizza in alta qualità
manim -pqh tuo_file.py TuaScena
```

### 5. Crea la Pagina HTML

Crea un file `index.html` nella stessa directory dell'animazione:

- Usa un design responsive e mobile-first
- Includi una descrizione chiara del concetto in italiano
- Incorpora il video renderizzato
- Aggiungi pulsanti di condivisione social
- Mantieni coerenza con lo stile delle altre pagine

### 6. Testa su Dispositivi Mobili

- Verifica che il video sia visibile e leggibile su smartphone
- Testa i pulsanti e l'interfaccia touch
- Controlla i tempi di caricamento

### 7. Commit e Push

```bash
# Aggiungi i file
git add .

# Commit con messaggio descrittivo
git commit -m "Aggiungi animazione sulle derivate delle funzioni composte

- Implementa regola della catena con esempio visivo
- Durata: 75 secondi
- Renderizzato in 1080p e 9:16 per social media"

# Push al tuo fork
git push origin matematica/derivate-funzioni
```

### 8. Crea una Pull Request

1. Vai al repository originale su GitHub
2. Clicca su "New Pull Request"
3. Seleziona il tuo branch
4. Descrivi chiaramente le modifiche
5. Includi screenshot o link al video se possibile

## Standard di Codice

### Python / Manim

```python
from manim import *

class NomeScenaPascalCase(Scene):
    """Descrizione breve della scena in italiano."""

    def construct(self):
        # Tema chiaro obbligatorio
        self.camera.background_color = WHITE

        # Usa colori scuri per la visibilità
        title = Text("Titolo in Italiano", font_size=44, color=BLACK)

        # Animazioni fluide e chiare
        self.play(Write(title))
        self.wait(1)

        # Commenti in italiano per spiegare passaggi complessi
        # [resto del codice...]
```

### HTML

- HTML5 valido e semantico
- Design responsive con CSS moderno
- Compatibilità con browser mobili (iOS Safari, Chrome Android)
- Accessibilità (alt text, ARIA labels)
- Performance ottimizzata (lazy loading video, immagini compresse)

## Revisione

Tutti i contributi passano attraverso una revisione. Potremmo chiederti di:

- Modificare colori per migliorare il contrasto
- Regolare la velocità delle animazioni
- Semplificare il linguaggio
- Ottimizzare la durata del video
- Migliorare la responsività mobile

Siamo qui per aiutarti a migliorare il contributo, non per criticare!

## Domande?

Se hai domande o dubbi:

1. Controlla prima CLAUDE.md e README.md
2. Cerca nelle Issues esistenti
3. Apri una nuova Issue con tag [question]

## Codice di Condotta

- Sii rispettoso e costruttivo
- Concentrati sul contenuto educativo e sulla qualità
- Accetta i feedback con spirito di miglioramento
- Aiuta gli altri contributor quando possibile

## Licenza

Contribuendo a questo progetto, accetti che i tuoi contributi siano rilasciati sotto la [Apache License 2.0](LICENSE).

---

**Grazie per aiutarci a rendere la matematica e la fisica più accessibili a tutti gli studenti!** 🎓📱

**Formule in Movimento** - Porta la conoscenza nel palmo della mano.

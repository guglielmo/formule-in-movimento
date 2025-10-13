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
- **Matematica**: Algebra, geometria, trigonometria, analisi, calcolo
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
├── index.html                          # Landing page principale
├── animations/                         # Animazioni organizzate per disciplina
│   ├── matematica/                     # Sezione matematica
│   │   └── [argomento]/
│   │       ├── [nome].py              # Scene Manim
│   │       ├── index.html             # Pagina HTML dell'animazione
│   │       └── media/                 # Video renderizzati
│   └── fisica/                        # Sezione fisica
│       └── [argomento]/
│           ├── [nome].py
│           ├── index.html
│           └── media/
├── requirements.txt                    # Dipendenze Python
├── .python-version                     # Versione Python (3.12)
├── .venv/                             # Virtual environment Python
└── CLAUDE.md                          # Linee guida per lo sviluppo
```

## Setup Rapido

### Prerequisiti
- Python 3.12+
- LaTeX (TeX Live su Linux, MiKTeX su Windows, MacTeX su macOS)
- Browser moderno per preview

### Installazione

```bash
# Clona/naviga nella directory del progetto
cd formule-in-movimento

# Crea e attiva virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# oppure
.venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt
```

### Creare una Nuova Animazione

```bash
# 1. Crea directory per l'argomento
mkdir -p animations/matematica/nuovo_argomento

# 2. Naviga nella directory
cd animations/matematica/nuovo_argomento

# 3. Crea il file Python con le scene Manim
# (segui le convenzioni in CLAUDE.md)

# 4. Renderizza l'animazione
manim -pql nome_file.py NomeScena

# 5. Crea index.html per la pagina web
# 6. Aggiorna index.html principale con il link
```

## Comandi Comuni

### Renderizzare Video

```bash
# Preview veloce (bassa qualità)
manim -pql file.py SceneName

# Alta qualità per pubblicazione
manim -pqh file.py SceneName

# Formato verticale (9:16) per social
manim -pqh file.py SceneName --resolution 1080,1920

# Lista tutte le scene nel file
manim file.py --list
```

### Qualità Disponibili
- `-ql`: 480p, 15fps (preview veloce)
- `-qm`: 720p, 30fps (media qualità)
- `-qh`: 1080p, 60fps (alta qualità, consigliata)
- `-qk`: 4K, 60fps (massima qualità)

## Tecnologie Utilizzate

- **Manim Community Edition**: Libreria Python per animazioni matematiche
- **Python 3.12**: Linguaggio di programmazione
- **LaTeX**: Rendering di formule matematiche
- **HTML5/CSS3**: Pagine web responsive
- **Git**: Version control

## Contribuire

Contributi di ogni tipo sono benvenuti! Consulta [CONTRIBUTING.md](CONTRIBUTING.md) per le linee guida su come contribuire al progetto.

Per dettagli tecnici sullo sviluppo, vedi [CLAUDE.md](CLAUDE.md).

## Licenza

Questo progetto è rilasciato sotto [Apache License 2.0](LICENSE).

Copyright 2025 Guglielmo Celata

## Contatti

[Da definire]

---

**Formule in Movimento** - Porta la matematica e la fisica nel palmo della mano degli studenti.

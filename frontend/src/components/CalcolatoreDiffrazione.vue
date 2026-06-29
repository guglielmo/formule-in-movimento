<script setup>
import { ref, computed } from 'vue';

// Colori della luce visibile con lunghezza d'onda rappresentativa (nm)
const colori = [
  { nome: 'Violetto', lambda: 410, hex: '#7a00cc' },
  { nome: 'Blu',      lambda: 460, hex: '#1f4fff' },
  { nome: 'Verde',    lambda: 530, hex: '#15a83a' },
  { nome: 'Giallo',   lambda: 580, hex: '#e6b400' },
  { nome: 'Arancio',  lambda: 610, hex: '#ff7a00' },
  { nome: 'Rosso',    lambda: 680, hex: '#e01515' },
];

const modo = ref('L');                // 'L' = trova distanza schermo; 'dy' = trova spaziatura frange
const selezionato = ref(colori[2]);   // Verde di default
const d_mm = ref(0.20);               // distanza tra le fenditure (mm) - condivisa
const dy_mm = ref(2.0);               // spaziatura frange desiderata (mm) - modo 'L'
const L_m_in = ref(1.5);              // distanza schermo (m) - modo 'dy'

const lambda_m = computed(() => selezionato.value.lambda * 1e-9);
const d_m = computed(() => d_mm.value * 1e-3);

// Modo 'L':  L = Δy · d / λ
const L_calc = computed(() => (dy_mm.value * 1e-3 * d_m.value) / lambda_m.value);
// Modo 'dy': Δy = λ · L / d   (in mm)
const dy_calc = computed(() => (lambda_m.value * L_m_in.value / d_m.value) * 1e3);

// Spaziatura frange "effettiva" (input nel modo L, calcolata nel modo dy)
const dy_eff = computed(() => (modo.value === 'L' ? dy_mm.value : dy_calc.value));

const L_testo = computed(() => {
  const L = L_calc.value;
  return L < 1 ? (L * 100).toFixed(0) + ' cm' : L.toFixed(2) + ' m';
});
const dy_testo = computed(() => {
  const dy = dy_calc.value;
  return dy < 1 ? dy.toFixed(2) + ' mm' : dy.toFixed(1) + ' mm';
});

const verdetto = computed(() => {
  if (modo.value === 'L') {
    const L = L_calc.value;
    if (L <= 3) return { testo: "Realizzabile in un'aula o in laboratorio", classe: 'ok' };
    if (L <= 10) return { testo: 'Serve una stanza molto lunga', classe: 'warn' };
    return { testo: 'Poco pratico: servono fenditure più vicine', classe: 'bad' };
  } else {
    const dy = dy_calc.value;
    if (dy >= 2) return { testo: 'Frange ben visibili a occhio', classe: 'ok' };
    if (dy >= 1) return { testo: 'Frange visibili', classe: 'ok' };
    if (dy >= 0.5) return { testo: 'Appena distinguibili', classe: 'warn' };
    return { testo: 'Troppo fitte: non distinguibili a occhio', classe: 'bad' };
  }
});

// --- Anteprima in scala reale (righello in mm) ---
const UPM = 20;     // unità SVG per millimetro
const HALF = 6;     // mezza larghezza del righello in mm (da -6 a +6)
const CX = 120;     // centro in unità SVG (larghezza viewBox = 240)

const ticks = computed(() => {
  const t = [];
  for (let mm = -HALF; mm <= HALF; mm++) t.push({ x: CX + mm * UPM, mm });
  return t;
});
const labelTicks = computed(() => ticks.value.filter((t) => t.mm % 2 === 0));
const frangeReali = computed(() => {
  const out = [];
  const dy = dy_eff.value;
  if (!(dy > 0)) return out;
  const mMax = Math.min(90, Math.floor(HALF / dy));
  for (let m = -mMax; m <= mMax; m++) {
    out.push({
      x: CX + m * dy * UPM,
      op: m === 0 ? 1 : Math.max(0.22, 1 - Math.abs(m) * 0.16),
    });
  }
  return out;
});
</script>

<template>
  <div class="calc">
    <h3 class="calc-title">Quanto contano le distanze reali?</h3>

    <!-- Selettore modalità -->
    <div class="modi">
      <button class="modo" :class="{ attivo: modo === 'L' }" @click="modo = 'L'">
        Trova la distanza schermo (L)
      </button>
      <button class="modo" :class="{ attivo: modo === 'dy' }" @click="modo = 'dy'">
        Trova la spaziatura frange (Δy)
      </button>
    </div>

    <p class="calc-intro">
      Relazione fondamentale: <strong>Δy = λL/d</strong>. Scegli il
      <strong>colore</strong> (lunghezza d'onda λ); poi, a fenditure fisse,
      <template v-if="modo === 'L'">
        imposta la spaziatura di frange che vuoi vedere e ottieni la distanza dello schermo.
      </template>
      <template v-else>
        imposta la distanza dello schermo e ottieni la spaziatura delle frange.
      </template>
    </p>

    <!-- Selettore colore (condiviso) -->
    <div class="riga">
      <label class="etichetta">Colore (λ)</label>
      <div class="colori">
        <button
          v-for="c in colori"
          :key="c.nome"
          class="chip"
          :class="{ attivo: c.nome === selezionato.nome }"
          :style="{ '--c': c.hex }"
          @click="selezionato = c"
        >
          {{ c.nome }}<small>{{ c.lambda }} nm</small>
        </button>
      </div>
    </div>

    <!-- Distanza fenditure (condivisa) -->
    <div class="riga">
      <label class="etichetta">
        Distanza tra le fenditure <strong>d</strong>: {{ d_mm.toFixed(2) }} mm
      </label>
      <input type="range" min="0.05" max="1.0" step="0.01" v-model.number="d_mm" />
    </div>

    <!-- Input dipendente dalla modalità -->
    <div class="riga" v-if="modo === 'L'">
      <label class="etichetta">
        Spaziatura frange desiderata <strong>Δy</strong>: {{ dy_mm.toFixed(1) }} mm
      </label>
      <input type="range" min="0.5" max="5.0" step="0.1" v-model.number="dy_mm" />
    </div>
    <div class="riga" v-else>
      <label class="etichetta">
        Distanza dello schermo <strong>L</strong>: {{ L_m_in.toFixed(2) }} m
      </label>
      <input type="range" min="0.2" max="5.0" step="0.05" v-model.number="L_m_in" />
    </div>

    <!-- Risultato -->
    <div class="risultato">
      <div class="out-valore" v-if="modo === 'L'">
        Distanza schermo: <span class="out-num">{{ L_testo }}</span>
      </div>
      <div class="out-valore" v-else>
        Spaziatura frange: <span class="out-num">{{ dy_testo }}</span>
      </div>
      <div class="formula" v-if="modo === 'L'">
        L = Δy · d / λ = {{ dy_mm.toFixed(1) }} mm · {{ d_mm.toFixed(2) }} mm / {{ selezionato.lambda }} nm
      </div>
      <div class="formula" v-else>
        Δy = λ · L / d = {{ selezionato.lambda }} nm · {{ L_m_in.toFixed(2) }} m / {{ d_mm.toFixed(2) }} mm
      </div>
      <div class="verdetto" :class="verdetto.classe">{{ verdetto.testo }}</div>
    </div>

    <!-- Anteprima delle frange in scala reale (righello in mm) -->
    <div class="scala-wrap">
      <div class="scala-tit">Anteprima sullo schermo — scala reale (mm)</div>
      <svg class="scala" viewBox="0 0 240 78" preserveAspectRatio="xMidYMid meet">
        <rect x="0" y="0" width="240" height="56" rx="4" fill="#1a1a1a" />
        <!-- frange chiare alla loro vera posizione -->
        <rect
          v-for="(f, idx) in frangeReali"
          :key="'f' + idx"
          :x="f.x - 2"
          y="6"
          width="4"
          height="44"
          rx="1.2"
          :fill="selezionato.hex"
          :opacity="f.op"
        />
        <!-- tacche del righello -->
        <g stroke="#777" stroke-width="0.8">
          <line
            v-for="(t, idx) in ticks"
            :key="'t' + idx"
            :x1="t.x"
            y1="58"
            :x2="t.x"
            :y2="t.mm % 2 === 0 ? 66 : 62"
          />
        </g>
        <!-- etichette in mm -->
        <g fill="#555" font-size="7" text-anchor="middle">
          <text v-for="(t, idx) in labelTicks" :key="'l' + idx" :x="t.x" y="76">{{ t.mm }}</text>
        </g>
      </svg>
    </div>

    <p class="nota">
      Con la luce visibile (λ ≈ 0,4–0,7 µm) e fenditure molto vicine
      (d ≈ 0,1–0,5 mm) basta uno schermo a pochi metri. Se le fenditure fossero
      distanti 1 cm servirebbe uno schermo a decine di metri: per questo devono
      essere strettissime. Nota anche che il <strong>rosso</strong> (λ grande) dà
      frange più larghe del <strong>violetto</strong> a parità di L e d.
    </p>
  </div>
</template>

<style scoped>
.calc {
  border: 1px solid #e2e2e2;
  border-left: 4px solid #3498db;
  border-radius: 10px;
  padding: 20px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin: 20px 0;
}
.calc-title {
  margin: 0 0 12px;
  color: #2c3e50;
}
.modi {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}
.modo {
  flex: 1 1 200px;
  padding: 10px 12px;
  border: 2px solid #3498db;
  border-radius: 8px;
  background: #fff;
  color: #2c3e50;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9em;
  transition: all 0.15s ease;
}
.modo.attivo {
  background: #3498db;
  color: #fff;
}
.calc-intro,
.nota {
  color: #555;
  line-height: 1.5;
  font-size: 0.95em;
}
.nota {
  margin-top: 16px;
  font-size: 0.88em;
  color: #666;
}
.riga {
  margin: 16px 0;
}
.etichetta {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-size: 0.95em;
}
.colori {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 8px 12px;
  border: 2px solid var(--c);
  border-radius: 8px;
  background: #fff;
  color: #333;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9em;
  transition: all 0.15s ease;
}
.chip small {
  font-weight: 400;
  font-size: 0.78em;
  color: #888;
}
.chip.attivo {
  background: var(--c);
  color: #fff;
}
.chip.attivo small {
  color: rgba(255, 255, 255, 0.85);
}
input[type='range'] {
  width: 100%;
  accent-color: #3498db;
}
.risultato {
  margin-top: 18px;
  padding: 16px;
  background: #f5f9ff;
  border-radius: 8px;
  text-align: center;
}
.out-valore {
  font-size: 1.1em;
  color: #2c3e50;
}
.out-num {
  font-size: 1.5em;
  font-weight: 700;
  color: #2563eb;
}
.formula {
  margin-top: 8px;
  font-size: 0.85em;
  color: #777;
}
.verdetto {
  margin-top: 10px;
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9em;
}
.verdetto.ok {
  background: #e3f6e8;
  color: #1c7c3a;
}
.verdetto.warn {
  background: #fff3da;
  color: #9a6b00;
}
.verdetto.bad {
  background: #fde2e2;
  color: #b42323;
}
.scala-wrap {
  margin-top: 18px;
}
.scala-tit {
  font-size: 0.82em;
  color: #777;
  margin-bottom: 6px;
  text-align: center;
}
.scala {
  width: 100%;
  height: auto;
  display: block;
}
</style>

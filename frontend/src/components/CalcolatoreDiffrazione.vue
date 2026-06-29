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

const selezionato = ref(colori[2]);   // Verde di default
const d_mm = ref(0.20);               // distanza tra le fenditure (mm) - fissa/regolabile
const dy_mm = ref(2.0);               // spaziatura delle frange desiderata (mm)

// L = Δy · d / λ   (formula della doppia fenditura: Δy = λL/d)
const L_m = computed(() => {
  const lambda_m = selezionato.value.lambda * 1e-9;
  const d_m = d_mm.value * 1e-3;
  const dy_m = dy_mm.value * 1e-3;
  return (dy_m * d_m) / lambda_m;
});

const L_testo = computed(() => {
  const L = L_m.value;
  if (L < 1) return (L * 100).toFixed(0) + ' cm';
  return L.toFixed(2) + ' m';
});

// Giudizio pratico sulla distanza dello schermo
const verdetto = computed(() => {
  const L = L_m.value;
  if (L <= 3) return { testo: "Realizzabile in un'aula o in laboratorio", classe: 'ok' };
  if (L <= 10) return { testo: 'Serve una stanza molto lunga', classe: 'warn' };
  return { testo: 'Poco pratico: servono fenditure più vicine', classe: 'bad' };
});

// Anteprima delle frange (bande chiare nel colore scelto, su fondo scuro)
const frange = computed(() => {
  const bande = [];
  for (let i = -4; i <= 4; i++) bande.push(i);
  return bande;
});
</script>

<template>
  <div class="calc">
    <h3 class="calc-title">Quanto lontano deve stare lo schermo?</h3>
    <p class="calc-intro">
      Per <strong>vedere</strong> le frange, la loro spaziatura
      <strong>Δy</strong> deve essere di qualche millimetro. Scegli il
      <strong>colore</strong> (la lunghezza d'onda λ) e regola i parametri:
      a fenditure fisse, lo schermo va messo a distanza
      <strong>L = Δy · d / λ</strong>.
    </p>

    <!-- Selettore colore -->
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

    <!-- Slider distanza fenditure -->
    <div class="riga">
      <label class="etichetta">
        Distanza tra le fenditure <strong>d</strong>: {{ d_mm.toFixed(2) }} mm
      </label>
      <input type="range" min="0.05" max="1.0" step="0.01" v-model.number="d_mm" />
    </div>

    <!-- Slider spaziatura frange desiderata -->
    <div class="riga">
      <label class="etichetta">
        Spaziatura frange desiderata <strong>Δy</strong>: {{ dy_mm.toFixed(1) }} mm
      </label>
      <input type="range" min="0.5" max="5.0" step="0.1" v-model.number="dy_mm" />
    </div>

    <!-- Risultato -->
    <div class="risultato">
      <div class="L-valore">
        Distanza schermo: <span class="L-num">{{ L_testo }}</span>
      </div>
      <div class="formula">
        L = Δy · d / λ = {{ dy_mm.toFixed(1) }} mm · {{ d_mm.toFixed(2) }} mm / {{ selezionato.lambda }} nm
      </div>
      <div class="verdetto" :class="verdetto.classe">{{ verdetto.testo }}</div>
    </div>

    <!-- Anteprima frange nel colore scelto -->
    <div class="frange" aria-hidden="true">
      <div
        v-for="i in frange"
        :key="i"
        class="banda"
        :style="{ background: selezionato.hex, opacity: i === 0 ? 1 : Math.max(0.2, 1 - Math.abs(i) * 0.18) }"
      ></div>
    </div>

    <p class="nota">
      Con la luce visibile (λ ≈ 0,4–0,7 µm) e fenditure molto vicine
      (d ≈ 0,1–0,5 mm) bastano pochi metri. Ma se le fenditure fossero distanti
      1 cm servirebbe uno schermo a decine di metri: ecco perché le fenditure
      devono essere strettissime. Nota anche che, a parità di tutto, il
      <strong>rosso</strong> (λ grande) richiede uno schermo più vicino del
      <strong>violetto</strong>.
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
  margin: 0 0 8px;
  color: #2c3e50;
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
.L-valore {
  font-size: 1.1em;
  color: #2c3e50;
}
.L-num {
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
.frange {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 18px;
  padding: 14px;
  background: #1a1a1a;
  border-radius: 8px;
}
.banda {
  width: 14px;
  height: 46px;
  border-radius: 3px;
}
@media (max-width: 520px) {
  .banda { width: 10px; height: 38px; }
}
</style>

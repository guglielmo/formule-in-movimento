# Copyright 2025–2026 Guglielmo Celata
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from manim import *
import sys, os
import numpy as np

# Rende importabile il package condiviso 'animations' (template, moduli, ...)
# calcolando la root del progetto: niente path hardcoded, funziona in locale e in CI.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from animations.vertical_template import VerticalTemplate


# ============================================================================
# Helper comuni
# ============================================================================

# Larghezza utile del frame verticale (frame_width = 8.0) con piccoli margini.
USABLE_W = 7.2


def fit(mobj, max_w=USABLE_W):
    """Rimpicciolisce un mobject se supera la larghezza utile del frame."""
    if mobj.width > max_w:
        mobj.scale_to_fit_width(max_w)
    return mobj


def titolo(testo, sottotitolo=None):
    """Crea un titolo (e sottotitolo) standard in alto, tema chiaro."""
    t = Text(testo, font_size=40, color=BLACK, weight=BOLD)
    fit(t)
    t.to_edge(UP, buff=0.3)
    if sottotitolo:
        s = Text(sottotitolo, font_size=26, color=DARK_BLUE)
        fit(s)
        s.next_to(t, DOWN, buff=0.2)
        return VGroup(t, s)
    return VGroup(t)


# ============================================================================
# 1. SOMMA DI ONDE: principio di sovrapposizione
# ============================================================================

class SommaDiOnde(Scene):
    """Quando due onde si incontrano, gli spostamenti si sommano."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Somma di onde", "Principio di sovrapposizione")
        self.play(Write(intestazione))
        self.wait(0.3)

        k = 2.0
        A = 0.6
        phi = PI / 3  # sfasamento tra le due onde

        w1 = FunctionGraph(lambda x: A * np.sin(k * x),
                           x_range=[-3.4, 3.4, 0.02], color=BLUE_D, stroke_width=4).move_to(UP * 3.3)
        lab1 = fit(MathTex(r"y_1", color=BLUE_D, font_size=34)).next_to(w1, UP, buff=0.1)

        w2 = FunctionGraph(lambda x: A * np.sin(k * x + phi),
                           x_range=[-3.4, 3.4, 0.02], color=GREEN_D, stroke_width=4).move_to(UP * 1.1)
        lab2 = fit(MathTex(r"y_2", color=GREEN_D, font_size=34)).next_to(w2, UP, buff=0.1)

        somma = FunctionGraph(lambda x: A * np.sin(k * x) + A * np.sin(k * x + phi),
                              x_range=[-3.4, 3.4, 0.02], color=RED_D, stroke_width=6).move_to(DOWN * 1.6)
        lab_s = fit(MathTex(r"y = y_1 + y_2", color=RED_D, font_size=38)).next_to(somma, UP, buff=0.15)

        self.play(Create(w1), Write(lab1))
        self.play(Create(w2), Write(lab2))
        self.wait(0.3)
        self.play(TransformFromCopy(VGroup(w1, w2), somma), Write(lab_s), run_time=2)

        nota = VGroup(
            Text("Gli spostamenti si sommano", font_size=24, color=BLACK),
            Text("punto per punto", font_size=24, color=BLACK),
        ).arrange(DOWN, buff=0.15)
        fit(nota)
        nota.move_to(DOWN * 4.6)
        self.play(FadeIn(nota))
        self.wait(1.5)


# ============================================================================
# 2. L'EFFETTO DELLA FASE: ampiezza risultante in funzione di Δφ
# ============================================================================

class EffettoFase(VerticalTemplate):
    """La risultante dipende dallo sfasamento Δφ tra le due onde."""

    def construct(self):
        self.setup_vertical_layout(
            title_text="L'effetto della fase",
            subtitle_text="due onde sovrapposte",
        )
        fit(self.title)
        fit(self.subtitle)

        dphi = ValueTracker(0)
        k = 2.0
        A = 0.55
        cy_top = self.top_block_center
        cy_bot = self.bottom_block_center

        # Blocco alto: le due onde sovrapposte (una fissa, una sfasata)
        w1 = FunctionGraph(lambda x: A * np.sin(k * x),
                           x_range=[-3.4, 3.4, 0.02], color=BLUE_D, stroke_width=4).move_to(UP * cy_top)
        w2 = always_redraw(lambda: FunctionGraph(
            lambda x: A * np.sin(k * x + dphi.get_value()),
            x_range=[-3.4, 3.4, 0.02], color=GREEN_D, stroke_width=4).move_to(UP * cy_top))
        lab_top = fit(Text("due onde uguali, sfasate di Δφ", font_size=22, color=DARK_GRAY))
        lab_top.move_to([0, cy_top + 1.7, 0])

        # Blocco basso: la risultante
        res = always_redraw(lambda: FunctionGraph(
            lambda x: A * np.sin(k * x) + A * np.sin(k * x + dphi.get_value()),
            x_range=[-3.4, 3.4, 0.02], color=RED_D, stroke_width=6).move_to(UP * cy_bot))
        lab_bot = fit(Text("risultante", font_size=22, color=RED_D))
        lab_bot.move_to([0, cy_bot + 1.7, 0])

        # Lettura di Δφ (DecimalNumber: niente ricompilazione LaTeX per frame)
        dlbl = MathTex(r"\Delta\varphi =", color=BLACK, font_size=32)
        dnum = DecimalNumber(0, num_decimal_places=2, color=BLACK, font_size=32)
        drad = MathTex(r"\mathrm{rad}", color=BLACK, font_size=32)
        dgrp = VGroup(dlbl, dnum, drad).arrange(RIGHT, buff=0.12)
        dgrp.move_to([0, 0.1, 0])
        dnum.add_updater(lambda m: m.set_value(dphi.get_value()))

        self.play(Create(w1))
        self.add(w2)
        self.play(FadeIn(lab_top))
        self.add(res)
        self.play(FadeIn(lab_bot), FadeIn(dgrp))
        self.play(dphi.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        dnum.clear_updaters()
        self.wait(1)


# ============================================================================
# 3. INTERFERENZA: costruttiva o distruttiva
# ============================================================================

class CostruttivaDistruttiva(VerticalTemplate):
    """Onde in fase si rinforzano; in opposizione si annullano."""

    def construct(self):
        self.setup_vertical_layout(
            title_text="Costruttiva o distruttiva",
            subtitle_text="rinforzo o annullamento",
        )
        fit(self.title)
        fit(self.subtitle)

        k = 2.0
        A = 0.45
        cy_top = self.top_block_center
        cy_bot = self.bottom_block_center

        # Blocco alto: in fase -> costruttiva
        a1 = FunctionGraph(lambda x: A * np.sin(k * x),
                           x_range=[-3.4, 3.4, 0.02], color=BLUE_D, stroke_width=3).move_to(UP * cy_top)
        a2 = FunctionGraph(lambda x: A * np.sin(k * x),
                           x_range=[-3.4, 3.4, 0.02], color=GREEN_D, stroke_width=3).move_to(UP * cy_top + UP * 0.07)
        asum = FunctionGraph(lambda x: 2 * A * np.sin(k * x),
                             x_range=[-3.4, 3.4, 0.02], color=RED_D, stroke_width=6).move_to(UP * cy_top)
        sub_c = fit(MathTex(r"\Delta\varphi = 0", color=DARK_GRAY, font_size=28))
        sub_c.move_to([0, cy_top - 1.7, 0])
        lab_c = fit(Text("In fase: si rinforzano", font_size=22, color=RED_D))
        lab_c.move_to([0, cy_top + 1.7, 0])

        # Blocco basso: in opposizione -> distruttiva
        b1 = FunctionGraph(lambda x: A * np.sin(k * x),
                           x_range=[-3.4, 3.4, 0.02], color=BLUE_D, stroke_width=3).move_to(UP * cy_bot)
        b2 = FunctionGraph(lambda x: A * np.sin(k * x + PI),
                           x_range=[-3.4, 3.4, 0.02], color=GREEN_D, stroke_width=3).move_to(UP * cy_bot)
        bsum = Line([-3.4, cy_bot, 0], [3.4, cy_bot, 0], color=RED_D, stroke_width=6)
        sub_d = fit(MathTex(r"\Delta\varphi = \pi", color=DARK_GRAY, font_size=28))
        sub_d.move_to([0, cy_bot - 1.7, 0])
        lab_d = fit(Text("In opposizione: si annullano", font_size=22, color=RED_D))
        lab_d.move_to([0, cy_bot + 1.7, 0])

        self.play(Create(a1), Create(a2), FadeIn(sub_c))
        self.play(TransformFromCopy(VGroup(a1, a2), asum), FadeIn(lab_c))
        self.wait(0.3)
        self.play(Create(b1), Create(b2), FadeIn(sub_d))
        self.play(TransformFromCopy(VGroup(b1, b2), bsum), FadeIn(lab_d))
        self.wait(1.5)


# ============================================================================
# 4. DIFFRAZIONE: l'onda aggira gli ostacoli (principio di Huygens)
# ============================================================================

class Diffrazione(Scene):
    """Oltre una fenditura stretta il fronte d'onda si allarga: diffrazione."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("La diffrazione", "l'onda aggira gli ostacoli")
        self.play(Write(intestazione))
        self.wait(0.3)

        Sy = 1.3            # altezza della fenditura
        g = 0.45            # semi-apertura della fenditura
        S = np.array([0.0, Sy, 0])

        # Barriera con fenditura centrale
        muro_top = Line([0, Sy + g, 0], [0, 3.4, 0], color=DARK_GRAY, stroke_width=9)
        muro_bot = Line([0, Sy - g, 0], [0, -1.2, 0], color=DARK_GRAY, stroke_width=9)

        # Fronti d'onda piani in arrivo (a sinistra)
        piani = VGroup(*[
            Line([x, -1.2, 0], [x, 3.4, 0], color=BLUE_D, stroke_width=4)
            for x in (-3.0, -2.3, -1.6, -0.9)
        ])
        # Fronti circolari oltre la fenditura (a destra): semicerchi
        circolari = VGroup(*[
            Arc(radius=r, arc_center=S, start_angle=-PI / 2, angle=PI,
                color=GREEN_D, stroke_width=4)
            for r in (0.6, 1.2, 1.8, 2.4)
        ])

        self.play(Create(muro_top), Create(muro_bot))
        self.play(LaggedStart(*[Create(l) for l in piani], lag_ratio=0.15))
        self.play(piani.animate.shift(RIGHT * 0.6), run_time=1.2, rate_func=linear)
        self.play(LaggedStart(*[Create(a) for a in circolari], lag_ratio=0.25))

        nota = VGroup(
            Text("Ogni punto del fronte è sorgente", font_size=23, color=BLACK),
            Text("di onde secondarie (Huygens):", font_size=23, color=BLACK),
            Text("oltre la fenditura l'onda si allarga.", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.16)
        fit(nota)
        nota.move_to(DOWN * 3.6)
        self.play(FadeIn(nota))
        self.wait(1.5)


# ============================================================================
# 5. DOPPIA FENDITURA: frange di interferenza
# ============================================================================

class DoppiaFenditura(Scene):
    """Due fenditure: le onde si sovrappongono e creano frange chiare e scure."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Doppia fenditura", "frange di interferenza")
        self.play(Write(intestazione))
        self.wait(0.3)

        # Due sorgenti (le due fenditure)
        S1 = np.array([-2.6, 2.7, 0])
        S2 = np.array([-2.6, 0.7, 0])
        sorg1 = Dot(S1, color=BLUE_D, radius=0.08)
        sorg2 = Dot(S2, color=GREEN_D, radius=0.08)

        onde1 = VGroup(*[Arc(radius=r, arc_center=S1, start_angle=-PI / 2, angle=PI,
                             color=BLUE_D, stroke_width=2.5, stroke_opacity=0.7)
                         for r in (0.8, 1.6, 2.4, 3.2, 4.0)])
        onde2 = VGroup(*[Arc(radius=r, arc_center=S2, start_angle=-PI / 2, angle=PI,
                             color=GREEN_D, stroke_width=2.5, stroke_opacity=0.7)
                         for r in (0.8, 1.6, 2.4, 3.2, 4.0)])

        # Schermo a destra
        schermo = Line([3.1, -1.8, 0], [3.1, 4.0, 0], color=DARK_GRAY, stroke_width=4)
        lab_schermo = fit(Text("schermo", font_size=20, color=DARK_GRAY)).next_to(schermo, DOWN, buff=0.1)

        # Frange sullo schermo: massimi (rossi) alternati a minimi
        ymid = (S1[1] + S2[1]) / 2
        massimi = VGroup(*[Dot([3.1, ymid + k * 0.85, 0], color=RED_D, radius=0.1)
                           for k in (-2, -1, 0, 1, 2)])
        minimi = VGroup(*[Line([2.95, ymid + (k + 0.5) * 0.85, 0],
                               [3.25, ymid + (k + 0.5) * 0.85, 0],
                               color=DARK_GRAY, stroke_width=2)
                          for k in (-2, -1, 0, 1)])

        self.play(FadeIn(sorg1), FadeIn(sorg2))
        self.play(LaggedStart(*[Create(a) for a in onde1], lag_ratio=0.12),
                  LaggedStart(*[Create(a) for a in onde2], lag_ratio=0.12),
                  run_time=2.5)
        self.play(Create(schermo), FadeIn(lab_schermo))
        self.play(LaggedStart(*[GrowFromCenter(m) for m in massimi], lag_ratio=0.15),
                  *[Create(m) for m in minimi])

        # Condizione dei massimi
        formula = fit(MathTex(r"d\,\sin\theta = m\,\lambda", color=BLACK, font_size=40))
        formula.move_to([0, -2.6, 0])
        box = SurroundingRectangle(formula, color=DARK_BLUE, buff=0.2, corner_radius=0.12)
        nota = VGroup(
            Text("In fase → massimo (chiaro)", font_size=22, color=RED_D),
            Text("In opposizione → minimo (scuro)", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.15)
        fit(nota)
        nota.move_to([0, -4.0, 0])

        self.play(Write(formula), Create(box))
        self.play(FadeIn(nota))
        self.wait(2)

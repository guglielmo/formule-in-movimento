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


def onda_quadra_parziale(n_armoniche, ampiezza=1.0):
    """Somma parziale della serie di Fourier dell'onda quadra.

    L'onda quadra dispari vale (4/π)·Σ_{k dispari} sin(kx)/k. Usando solo le
    prime ``n_armoniche`` armoniche dispari si ottiene un'approssimazione che
    migliora all'aumentare dei termini.
    """
    def f(x):
        s = 0.0
        for i in range(n_armoniche):
            k = 2 * i + 1
            s += np.sin(k * x) / k
        return ampiezza * (4.0 / PI) * s
    return f


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

        # ---------- FASE 1: le frange (vista d'insieme) ----------
        S1p = np.array([-2.7, 2.4, 0])
        S2p = np.array([-2.7, 0.8, 0])
        sorg1 = Dot(S1p, color=BLUE_D, radius=0.08)
        sorg2 = Dot(S2p, color=GREEN_D, radius=0.08)
        onde1 = VGroup(*[Arc(radius=r, arc_center=S1p, start_angle=-PI / 2, angle=PI,
                             color=BLUE_D, stroke_width=2.5, stroke_opacity=0.6)
                         for r in (0.9, 1.8, 2.7, 3.6)])
        onde2 = VGroup(*[Arc(radius=r, arc_center=S2p, start_angle=-PI / 2, angle=PI,
                             color=GREEN_D, stroke_width=2.5, stroke_opacity=0.6)
                         for r in (0.9, 1.8, 2.7, 3.6)])
        schermo = Line([3.1, -1.0, 0], [3.1, 4.2, 0], color=DARK_GRAY, stroke_width=4)
        ymid = (S1p[1] + S2p[1]) / 2
        massimi = VGroup(*[Dot([3.1, ymid + kk * 0.8, 0], color=RED_D, radius=0.09)
                           for kk in (-2, -1, 0, 1, 2)])
        lab_frange = fit(Text("frange: massimi e minimi", font_size=22, color=DARK_GRAY))
        lab_frange.move_to([0, -1.4, 0])
        # La legge che governa le frange: mostrata PRIMA del dettaglio
        formula_intro = fit(MathTex(r"d\,\sin\theta = m\,\lambda", color=BLACK, font_size=46))
        formula_intro.move_to([0, -2.7, 0])
        box_intro = SurroundingRectangle(formula_intro, color=DARK_BLUE, buff=0.2, corner_radius=0.12)

        fase1 = VGroup(sorg1, sorg2, onde1, onde2, schermo, massimi, lab_frange,
                       formula_intro, box_intro)
        self.play(FadeIn(sorg1), FadeIn(sorg2))
        self.play(LaggedStart(*[Create(a) for a in onde1], lag_ratio=0.1),
                  LaggedStart(*[Create(a) for a in onde2], lag_ratio=0.1), run_time=2)
        self.play(Create(schermo), LaggedStart(*[GrowFromCenter(m) for m in massimi], lag_ratio=0.12))
        self.play(FadeIn(lab_frange))
        self.play(Write(formula_intro), Create(box_intro))
        self.wait(1.2)
        self.play(FadeOut(fase1))

        # ---------- FASE 2: da dove viene d·sinθ = m·λ ----------
        sotto = fit(Text("Da dove viene la formula?", font_size=24, color=DARK_BLUE))
        sotto.next_to(intestazione, DOWN, buff=0.4)
        self.play(FadeIn(sotto))

        def nrm(v):
            return v / np.linalg.norm(v)

        th = 35 * DEGREES
        u = np.array([np.cos(th), np.sin(th), 0])   # direzione (parallela) dei due raggi
        S1 = np.array([-1.7, 1.5, 0])               # fenditura in alto
        d_vis = 1.4
        S2 = S1 + np.array([0, -d_vis, 0])          # fenditura in basso
        R = 3.6
        delta = d_vis * np.sin(th)
        F = S2 + delta * u                          # piede della perpendicolare da S1 sul raggio di S2

        s1 = Dot(S1, color=BLUE_D, radius=0.08)
        s2 = Dot(S2, color=GREEN_D, radius=0.08)
        # distanza tra le fenditure d
        d_arrow = DoubleArrow(S1 + LEFT * 0.35, S2 + LEFT * 0.35, buff=0,
                              color=DARK_GRAY, stroke_width=3, tip_length=0.16)
        lab_d = MathTex(r"d", color=BLACK, font_size=34).next_to(d_arrow, LEFT, buff=0.12)
        # i due raggi paralleli verso lo schermo lontano
        ray1 = Arrow(S1, S1 + R * u, buff=0, color=BLUE_D, stroke_width=4)
        ray2 = Arrow(S2, S2 + R * u, buff=0, color=GREEN_D, stroke_width=4)
        lab_par = fit(Text("raggi paralleli (schermo lontano)", font_size=20, color=DARK_GRAY))
        lab_par.move_to([0, 4.4, 0])

        self.play(FadeIn(s1), FadeIn(s2), GrowArrow(d_arrow), Write(lab_d))
        self.play(GrowArrow(ray1), GrowArrow(ray2), FadeIn(lab_par))

        # fronte d'onda: perpendicolare ai raggi, da S1 fino al raggio di S2
        fronte = DashedLine(S1, F, color=DARK_GRAY, stroke_width=2)
        # marcatore di angolo retto in F
        a = 0.2
        dF1 = nrm(S1 - F)
        dF2 = nrm(S2 - F)
        angolo_retto = VGroup(
            Line(F + a * dF1, F + a * dF1 + a * dF2, color=DARK_GRAY, stroke_width=2),
            Line(F + a * dF2, F + a * dF1 + a * dF2, color=DARK_GRAY, stroke_width=2),
        )
        # differenza di cammino δ = tratto S2->F, evidenziato
        delta_seg = Line(S2, F, color=RED_D, stroke_width=7)
        lab_delta = MathTex(r"\delta = d\,\sin\theta", color=RED_D, font_size=34)
        lab_delta.next_to(F, RIGHT, buff=0.25).shift(UP * 0.1)
        # angolo θ presso S1 (tra la congiungente delle fenditure e il fronte)
        ang = Angle(Line(S1, S2), Line(S1, F), radius=0.55, color=DARK_BLUE, stroke_width=3)
        lab_th = MathTex(r"\theta", color=DARK_BLUE, font_size=30)
        bis = nrm(nrm(S2 - S1) + nrm(F - S1))
        lab_th.move_to(S1 + 0.85 * bis)

        self.play(Create(fronte), Create(angolo_retto))
        self.play(Create(delta_seg), Write(lab_delta))
        self.play(Create(ang), Write(lab_th))
        self.wait(0.5)

        # conclusione: massimo quando δ = m·λ
        cond = VGroup(
            Text("Massimo (frangia chiara) quando", font_size=23, color=BLACK),
            Text("la differenza di cammino è un multiplo di λ:", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.15)
        fit(cond)
        cond.move_to([0, -3.4, 0])
        formula = fit(MathTex(r"d\,\sin\theta = m\,\lambda", color=BLACK, font_size=48))
        formula.next_to(cond, DOWN, buff=0.4)
        box = SurroundingRectangle(formula, color=DARK_BLUE, buff=0.22, corner_radius=0.14)
        m_nota = fit(MathTex(r"m = 0,\ \pm 1,\ \pm 2,\ \dots", color=DARK_GRAY, font_size=30))
        m_nota.next_to(box, DOWN, buff=0.3)

        self.play(FadeIn(cond))
        self.play(Write(formula), Create(box))
        self.play(FadeIn(m_nota))
        self.wait(2)


# ============================================================================
# 6. TEOREMA DI FOURIER: ogni onda periodica è una somma di armoniche
# ============================================================================

class TeoremaFourier(Scene):
    """Un'onda periodica qualsiasi si scompone in una somma di sinusoidi."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Il teorema di Fourier", "Onde armoniche e periodiche")
        self.play(Write(intestazione))
        self.wait(0.3)

        # Onda complessa ma periodica: somma di tre armoniche
        def complessa(x):
            return 1.0 * np.sin(x) + 0.5 * np.sin(2 * x) + 0.33 * np.sin(3 * x)

        cy_top = 3.3
        onda = FunctionGraph(complessa, x_range=[-3.4, 3.4, 0.02],
                             color=RED_D, stroke_width=6).move_to(UP * cy_top)
        lab_onda = fit(Text("un'onda periodica qualsiasi", font_size=24, color=RED_D))
        lab_onda.next_to(onda, DOWN, buff=0.3)
        self.play(Create(onda), run_time=2)
        self.play(FadeIn(lab_onda))
        self.wait(0.5)

        # Si scompone in onde semplici (armoniche): fondamentale + multipli
        uguale = MathTex(r"=", color=BLACK, font_size=60).move_to([0, 1.1, 0])
        self.play(Write(uguale))

        a1 = FunctionGraph(lambda x: 1.0 * np.sin(x), x_range=[-3.4, 3.4, 0.02],
                           color=BLUE_D, stroke_width=4).move_to([0, -0.6, 0])
        lab_a1 = fit(MathTex(r"f_1", color=BLUE_D, font_size=30)).next_to(a1, LEFT, buff=0.2)
        a2 = FunctionGraph(lambda x: 0.5 * np.sin(2 * x), x_range=[-3.4, 3.4, 0.02],
                           color=GREEN_D, stroke_width=4).move_to([0, -2.6, 0])
        lab_a2 = fit(MathTex(r"2f_1", color=GREEN_D, font_size=30)).next_to(a2, LEFT, buff=0.2)
        a3 = FunctionGraph(lambda x: 0.33 * np.sin(3 * x), x_range=[-3.4, 3.4, 0.02],
                           color=DARK_BLUE, stroke_width=4).move_to([0, -4.6, 0])
        lab_a3 = fit(MathTex(r"3f_1", color=DARK_BLUE, font_size=30)).next_to(a3, LEFT, buff=0.2)
        plus1 = MathTex(r"+", color=BLACK, font_size=44).move_to([0, -1.6, 0])
        plus2 = MathTex(r"+", color=BLACK, font_size=44).move_to([0, -3.6, 0])

        self.play(TransformFromCopy(onda, a1), FadeIn(lab_a1))
        self.play(Write(plus1), TransformFromCopy(onda, a2), FadeIn(lab_a2))
        self.play(Write(plus2), TransformFromCopy(onda, a3), FadeIn(lab_a3))
        self.wait(0.5)

        msg = VGroup(
            Text("Armoniche: la fondamentale e i suoi multipli", font_size=22, color=BLACK),
            Text("ricostruiscono qualsiasi onda periodica", font_size=22, color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.2)
        fit(msg)
        msg.move_to(DOWN * 6.2)
        self.play(Write(msg))
        self.wait(1.5)


# ============================================================================
# 7. SINTESI: costruire un'onda quadra sommando le armoniche
# ============================================================================

class SintesiOndaQuadra(Scene):
    """Sommando sempre più armoniche dispari ci si avvicina a un'onda quadra."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Costruire un'onda quadra", "Sommando le armoniche")
        self.play(Write(intestazione))
        self.wait(0.3)

        A = 1.3
        cy = 2.4
        x_rng = [-3.4, 3.4, 0.01]

        asse = Line([-3.4, cy, 0], [3.4, cy, 0], color=DARK_GRAY, stroke_width=2)
        self.play(Create(asse))

        # Bersaglio: l'onda quadra (tratteggiata, fissa)
        bersaglio = DashedVMobject(
            FunctionGraph(onda_quadra_parziale(60, A), x_range=x_rng,
                          color=DARK_GRAY, stroke_width=3).move_to(UP * cy),
            num_dashes=120,
        )
        lab_bersaglio = fit(Text("onda quadra (obiettivo)", font_size=22, color=DARK_GRAY))
        lab_bersaglio.move_to([0, cy + 2.0, 0])
        self.play(Create(bersaglio), FadeIn(lab_bersaglio))
        self.wait(0.3)

        # Contatore del numero di armoniche sommate
        n_lbl = Text("Armoniche sommate:", font_size=26, color=BLACK)
        n_num = Integer(1, color=RED_D, font_size=40)
        contatore = VGroup(n_lbl, n_num).arrange(RIGHT, buff=0.25)
        fit(contatore)
        contatore.move_to([0, -1.3, 0])

        # Formula della serie
        formula = fit(MathTex(
            r"y = \frac{4}{\pi}\left(\sin x + \tfrac{1}{3}\sin 3x + \tfrac{1}{5}\sin 5x + \dots\right)",
            color=DARK_BLUE, font_size=32))
        formula.move_to([0, -3.0, 0])

        # Prima approssimazione: una sola armonica (la fondamentale)
        approx = FunctionGraph(onda_quadra_parziale(1, A), x_range=x_rng,
                               color=RED_D, stroke_width=6).move_to(UP * cy)
        self.play(Create(approx), FadeIn(contatore))
        self.play(Write(formula))
        self.wait(0.5)

        # Aggiunge armoniche dispari, una alla volta
        for n in (2, 3, 4, 6, 10):
            nuova = FunctionGraph(onda_quadra_parziale(n, A), x_range=x_rng,
                                  color=RED_D, stroke_width=6).move_to(UP * cy)
            self.play(
                Transform(approx, nuova),
                n_num.animate.set_value(n),
                run_time=1.2,
            )
            self.wait(0.3)

        nota = fit(Text("Più armoniche sommi, più la forma è esatta",
                        font_size=22, color=GREEN_D, weight=BOLD))
        nota.move_to([0, -5.0, 0])
        self.play(FadeIn(nota))
        self.wait(1.5)


# ============================================================================
# 8. LO SPETTRO: dal dominio del tempo a quello delle frequenze
# ============================================================================

class SpettroFrequenze(Scene):
    """Lo spettro: quanto pesa ciascuna armonica nell'onda quadra."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Lo spettro", "Il peso di ogni armonica")
        self.play(Write(intestazione))
        self.wait(0.3)

        # --- BLOCCO ALTO: l'onda nel tempo ---
        cy_top = 3.6
        onda = FunctionGraph(onda_quadra_parziale(10, 1.0), x_range=[-3.4, 3.4, 0.01],
                             color=RED_D, stroke_width=5).move_to(UP * cy_top)
        lab_tempo = fit(Text("Dominio del tempo", font_size=24, color=RED_D, weight=BOLD))
        lab_tempo.move_to([0, cy_top + 1.6, 0])
        self.play(FadeIn(lab_tempo), Create(onda), run_time=1.5)
        self.wait(0.3)

        # --- BLOCCO BASSO: spettro a barre ---
        lab_freq = fit(Text("Dominio delle frequenze", font_size=24, color=DARK_BLUE, weight=BOLD))
        lab_freq.move_to([0, 0.9, 0])
        self.play(FadeIn(lab_freq))

        base_y = -4.6
        asse_x = Line([-3.0, base_y, 0], [3.2, base_y, 0], color=DARK_GRAY, stroke_width=2)
        asse_y = Line([-3.0, base_y, 0], [-3.0, base_y + 4.2, 0], color=DARK_GRAY, stroke_width=2)
        lab_ax_x = Text("frequenza", font_size=20, color=DARK_GRAY).next_to(asse_x, RIGHT, buff=0.1)
        lab_ax_y = Text("ampiezza", font_size=20, color=DARK_GRAY).rotate(PI / 2).next_to(asse_y, LEFT, buff=0.1)
        self.play(Create(asse_x), Create(asse_y), FadeIn(lab_ax_x), FadeIn(lab_ax_y))

        # Armoniche dispari: ampiezza ∝ 1/n
        armoniche = [1, 3, 5, 7, 9]
        larghezza = 0.5
        passo = 1.15
        x0 = -2.3
        altezza_max = 3.6  # corrisponde all'armonica n = 1
        barre = VGroup()
        etichette = VGroup()
        for i, n in enumerate(armoniche):
            h = altezza_max / n
            x = x0 + i * passo
            barra = Rectangle(width=larghezza, height=h, color=DARK_BLUE,
                              fill_color=DARK_BLUE, fill_opacity=0.7, stroke_width=2)
            barra.move_to([x, base_y + h / 2, 0])
            et = MathTex(rf"{n}f_1", color=DARK_BLUE, font_size=26)
            et.next_to(barra, DOWN, buff=0.12)
            barre.add(barra)
            etichette.add(et)

        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in barre], lag_ratio=0.2),
            LaggedStart(*[FadeIn(e) for e in etichette], lag_ratio=0.2),
        )
        self.wait(0.5)

        nota = fit(Text("Solo armoniche dispari, ampiezza ∝ 1/n",
                        font_size=22, color=BLACK))
        nota.next_to(asse_x, DOWN, buff=0.7)
        self.play(FadeIn(nota))
        self.wait(1.5)


# ============================================================================
# 9. INTERFERENZA: descrizione geometrica (cammini ottici e differenza di percorso)
# ============================================================================

class InterferenzaGeometrica(Scene):
    """I cammini ottici da due sorgenti a un punto: la differenza di percorso
    decide se l'interferenza è costruttiva (massimo) o distruttiva (minimo)."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("La geometria dell'interferenza", "I cammini ottici")
        self.play(Write(intestazione))
        self.wait(0.3)

        def nrm(v):
            return v / np.linalg.norm(v)

        # Due sorgenti coerenti a sinistra e un punto di osservazione P a destra
        S1 = np.array([-2.8, 2.8, 0])
        S2 = np.array([-2.8, 0.4, 0])
        P = np.array([3.0, 3.6, 0])
        r1 = np.linalg.norm(P - S1)
        r2 = np.linalg.norm(P - S2)
        delta = r2 - r1  # P è più vicino a S1: r2 è il cammino più lungo

        s1 = Dot(S1, color=BLUE_D, radius=0.09)
        s2 = Dot(S2, color=GREEN_D, radius=0.09)
        p = Dot(P, color=RED_D, radius=0.09)
        lab_s1 = MathTex(r"S_1", color=BLUE_D, font_size=34).next_to(s1, LEFT, buff=0.15)
        lab_s2 = MathTex(r"S_2", color=GREEN_D, font_size=34).next_to(s2, LEFT, buff=0.15)
        lab_p = MathTex(r"P", color=RED_D, font_size=34).next_to(p, RIGHT, buff=0.15)

        # I due cammini ottici verso P
        ray1 = Line(S1, P, color=BLUE_D, stroke_width=4)
        ray2 = Line(S2, P, color=GREEN_D, stroke_width=4)
        lab_r1 = MathTex(r"r_1", color=BLUE_D, font_size=32).move_to(
            (S1 + P) / 2 + np.array([0, 0.32, 0]))
        lab_r2 = MathTex(r"r_2", color=GREEN_D, font_size=32).move_to(
            (S2 + P) / 2 + np.array([0, -0.32, 0]))

        # Distanza d tra le sorgenti
        d_arrow = DoubleArrow(S1 + LEFT * 0.55, S2 + LEFT * 0.55, buff=0,
                              color=DARK_GRAY, stroke_width=3, tip_length=0.16)
        lab_d = MathTex(r"d", color=BLACK, font_size=34).next_to(d_arrow, LEFT, buff=0.12)

        self.play(FadeIn(s1), FadeIn(s2), FadeIn(p),
                  Write(lab_s1), Write(lab_s2), Write(lab_p))
        self.play(GrowArrow(d_arrow), Write(lab_d))
        self.play(Create(ray1), Create(ray2), Write(lab_r1), Write(lab_r2))
        self.wait(0.4)

        # Punto Q su r2 alla stessa distanza r1 da P: il tratto S2->Q è la
        # differenza di cammino δ = r2 - r1.
        Q = S2 + (delta / r2) * (P - S2)
        # Arco centrato in P, raggio r1: passa per S1 e per Q (punti equidistanti da P)
        ang_s1 = np.arctan2((S1 - P)[1], (S1 - P)[0])
        ang_q = np.arctan2((Q - P)[1], (Q - P)[0])
        arco = Arc(radius=r1, arc_center=P, start_angle=ang_s1, angle=ang_q - ang_s1,
                   color=DARK_GRAY, stroke_width=2)
        arco = DashedVMobject(arco, num_dashes=22)
        lab_arco = fit(Text("stessa distanza da P", font_size=20, color=DARK_GRAY))
        lab_arco.next_to(arco, RIGHT, buff=0.1).shift(DOWN * 0.1)

        delta_seg = Line(S2, Q, color=RED_D, stroke_width=7)
        lab_delta = MathTex(r"\delta", color=RED_D, font_size=36).next_to(
            delta_seg, UP, buff=0.12).shift(LEFT * 0.1)

        self.play(Create(arco), FadeIn(lab_arco))
        self.play(Create(delta_seg), Write(lab_delta))
        def_delta = fit(MathTex(r"\delta = r_2 - r_1 = \text{differenza di cammino}",
                                color=BLACK, font_size=34))
        def_delta.move_to([0, -1.3, 0])
        self.play(Write(def_delta))
        self.wait(0.5)

        # Le due condizioni: massimo (costruttiva) e minimo (distruttiva)
        cond_max = fit(MathTex(r"\delta = m\,\lambda \;\;\Rightarrow\;\; \text{MASSIMO}",
                               color=GREEN_D, font_size=38))
        cond_max.move_to([0, -2.6, 0])
        sub_max = fit(Text("le onde arrivano in fase: costruttiva", font_size=22, color=DARK_GRAY))
        sub_max.next_to(cond_max, DOWN, buff=0.2)

        cond_min = fit(MathTex(r"\delta = \left(m + \tfrac{1}{2}\right)\lambda \;\;\Rightarrow\;\; \text{MINIMO}",
                               color=RED_D, font_size=38))
        cond_min.move_to([0, -4.4, 0])
        sub_min = fit(Text("in opposizione di fase: distruttiva", font_size=22, color=DARK_GRAY))
        sub_min.next_to(cond_min, DOWN, buff=0.2)

        self.play(Write(cond_max), FadeIn(sub_max))
        self.play(Write(cond_min), FadeIn(sub_min))
        self.wait(0.5)

        m_nota = fit(MathTex(r"m = 0,\ \pm 1,\ \pm 2,\ \dots", color=DARK_GRAY, font_size=30))
        m_nota.move_to([0, -5.7, 0])
        legame = fit(Text("Con lo schermo lontano: δ = d · sin θ", font_size=22, color=DARK_BLUE))
        legame.move_to([0, -6.4, 0])
        self.play(FadeIn(m_nota))
        self.play(FadeIn(legame))
        self.wait(1.5)

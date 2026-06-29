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
# 4. FRONTI D'ONDA E RAGGI
# ============================================================================

class FrontiDOnda(Scene):
    """Il fronte d'onda unisce i punti in fase; il raggio ne indica la direzione."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Fronti d'onda e raggi", "dai fronti alla direzione")
        self.play(Write(intestazione))
        self.wait(0.3)

        # Fronti d'onda piani (linee verticali) che avanzano
        fronti = VGroup(*[
            Line([x, 2.6, 0], [x, -0.6, 0], color=BLUE_D, stroke_width=4)
            for x in np.arange(-3.0, 1.01, 1.0)
        ])
        self.play(LaggedStart(*[Create(l) for l in fronti], lag_ratio=0.12))

        lab_fronte = fit(Text("fronte d'onda", font_size=22, color=BLUE_D))
        lab_fronte.move_to([0, 3.1, 0])

        # Raggio: perpendicolare ai fronti
        raggio = Arrow([-3.4, 1.0, 0], [3.4, 1.0, 0], color=RED_D, buff=0)
        lab_raggio = fit(Text("raggio", font_size=22, color=RED_D))
        lab_raggio.next_to(raggio.get_end(), UP, buff=0.1)

        self.play(FadeIn(lab_fronte))
        self.play(GrowArrow(raggio), FadeIn(lab_raggio))

        # I fronti avanzano nella direzione del raggio
        self.play(fronti.animate.shift(RIGHT * 2.0), run_time=3, rate_func=linear)

        nota = VGroup(
            Text("Il fronte d'onda unisce i punti in fase.", font_size=23, color=BLACK),
            Text("Il raggio è perpendicolare ai fronti", font_size=23, color=DARK_GRAY),
            Text("e indica la direzione di propagazione.", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.18)
        fit(nota)
        nota.move_to(DOWN * 3.6)
        self.play(FadeIn(nota))
        self.wait(1.5)


# ============================================================================
# 5. LA RIFRAZIONE
# ============================================================================

class Rifrazione(Scene):
    """Cambiando mezzo cambiano velocità e lunghezza d'onda: l'onda piega."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("La rifrazione", "cambio di mezzo e velocità")
        self.play(Write(intestazione))
        self.wait(0.3)

        O = np.array([0.0, 1.4, 0])
        th1 = 42 * DEGREES
        th2 = 26 * DEGREES
        d1 = np.array([np.sin(th1), -np.cos(th1), 0])   # propagazione incidente (giù-destra)
        d2 = np.array([np.sin(th2), -np.cos(th2), 0])   # propagazione rifratta
        perp1 = np.array([np.cos(th1), np.sin(th1), 0])
        perp2 = np.array([np.cos(th2), np.sin(th2), 0])
        P1 = O - d1 * 2.3
        P2 = O + d2 * 2.6

        # Mezzi: 1 (sopra, veloce) e 2 (sotto, lento)
        mezzo2 = Rectangle(width=7.2, height=6.2, fill_color=BLUE_D, fill_opacity=0.10,
                           stroke_width=0).move_to([0, O[1] - 6.2 / 2, 0])
        confine = Line([-3.6, O[1], 0], [3.6, O[1], 0], color=DARK_GRAY, stroke_width=3)
        lab_m1 = fit(Text("Mezzo 1 (veloce)", font_size=22, color=DARK_GRAY)).move_to([1.9, O[1] + 1.5, 0])
        lab_m2 = fit(Text("Mezzo 2 (lento)", font_size=22, color=DARK_BLUE)).move_to([-1.9, O[1] - 1.0, 0])

        normale = DashedLine(O + UP * 2.2, O + DOWN * 2.2, color=DARK_GRAY, stroke_width=2)

        incidente = Arrow(P1, O, color=RED_D, buff=0)
        rifratto = Arrow(O, P2, color=GREEN_D, buff=0)

        arc1 = Arc(radius=0.7, arc_center=O, start_angle=PI / 2, angle=th1,
                   color=DARK_BLUE, stroke_width=3)
        lab_th1 = MathTex(r"\theta_1", color=DARK_BLUE, font_size=32).move_to(
            O + 1.05 * np.array([np.cos(PI / 2 + th1 / 2), np.sin(PI / 2 + th1 / 2), 0]))
        arc2 = Arc(radius=0.7, arc_center=O, start_angle=-PI / 2, angle=th2,
                   color=DARK_BLUE, stroke_width=3)
        lab_th2 = MathTex(r"\theta_2", color=DARK_BLUE, font_size=32).move_to(
            O + 1.05 * np.array([np.cos(-PI / 2 + th2 / 2), np.sin(-PI / 2 + th2 / 2), 0]))

        # Fronti d'onda: piu' larghi nel mezzo 1, piu' stretti nel mezzo 2
        def fronti_lungo(direction, perp, spacing, n, start, length, color):
            g = VGroup()
            for i in range(n):
                c = O + direction * (start + i * spacing)
                g.add(Line(c - perp * length / 2, c + perp * length / 2,
                           color=color, stroke_width=3))
            return g

        fronti1 = fronti_lungo(-d1, perp1, 0.85, 3, 0.6, 1.0, RED_D)
        fronti2 = fronti_lungo(d2, perp2, 0.5, 3, 0.5, 0.8, GREEN_D)

        self.play(FadeIn(mezzo2), Create(confine), FadeIn(lab_m1), FadeIn(lab_m2))
        self.play(Create(normale))
        self.play(GrowArrow(incidente))
        self.play(LaggedStart(*[Create(f) for f in fronti1], lag_ratio=0.2))
        self.play(GrowArrow(rifratto))
        self.play(LaggedStart(*[Create(f) for f in fronti2], lag_ratio=0.2))
        self.play(Create(arc1), Write(lab_th1), Create(arc2), Write(lab_th2))
        self.wait(0.3)

        # Legge di Snell e relazioni
        snell = fit(MathTex(r"n_1 \sin\theta_1 = n_2 \sin\theta_2", color=BLACK, font_size=40))
        snell.move_to([0, -2.9, 0])
        box = SurroundingRectangle(snell, color=DARK_BLUE, buff=0.2, corner_radius=0.12)
        rel = fit(MathTex(r"\frac{\sin\theta_1}{\sin\theta_2} = \frac{v_1}{v_2} = \frac{\lambda_1}{\lambda_2}",
                          color=DARK_BLUE, font_size=36))
        rel.next_to(snell, DOWN, buff=0.5)
        self.play(Write(snell), Create(box))
        self.play(Write(rel))

        nota = VGroup(
            Text("Cambiano velocità e lunghezza d'onda;", font_size=22, color=BLACK),
            Text("la frequenza resta la stessa: l'onda piega.", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.15)
        fit(nota)
        nota.move_to([0, -5.6, 0])
        self.play(FadeIn(nota))
        self.wait(2)

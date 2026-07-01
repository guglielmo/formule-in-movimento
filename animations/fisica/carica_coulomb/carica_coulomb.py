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
import numpy as np


def carica(segno, color, pos):
    """Pallino con il simbolo + o − che rappresenta una carica."""
    c = Circle(radius=0.4, color=color, fill_opacity=0.9, stroke_width=0).move_to(pos)
    simbolo = MathTex(segno, color=WHITE, font_size=40).move_to(pos)
    return VGroup(c, simbolo)


class CaricaElettrica(Scene):
    """La carica elettrica: due tipi, quantizzazione, unità di misura."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("La Carica Elettrica", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("esistono due tipi di carica", font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        # Le due cariche
        pos_pos = LEFT * 1.6 + UP * 1.8
        neg_pos = RIGHT * 1.6 + UP * 1.8
        q_pos = carica("+", RED_D, pos_pos)
        q_neg = carica("-", BLUE_D, neg_pos)
        lab_pos = Text("positiva", font_size=22, color=RED_D).next_to(q_pos, DOWN, buff=0.25)
        lab_neg = Text("negativa", font_size=22, color=BLUE_D).next_to(q_neg, DOWN, buff=0.25)
        self.play(FadeIn(q_pos, scale=0.5), FadeIn(q_neg, scale=0.5))
        self.play(Write(lab_pos), Write(lab_neg))
        self.wait(0.8)

        # Quantizzazione della carica
        h = Text("La carica è quantizzata:", font_size=24, color=DARK_GRAY, weight=BOLD)
        q = MathTex(r"q = n\,e", color=BLACK, font_size=44)
        e = MathTex(r"e = 1.6\times 10^{-19}\ \text{C}", color=DARK_BLUE, font_size=32)
        gruppo = VGroup(h, q, e).arrange(DOWN, buff=0.4)
        gruppo.next_to(lab_pos, DOWN, buff=1.0).set_x(0)
        self.play(FadeIn(h))
        self.play(Write(q))
        box = SurroundingRectangle(q, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.play(Write(e))
        self.wait(0.6)

        nota = VGroup(
            Text("n = numero intero,  e = carica elementare", font_size=20, color=DARK_GRAY),
            Text("L'unità di misura è il coulomb (C)", font_size=22,
                 color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(gruppo, DOWN, buff=0.7)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class AttrazioneRepulsione(Scene):
    """Cariche dello stesso segno si respingono, di segno opposto si attraggono."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Attrazione e Repulsione", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        # Caso 1: cariche uguali si respingono
        h1 = Text("Cariche uguali → si respingono", font_size=24,
                  color=DARK_GRAY, weight=BOLD)
        h1.next_to(title, DOWN, buff=0.7)
        self.play(FadeIn(h1))
        a = carica("+", RED_D, LEFT * 1.3 + UP * 1.6)
        b = carica("+", RED_D, RIGHT * 1.3 + UP * 1.6)
        f_a = Arrow(LEFT * 1.3 + UP * 1.6, LEFT * 2.6 + UP * 1.6, color=DARK_GRAY,
                    buff=0.45, stroke_width=5)
        f_b = Arrow(RIGHT * 1.3 + UP * 1.6, RIGHT * 2.6 + UP * 1.6, color=DARK_GRAY,
                    buff=0.45, stroke_width=5)
        self.play(FadeIn(a, scale=0.5), FadeIn(b, scale=0.5))
        self.play(GrowArrow(f_a), GrowArrow(f_b))
        self.wait(0.8)

        # Caso 2: cariche opposte si attraggono
        h2 = Text("Cariche opposte → si attraggono", font_size=24,
                  color=DARK_GRAY, weight=BOLD)
        h2.next_to(h1, DOWN, buff=1.7)
        self.play(FadeIn(h2))
        c = carica("+", RED_D, LEFT * 1.3 + DOWN * 1.2)
        d = carica("-", BLUE_D, RIGHT * 1.3 + DOWN * 1.2)
        f_c = Arrow(LEFT * 1.3 + DOWN * 1.2, RIGHT * 0.0 + DOWN * 1.2, color=DARK_GRAY,
                    buff=0.45, stroke_width=5)
        f_d = Arrow(RIGHT * 1.3 + DOWN * 1.2, LEFT * 0.0 + DOWN * 1.2, color=DARK_GRAY,
                    buff=0.45, stroke_width=5)
        self.play(FadeIn(c, scale=0.5), FadeIn(d, scale=0.5))
        self.play(GrowArrow(f_c), GrowArrow(f_d))
        self.wait(0.8)

        nota = Text("La forza è diretta lungo la retta che unisce le cariche",
                    font_size=21, color=GREEN_D, weight=BOLD, slant=ITALIC)
        nota.next_to(h2, DOWN, buff=1.6)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class LeggeCoulomb(Scene):
    """La legge di Coulomb: F = k q1 q2 / r²."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("La Legge di Coulomb", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        # Due cariche a distanza r
        A = LEFT * 1.8 + UP * 2.0
        B = RIGHT * 1.8 + UP * 2.0
        qa = carica("+", RED_D, A)
        qb = carica("+", RED_D, B)
        linea = DashedLine(A, B, color=DARK_GRAY, stroke_width=2)
        r_lab = MathTex("r", color=DARK_GRAY, font_size=30).next_to(linea, UP, buff=0.15)
        q1_lab = MathTex("q_1", color=RED_D, font_size=28).next_to(qa, DOWN, buff=0.2)
        q2_lab = MathTex("q_2", color=RED_D, font_size=28).next_to(qb, DOWN, buff=0.2)
        self.play(FadeIn(qa, scale=0.5), FadeIn(qb, scale=0.5))
        self.play(Create(linea), Write(r_lab), Write(q1_lab), Write(q2_lab))
        self.wait(0.6)

        # La formula
        formula = MathTex(r"F = k\,\dfrac{q_1\,q_2}{r^2}", color=BLACK, font_size=52)
        formula.next_to(qa, DOWN, buff=1.6).set_x(0)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.3,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.5)

        k = MathTex(r"k \approx 9\times 10^{9}\ \dfrac{\text{N}\cdot\text{m}^2}{\text{C}^2}",
                    color=DARK_BLUE, font_size=32)
        k.next_to(box, DOWN, buff=0.5)
        self.play(Write(k))
        self.wait(0.5)

        nota = VGroup(
            Text("La forza cresce col prodotto delle cariche", font_size=20, color=DARK_GRAY),
            Text("e diminuisce col quadrato della distanza", font_size=20, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.2)
        nota.next_to(k, DOWN, buff=0.55)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class EsempioCoulomb(Scene):
    """Esempio numerico della legge di Coulomb."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio: Forza di Coulomb", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"q_1 = 2\ \mu C,\quad q_2 = 3\ \mu C,\quad r = 0.1\ \text{m}",
                       color=DARK_BLUE, font_size=30)
        dati.next_to(title, DOWN, buff=0.6)
        self.play(Write(dati))
        self.wait(0.5)

        s1 = MathTex(r"F = k\,\dfrac{q_1\,q_2}{r^2}", color=BLACK, font_size=36)
        s2 = MathTex(r"F = 9\times 10^{9}\cdot\dfrac{(2\times 10^{-6})(3\times 10^{-6})}{(0.1)^2}",
                     color=BLACK, font_size=28)
        s3 = MathTex(r"F = 9\times 10^{9}\cdot\dfrac{6\times 10^{-12}}{10^{-2}}",
                     color=BLACK, font_size=30)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.5)
        passi.next_to(dati, DOWN, buff=0.7)
        for s in passi:
            self.play(Write(s))
            self.wait(0.4)
        self.wait(0.4)

        ris = MathTex(r"F = 5.4\ \text{N}", color=GREEN_D, font_size=48)
        ris.next_to(passi, DOWN, buff=0.7)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        nota = Text("(forza repulsiva: le cariche sono entrambe positive)",
                    font_size=20, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(box, DOWN, buff=0.45)
        self.play(FadeIn(nota))
        self.wait(2.5)


class AnalogiaGravitazione(Scene):
    """Coulomb e gravitazione: stessa struttura, l'inverso del quadrato."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Coulomb e Gravitazione", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        subtitle = Text("due forze, la stessa struttura", font_size=23, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        h1 = Text("Forza elettrica", font_size=26, color=RED_D, weight=BOLD)
        f1 = MathTex(r"F = k\,\dfrac{q_1\,q_2}{r^2}", color=BLACK, font_size=40)
        blocco1 = VGroup(h1, f1).arrange(DOWN, buff=0.3)

        h2 = Text("Forza gravitazionale", font_size=26, color=DARK_BLUE, weight=BOLD)
        f2 = MathTex(r"F = G\,\dfrac{m_1\,m_2}{r^2}", color=BLACK, font_size=40)
        blocco2 = VGroup(h2, f2).arrange(DOWN, buff=0.3)

        blocchi = VGroup(blocco1, blocco2).arrange(DOWN, buff=1.0)
        blocchi.next_to(subtitle, DOWN, buff=0.8)
        self.play(FadeIn(h1), Write(f1))
        self.wait(0.5)
        self.play(FadeIn(h2), Write(f2))
        self.wait(0.8)

        nota = VGroup(
            Text("Entrambe vanno come 1/r²", font_size=23, color=GREEN_D, weight=BOLD),
            Text("Ma quella elettrica può attrarre O respingere;",
                 font_size=20, color=DARK_GRAY),
            Text("la gravità solo attrarre.", font_size=20, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.2)
        nota.next_to(blocchi, DOWN, buff=0.8)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

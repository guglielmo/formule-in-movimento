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


def _norm(v):
    n = np.linalg.norm(v)
    return v / n if n else v


def triangolo_etichettato(A, B, C):
    """Triangolo con vertici A,B,C, angoli α,β,γ e lati a,b,c (opposti)."""
    G = (A + B + C) / 3
    tri = Polygon(A, B, C, color=BLACK, stroke_width=4)

    # Vertici
    vA = MathTex("A", color=BLACK, font_size=26).move_to(A + 0.35 * _norm(A - G))
    vB = MathTex("B", color=BLACK, font_size=26).move_to(B + 0.35 * _norm(B - G))
    vC = MathTex("C", color=BLACK, font_size=26).move_to(C + 0.35 * _norm(C - G))

    # Angoli (appena dentro ai vertici)
    aA = MathTex(r"\alpha", color=GREEN_D, font_size=28).move_to(A + 0.7 * _norm(G - A))
    aB = MathTex(r"\beta", color=GREEN_D, font_size=28).move_to(B + 0.7 * _norm(G - B))
    aC = MathTex(r"\gamma", color=GREEN_D, font_size=28).move_to(C + 0.7 * _norm(G - C))

    # Lati (al di fuori, opposti al rispettivo vertice)
    mBC = (B + C) / 2
    mAC = (A + C) / 2
    mAB = (A + B) / 2
    la = MathTex("a", color=RED_D, font_size=28).move_to(mBC + 0.4 * _norm(mBC - G))
    lb = MathTex("b", color=BLUE_D, font_size=28).move_to(mAC + 0.4 * _norm(mAC - G))
    lc = MathTex("c", color=DARK_BLUE, font_size=28).move_to(mAB + 0.4 * _norm(mAB - G))

    return VGroup(tri, vA, vB, vC, aA, aB, aC, la, lb, lc)


class TeoremaSeni(Scene):
    """Teorema dei seni: a/sin α = b/sin β = c/sin γ = 2R."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Teorema dei Seni", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        A = np.array([-2.0, 0.6, 0.0])
        B = np.array([2.3, 0.2, 0.0])
        C = np.array([0.2, 3.0, 0.0])
        fig = triangolo_etichettato(A, B, C)
        self.play(Create(fig[0]))
        self.play(LaggedStart(*[Write(m) for m in fig[1:]], lag_ratio=0.15))
        self.wait(0.8)

        formula = MathTex(r"\dfrac{a}{\sin\alpha} = \dfrac{b}{\sin\beta}"
                          r" = \dfrac{c}{\sin\gamma} = 2R",
                          color=BLACK, font_size=40)
        formula.next_to(fig, DOWN, buff=1.0)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.8)

        nota = Text("Ogni lato è proporzionale al seno dell'angolo opposto",
                    font_size=21, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class EsempioSeni(Scene):
    """Esempio: noti a, α, β trovare il lato b."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio: Teorema dei Seni", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"a = 10,\quad \alpha = 30^\circ,\quad \beta = 45^\circ",
                       color=DARK_BLUE, font_size=32)
        dati.next_to(title, DOWN, buff=0.6)
        self.play(Write(dati))
        domanda = Text("Trovare il lato b", font_size=24, color=DARK_GRAY, weight=BOLD)
        domanda.next_to(dati, DOWN, buff=0.4)
        self.play(FadeIn(domanda))
        self.wait(0.5)

        s1 = MathTex(r"\dfrac{a}{\sin\alpha} = \dfrac{b}{\sin\beta}",
                     color=BLACK, font_size=36)
        s2 = MathTex(r"b = \dfrac{a\,\sin\beta}{\sin\alpha}"
                     r" = \dfrac{10\,\sin 45^\circ}{\sin 30^\circ}",
                     color=BLACK, font_size=32)
        s3 = MathTex(r"b = \dfrac{10\cdot\tfrac{\sqrt{2}}{2}}{\tfrac{1}{2}}"
                     r" = 10\sqrt{2}", color=BLACK, font_size=32)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.5)
        passi.next_to(domanda, DOWN, buff=0.6)
        for s in passi:
            self.play(Write(s))
            self.wait(0.4)
        self.wait(0.4)

        ris = MathTex(r"b = 10\sqrt{2} \approx 14.14", color=GREEN_D, font_size=42)
        ris.next_to(passi, DOWN, buff=0.7)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)


class TeoremaCoseno(Scene):
    """Teorema del coseno: c² = a² + b² − 2ab·cos γ."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Teorema del Coseno", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        A = np.array([-2.0, 0.6, 0.0])
        B = np.array([2.3, 0.2, 0.0])
        C = np.array([0.2, 3.0, 0.0])
        fig = triangolo_etichettato(A, B, C)
        self.play(Create(fig[0]))
        self.play(LaggedStart(*[Write(m) for m in fig[1:]], lag_ratio=0.15))
        self.wait(0.8)

        formula = MathTex(r"c^2 = a^2 + b^2 - 2ab\,\cos\gamma",
                          color=BLACK, font_size=40)
        formula.next_to(fig, DOWN, buff=1.0)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.8)

        nota = VGroup(
            Text("È il teorema di Pitagora generalizzato:", font_size=21, color=DARK_GRAY),
            MathTex(r"\text{se } \gamma = 90^\circ \Rightarrow \cos\gamma = 0"
                    r"\Rightarrow c^2 = a^2 + b^2", color=DARK_GRAY, font_size=26),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class EsempioCoseno(Scene):
    """Esempio: noti a, b e l'angolo compreso γ trovare c."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio: Teorema del Coseno", font_size=30, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"a = 5,\quad b = 8,\quad \gamma = 60^\circ",
                       color=DARK_BLUE, font_size=32)
        dati.next_to(title, DOWN, buff=0.6)
        self.play(Write(dati))
        domanda = Text("Trovare il lato c", font_size=24, color=DARK_GRAY, weight=BOLD)
        domanda.next_to(dati, DOWN, buff=0.4)
        self.play(FadeIn(domanda))
        self.wait(0.5)

        s1 = MathTex(r"c^2 = a^2 + b^2 - 2ab\,\cos\gamma", color=BLACK, font_size=34)
        s2 = MathTex(r"c^2 = 25 + 64 - 2\cdot 5\cdot 8\cdot\cos 60^\circ",
                     color=BLACK, font_size=30)
        s3 = MathTex(r"c^2 = 89 - 80\cdot\tfrac{1}{2} = 49", color=BLACK, font_size=32)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.5)
        passi.next_to(domanda, DOWN, buff=0.6)
        for s in passi:
            self.play(Write(s))
            self.wait(0.4)
        self.wait(0.4)

        ris = MathTex(r"c = 7", color=GREEN_D, font_size=52)
        ris.next_to(passi, DOWN, buff=0.7)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)


class QuandoUsarli(Scene):
    """Quando usare il teorema dei seni e quando quello del coseno."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Quale Teorema Usare?", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        # Teorema dei seni
        h1 = Text("Teorema dei seni", font_size=26, color=GREEN_D, weight=BOLD)
        d1 = VGroup(
            Text("• un lato e l'angolo opposto", font_size=22, color=DARK_GRAY),
            Text("• più un altro angolo o lato", font_size=22, color=DARK_GRAY),
            Text("(casi ALA, AAL, SSA)", font_size=20, color=DARK_GRAY, slant=ITALIC),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        blocco1 = VGroup(h1, d1).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        # Teorema del coseno
        h2 = Text("Teorema del coseno", font_size=26, color=DARK_BLUE, weight=BOLD)
        d2 = VGroup(
            Text("• due lati e l'angolo compreso", font_size=22, color=DARK_GRAY),
            Text("• oppure tutti e tre i lati", font_size=22, color=DARK_GRAY),
            Text("(casi SAS, SSS)", font_size=20, color=DARK_GRAY, slant=ITALIC),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        blocco2 = VGroup(h2, d2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        blocchi = VGroup(blocco1, blocco2).arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        blocchi.next_to(title, DOWN, buff=0.9)

        self.play(FadeIn(h1))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in d1], lag_ratio=0.3))
        self.wait(0.6)
        self.play(FadeIn(h2))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in d2], lag_ratio=0.3))
        self.wait(0.8)

        nota = Text("Insieme risolvono qualsiasi triangolo",
                    font_size=24, color=GREEN_D, weight=BOLD, slant=ITALIC)
        nota.next_to(blocchi, DOWN, buff=0.8)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

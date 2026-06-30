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

    aA = MathTex(r"\alpha", color=GREEN_D, font_size=26).move_to(A + 0.65 * _norm(G - A))
    aB = MathTex(r"\beta", color=GREEN_D, font_size=26).move_to(B + 0.65 * _norm(G - B))
    aC = MathTex(r"\gamma", color=GREEN_D, font_size=26).move_to(C + 0.65 * _norm(G - C))

    mBC, mAC, mAB = (B + C) / 2, (A + C) / 2, (A + B) / 2
    la = MathTex("a", color=RED_D, font_size=26).move_to(mBC + 0.38 * _norm(mBC - G))
    lb = MathTex("b", color=BLUE_D, font_size=26).move_to(mAC + 0.38 * _norm(mAC - G))
    lc = MathTex("c", color=DARK_BLUE, font_size=26).move_to(mAB + 0.38 * _norm(mAB - G))

    return VGroup(tri, aA, aB, aC, la, lb, lc)


class CosaSignifica(Scene):
    """Risolvere un triangolo: trovare tutti e sei gli elementi."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Risolvere un Triangolo", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        defin = Text("trovare tutti i 6 elementi: 3 lati e 3 angoli",
                     font_size=23, color=DARK_BLUE)
        defin.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(defin))
        self.wait(0.4)

        A = np.array([-1.8, 0.8, 0.0])
        B = np.array([2.0, 0.5, 0.0])
        C = np.array([0.0, 2.6, 0.0])
        fig = triangolo_etichettato(A, B, C)
        self.play(Create(fig[0]), LaggedStart(*[Write(m) for m in fig[1:]], lag_ratio=0.1))
        self.wait(0.6)

        regola = MathTex(r"\alpha + \beta + \gamma = 180^\circ", color=BLACK, font_size=32)
        regola.next_to(fig, DOWN, buff=0.6)
        self.play(Write(regola))
        self.wait(0.6)

        h = Text("I quattro casi:", font_size=24, color=DARK_GRAY, weight=BOLD)
        casi = VGroup(
            Text("• due angoli e un lato → seni", font_size=21, color=DARK_GRAY),
            Text("• due lati e l'angolo compreso → coseno", font_size=21, color=DARK_GRAY),
            Text("• due lati e un angolo opposto → seni", font_size=21, color=DARK_GRAY),
            Text("• tre lati → coseno", font_size=21, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        gruppo = VGroup(h, casi).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        gruppo.next_to(regola, DOWN, buff=0.6)
        self.play(FadeIn(h))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in casi], lag_ratio=0.3))
        self.wait(2.5)


class CasoDueAngoliUnLato(Scene):
    """Caso ALA: noti un lato e due angoli, con il teorema dei seni."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Caso: due angoli e un lato", font_size=30, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"c = 14,\quad \alpha = 30^\circ,\quad \beta = 105^\circ",
                       color=DARK_BLUE, font_size=30)
        dati.next_to(title, DOWN, buff=0.5)
        self.play(Write(dati))
        self.wait(0.4)

        s0 = MathTex(r"\gamma = 180^\circ - 30^\circ - 105^\circ = 45^\circ",
                     color=BLACK, font_size=30)
        s0.next_to(dati, DOWN, buff=0.5)
        self.play(Write(s0))
        self.wait(0.5)

        s1 = MathTex(r"\dfrac{a}{\sin\alpha} = \dfrac{c}{\sin\gamma}", color=BLACK, font_size=32)
        s2 = MathTex(r"a = \dfrac{c\,\sin\alpha}{\sin\gamma}"
                     r" = \dfrac{14\,\sin 30^\circ}{\sin 45^\circ}", color=BLACK, font_size=30)
        s3 = MathTex(r"a = \dfrac{14\cdot\tfrac{1}{2}}{\tfrac{\sqrt{2}}{2}} = 7\sqrt{2}",
                     color=BLACK, font_size=30)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.45)
        passi.next_to(s0, DOWN, buff=0.6)
        for s in passi:
            self.play(Write(s))
            self.wait(0.3)

        ris = MathTex(r"a = 7\sqrt{2} \approx 9.9", color=GREEN_D, font_size=40)
        ris.next_to(passi, DOWN, buff=0.6)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.22,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        nota = Text("(b si trova allo stesso modo)", font_size=20,
                    color=DARK_GRAY, slant=ITALIC)
        nota.next_to(box, DOWN, buff=0.35)
        self.play(FadeIn(nota))
        self.wait(2.5)


class CasoDueLatiAngolo(Scene):
    """Caso SAS: noti due lati e l'angolo compreso, con il teorema del coseno."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Caso: due lati e l'angolo compreso", font_size=28,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"a = 8,\quad b = 5,\quad \gamma = 60^\circ",
                       color=DARK_BLUE, font_size=30)
        dati.next_to(title, DOWN, buff=0.5)
        self.play(Write(dati))
        self.wait(0.4)

        s1 = MathTex(r"c^2 = a^2 + b^2 - 2ab\,\cos\gamma", color=BLACK, font_size=30)
        s2 = MathTex(r"c^2 = 64 + 25 - 80\cdot\tfrac{1}{2} = 49", color=BLACK, font_size=30)
        s3 = MathTex(r"c = 7", color=GREEN_D, font_size=34)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.4)
        passi.next_to(dati, DOWN, buff=0.55)
        for s in passi:
            self.play(Write(s))
            self.wait(0.3)
        self.wait(0.3)

        # Trovo un angolo con il teorema dei seni
        h = Text("poi un angolo con i seni:", font_size=22, color=DARK_GRAY, weight=BOLD)
        h.next_to(passi, DOWN, buff=0.5)
        self.play(FadeIn(h))

        a1 = MathTex(r"\sin\alpha = \dfrac{a\,\sin\gamma}{c}"
                     r" = \dfrac{8\cdot\tfrac{\sqrt{3}}{2}}{7} \approx 0.99",
                     color=BLACK, font_size=28)
        a2 = MathTex(r"\alpha \approx 81.8^\circ, \quad \beta \approx 38.2^\circ",
                     color=BLACK, font_size=30)
        ang = VGroup(a1, a2).arrange(DOWN, buff=0.4)
        ang.next_to(h, DOWN, buff=0.4)
        self.play(Write(a1))
        self.play(Write(a2))
        box = SurroundingRectangle(VGroup(s3, ang), color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(2.5)


class CasoTreLati(Scene):
    """Caso SSS: noti i tre lati, con il teorema del coseno per gli angoli."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Caso: tre lati", font_size=30, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"a = 7,\quad b = 8,\quad c = 13", color=DARK_BLUE, font_size=32)
        dati.next_to(title, DOWN, buff=0.5)
        self.play(Write(dati))
        domanda = Text("Trovare gli angoli", font_size=23, color=DARK_GRAY, weight=BOLD)
        domanda.next_to(dati, DOWN, buff=0.4)
        self.play(FadeIn(domanda))
        self.wait(0.5)

        s1 = MathTex(r"\cos\gamma = \dfrac{a^2 + b^2 - c^2}{2ab}", color=BLACK, font_size=30)
        s2 = MathTex(r"\cos\gamma = \dfrac{49 + 64 - 169}{2\cdot 7\cdot 8}"
                     r" = \dfrac{-56}{112} = -\tfrac{1}{2}", color=BLACK, font_size=28)
        s3 = MathTex(r"\gamma = 120^\circ", color=GREEN_D, font_size=38)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.45)
        passi.next_to(domanda, DOWN, buff=0.6)
        for s in passi:
            self.play(Write(s))
            self.wait(0.3)

        box = SurroundingRectangle(s3, color=GREEN_D, buff=0.22,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        nota = VGroup(
            Text("Gli altri angoli con il teorema dei seni;", font_size=20, color=DARK_GRAY),
            Text("il terzo per differenza da 180°.", font_size=20, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.15)
        nota.next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class ProblemaReale(Scene):
    """Applicazione: distanza tra due punti separati da un lago."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Un Problema Reale", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        testo = VGroup(
            Text("Quanto distano due punti A e B", font_size=23, color=DARK_GRAY),
            Text("separati da un lago?", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.15)
        testo.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(testo))
        self.wait(0.4)

        # Figura: punto C, lago, A e B oltre il lago
        C = np.array([0.0, 0.3, 0.0])
        A = np.array([-2.2, 2.6, 0.0])
        B = np.array([2.2, 2.4, 0.0])
        lago = Ellipse(width=4.2, height=1.4, color=BLUE_D, fill_opacity=0.2,
                       stroke_width=2).move_to(np.array([0.0, 1.7, 0.0]))
        tri = Polygon(A, B, C, color=BLACK, stroke_width=3)
        dC = Dot(C, color=BLACK)
        dA = Dot(A, color=RED_D)
        dB = Dot(B, color=RED_D)
        lC = MathTex("C", font_size=24, color=BLACK).next_to(dC, DOWN, buff=0.1)
        lA = MathTex("A", font_size=24, color=RED_D).next_to(dA, UP, buff=0.1)
        lB = MathTex("B", font_size=24, color=RED_D).next_to(dB, UP, buff=0.1)
        l_ca = MathTex("80", font_size=22, color=DARK_BLUE).move_to((A + C) / 2 + LEFT * 0.4)
        l_cb = MathTex("100", font_size=22, color=DARK_BLUE).move_to((B + C) / 2 + RIGHT * 0.45)
        ang = MathTex(r"60^\circ", font_size=22, color=GREEN_D).next_to(dC, UP, buff=0.2)
        self.play(FadeIn(lago), Create(tri))
        self.play(FadeIn(dC), FadeIn(dA), FadeIn(dB), Write(lC), Write(lA), Write(lB))
        self.play(Write(l_ca), Write(l_cb), Write(ang))
        self.wait(0.6)

        # Risoluzione con il teorema del coseno
        s1 = MathTex(r"\overline{AB}^2 = 80^2 + 100^2 - 2\cdot 80\cdot 100\cdot\cos 60^\circ",
                     color=BLACK, font_size=26)
        s2 = MathTex(r"\overline{AB}^2 = 16400 - 8000 = 8400", color=BLACK, font_size=28)
        s3 = MathTex(r"\overline{AB} = \sqrt{8400} \approx 91.7\ \text{m}",
                     color=GREEN_D, font_size=34)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.4)
        passi.next_to(tri, DOWN, buff=0.7)
        self.play(Write(s1))
        self.play(Write(s2))
        self.play(Write(s3))
        box = SurroundingRectangle(s3, color=GREEN_D, buff=0.22,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)

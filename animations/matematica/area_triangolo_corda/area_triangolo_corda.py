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


def punto(center, R, angle):
    """Punto sulla circonferenza di centro `center` e raggio `R` all'angolo `angle`."""
    return center + R * np.array([np.cos(angle), np.sin(angle), 0])


class AreaTriangolo(Scene):
    """Area = 1/2 · a · b · sin(γ): due lati e l'angolo compreso."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Area di un Triangolo", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("con due lati e l'angolo compreso", font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        # Triangolo: base CA orizzontale, vertice B in alto
        gamma = 52 * DEGREES
        a_len = 3.4
        C = np.array([-2.0, 1.2, 0.0])
        A = np.array([2.2, 1.2, 0.0])
        B = C + a_len * np.array([np.cos(gamma), np.sin(gamma), 0.0])
        H = np.array([B[0], C[1], 0.0])

        tri = Polygon(C, A, B, color=BLACK, stroke_width=4)
        self.play(Create(tri))

        # Etichette dei lati e dei vertici
        lab_b = MathTex("b", color=DARK_BLUE, font_size=32).next_to(Line(C, A), DOWN, buff=0.15)
        lab_a = MathTex("a", color=RED_D, font_size=32).next_to(Line(C, B).get_center(),
                                                                UL, buff=0.1)
        self.play(Write(lab_b), Write(lab_a))

        # Angolo compreso γ in C
        ang = Arc(radius=0.55, start_angle=0, angle=gamma, arc_center=C,
                  color=GREEN_D, stroke_width=4)
        ang_lab = MathTex(r"\gamma", color=GREEN_D, font_size=30)
        ang_lab.move_to(C + 0.95 * np.array([np.cos(gamma / 2), np.sin(gamma / 2), 0]))
        self.play(Create(ang), Write(ang_lab))
        self.wait(0.4)

        # Altezza h = a·sin γ
        h_line = DashedLine(B, H, color=DARK_GRAY, stroke_width=3)
        sq = Square(side_length=0.28, color=DARK_GRAY, stroke_width=3)
        sq.move_to(H + LEFT * 0.14 + UP * 0.14)
        h_lab = MathTex(r"h = a\,\sin\gamma", color=DARK_GRAY, font_size=28)
        h_lab.next_to(h_line, RIGHT, buff=0.15)
        self.play(Create(h_line), Create(sq), Write(h_lab))
        self.wait(0.8)

        # Formula
        f1 = MathTex(r"A = \tfrac{1}{2}\,b\,h", color=BLACK, font_size=36)
        f2 = MathTex(r"A = \tfrac{1}{2}\,a\,b\,\sin\gamma", color=BLACK, font_size=44)
        formule = VGroup(f1, f2).arrange(DOWN, buff=0.45)
        formule.next_to(tri, DOWN, buff=1.2)
        self.play(Write(f1))
        self.wait(0.4)
        self.play(TransformMatchingShapes(f1.copy(), f2))
        box = SurroundingRectangle(f2, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)


class EsempioArea(Scene):
    """Esempio numerico del calcolo dell'area."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio: calcoliamo l'area", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"a = 6,\quad b = 8,\quad \gamma = 30^\circ",
                       color=DARK_BLUE, font_size=34)
        dati.next_to(title, DOWN, buff=0.6)
        self.play(Write(dati))
        self.wait(0.5)

        s1 = MathTex(r"A = \tfrac{1}{2}\,a\,b\,\sin\gamma", color=BLACK, font_size=36)
        s2 = MathTex(r"A = \tfrac{1}{2}\cdot 6 \cdot 8 \cdot \sin 30^\circ",
                     color=BLACK, font_size=34)
        s3 = MathTex(r"A = 24 \cdot \tfrac{1}{2}", color=BLACK, font_size=34)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.5)
        passi.next_to(dati, DOWN, buff=0.7)
        for s in passi:
            self.play(Write(s))
            self.wait(0.4)
        self.wait(0.4)

        ris = MathTex(r"A = 12", color=GREEN_D, font_size=52)
        ris.next_to(passi, DOWN, buff=0.7)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)


class TeoremaCorda(Scene):
    """Teorema della corda: AB = 2R·sin(γ)."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Teorema della Corda", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        # Circonferenza con centro
        R = 2.0
        center = UP * 1.4
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=3).move_to(center)
        dot_o = Dot(center, color=BLACK)
        o_lab = MathTex("O", color=BLACK, font_size=26).next_to(dot_o, DOWN, buff=0.1)
        self.play(Create(circle), FadeIn(dot_o), Write(o_lab))

        # Corda AB e angolo alla circonferenza in P
        aA, aB, aP = 205 * DEGREES, 335 * DEGREES, 75 * DEGREES
        A, Bp, P = punto(center, R, aA), punto(center, R, aB), punto(center, R, aP)
        corda = Line(A, Bp, color=RED_D, stroke_width=6)
        dA = Dot(A, color=BLACK)
        dB = Dot(Bp, color=BLACK)
        dP = Dot(P, color=BLACK)
        lA = MathTex("A", color=BLACK, font_size=26).next_to(dA, DL, buff=0.05)
        lB = MathTex("B", color=BLACK, font_size=26).next_to(dB, DR, buff=0.05)
        lP = MathTex("P", color=BLACK, font_size=26).next_to(dP, UP, buff=0.1)
        self.play(Create(corda), FadeIn(dA), FadeIn(dB), Write(lA), Write(lB))
        self.wait(0.3)

        # Angolo alla circonferenza in P che insiste su AB
        lpa = Line(P, A, color=BLACK, stroke_width=3)
        lpb = Line(P, Bp, color=BLACK, stroke_width=3)
        ang = Angle(Line(P, A), Line(P, Bp), radius=0.6, color=GREEN_D, stroke_width=4)
        ang_lab = MathTex(r"\gamma", color=GREEN_D, font_size=30)
        ang_lab.next_to(dP, DOWN, buff=0.35)
        self.play(Create(lpa), Create(lpb), FadeIn(dP), Write(lP))
        self.play(Create(ang), Write(ang_lab))
        self.wait(0.8)

        # Enunciato e formula
        testo = Text("corda = diametro × seno dell'angolo", font_size=22,
                     color=DARK_GRAY, slant=ITALIC)
        testo.next_to(circle, DOWN, buff=0.6)
        self.play(FadeIn(testo))

        formula = MathTex(r"\overline{AB} = 2R\,\sin\gamma", color=BLACK, font_size=44)
        formula.next_to(testo, DOWN, buff=0.5)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)


class EsempioCorda(Scene):
    """Esempio numerico con il teorema della corda."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio: lunghezza di una corda", font_size=30,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"R = 5,\quad \gamma = 30^\circ", color=DARK_BLUE, font_size=34)
        dati.next_to(title, DOWN, buff=0.6)
        self.play(Write(dati))
        self.wait(0.5)

        s1 = MathTex(r"\overline{AB} = 2R\,\sin\gamma", color=BLACK, font_size=36)
        s2 = MathTex(r"\overline{AB} = 2 \cdot 5 \cdot \sin 30^\circ", color=BLACK, font_size=34)
        s3 = MathTex(r"\overline{AB} = 10 \cdot \tfrac{1}{2}", color=BLACK, font_size=34)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.5)
        passi.next_to(dati, DOWN, buff=0.7)
        for s in passi:
            self.play(Write(s))
            self.wait(0.4)
        self.wait(0.4)

        ris = MathTex(r"\overline{AB} = 5", color=GREEN_D, font_size=52)
        ris.next_to(passi, DOWN, buff=0.7)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)


class Riepilogo(Scene):
    """Le due formule a confronto: entrambe usano il seno."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Riepilogo", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        h1 = Text("Area del triangolo", font_size=26, color=DARK_BLUE, weight=BOLD)
        f1 = MathTex(r"A = \tfrac{1}{2}\,a\,b\,\sin\gamma", color=BLACK, font_size=40)
        blocco1 = VGroup(h1, f1).arrange(DOWN, buff=0.3)

        h2 = Text("Teorema della corda", font_size=26, color=DARK_BLUE, weight=BOLD)
        f2 = MathTex(r"\overline{AB} = 2R\,\sin\gamma", color=BLACK, font_size=40)
        blocco2 = VGroup(h2, f2).arrange(DOWN, buff=0.3)

        blocchi = VGroup(blocco1, blocco2).arrange(DOWN, buff=1.1)
        blocchi.next_to(title, DOWN, buff=0.9)

        box1 = SurroundingRectangle(f1, color=GREEN_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)
        box2 = SurroundingRectangle(f2, color=GREEN_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)

        self.play(FadeIn(h1), Write(f1), Create(box1))
        self.wait(0.6)
        self.play(FadeIn(h2), Write(f2), Create(box2))
        self.wait(0.8)

        nota = Text("In entrambe compare il seno di un angolo", font_size=23,
                    color=GREEN_D, weight=BOLD, slant=ITALIC)
        nota.next_to(blocchi, DOWN, buff=0.9)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

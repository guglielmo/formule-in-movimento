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


def estremo_aperto(p, color):
    """Pallino vuoto per indicare un estremo escluso."""
    return Circle(radius=0.1, color=color, stroke_width=4,
                  fill_color=WHITE, fill_opacity=1).move_to(p)


class ComeSiRisolve(Scene):
    """Il metodo per risolvere una disequazione goniometrica."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Disequazioni Goniometriche", font_size=32,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("Come si risolvono", font_size=26, color=DARK_BLUE, weight=BOLD)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        passi = VGroup(
            Text("1. Risolvo l'equazione associata", font_size=26, color=DARK_GRAY),
            Text("    (trovo gli angoli di confine)", font_size=22, color=DARK_GRAY),
            Text("2. Segno gli archi sulla circonferenza", font_size=26, color=DARK_GRAY),
            Text("3. Leggo dove vale la disuguaglianza", font_size=26, color=DARK_GRAY),
            Text("4. Aggiungo il periodo", font_size=26, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        passi.next_to(subtitle, DOWN, buff=0.7)
        for p in passi:
            self.play(FadeIn(p, shift=RIGHT * 0.2))
            self.wait(0.2)
        self.wait(1)

        nota = VGroup(
            Text("Il segno della disequazione", font_size=23, color=GREEN_D, weight=BOLD),
            Text("indica QUALE arco prendere", font_size=23, color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        nota.next_to(passi, DOWN, buff=0.8)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class SenoMaggiore(Scene):
    """Disequazione sin x > 1/2: l'arco superiore della circonferenza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Disequazione: sin x > 1/2", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        R = 2.0
        center = UP * 1.3
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=3).move_to(center)
        cx = Line(center + LEFT * (R + 0.5), center + RIGHT * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        cy = Line(center + DOWN * (R + 0.5), center + UP * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        self.play(Create(cx), Create(cy), Create(circle))

        # Retta sin x = 1/2 (equazione associata)
        retta = DashedLine(center + LEFT * (R + 0.3) + UP * R * 0.5,
                           center + RIGHT * (R + 0.3) + UP * R * 0.5,
                           color=DARK_GRAY, stroke_width=2)
        self.play(Create(retta))

        # Angoli di confine π/6 e 5π/6 (esclusi)
        a1, a2 = PI / 6, 5 * PI / 6
        e1 = estremo_aperto(punto(center, R, a1), RED_D)
        e2 = estremo_aperto(punto(center, R, a2), RED_D)
        l1 = MathTex(r"\tfrac{\pi}{6}", color=BLACK, font_size=26).next_to(e1, UR, buff=0.05)
        l2 = MathTex(r"\tfrac{5\pi}{6}", color=BLACK, font_size=26).next_to(e2, UL, buff=0.05)
        self.play(FadeIn(e1), FadeIn(e2), Write(l1), Write(l2))

        # Arco soluzione: da π/6 a 5π/6 (dove l'altezza è > 1/2)
        arco = Arc(radius=R, start_angle=a1, angle=a2 - a1, arc_center=center,
                   color=GREEN_D, stroke_width=9)
        self.play(Create(arco))
        self.wait(0.4)
        nota = Text("l'arco dove l'altezza supera 1/2", font_size=21,
                    color=GREEN_D, slant=ITALIC)
        nota.next_to(circle, DOWN, buff=0.55)
        self.play(FadeIn(nota))
        self.wait(0.6)

        sol = MathTex(r"\tfrac{\pi}{6} + 2k\pi < x < \tfrac{5\pi}{6} + 2k\pi",
                      color=BLACK, font_size=32)
        sol.next_to(nota, DOWN, buff=0.5)
        self.play(Write(sol))
        box = SurroundingRectangle(sol, color=GREEN_D, buff=0.22,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(2.5)


class CosenoMinore(Scene):
    """Disequazione cos x < 1/2: l'arco di sinistra della circonferenza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Disequazione: cos x < 1/2", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        R = 2.0
        center = UP * 1.3
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=3).move_to(center)
        cx = Line(center + LEFT * (R + 0.5), center + RIGHT * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        cy = Line(center + DOWN * (R + 0.5), center + UP * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        self.play(Create(cx), Create(cy), Create(circle))

        # Retta verticale cos x = 1/2
        retta = DashedLine(center + RIGHT * R * 0.5 + DOWN * (R + 0.3),
                           center + RIGHT * R * 0.5 + UP * (R + 0.3),
                           color=DARK_GRAY, stroke_width=2)
        self.play(Create(retta))

        # Angoli di confine ±π/3 (esclusi)
        a1, a2 = PI / 3, -PI / 3
        e1 = estremo_aperto(punto(center, R, a1), BLUE_D)
        e2 = estremo_aperto(punto(center, R, a2), BLUE_D)
        l1 = MathTex(r"\tfrac{\pi}{3}", color=BLACK, font_size=26).next_to(e1, UR, buff=0.05)
        l2 = MathTex(r"\tfrac{5\pi}{3}", color=BLACK, font_size=26).next_to(e2, DR, buff=0.05)
        self.play(FadeIn(e1), FadeIn(e2), Write(l1), Write(l2))

        # Arco soluzione: da π/3 a 5π/3 (lato sinistro, ascissa < 1/2)
        arco = Arc(radius=R, start_angle=a1, angle=4 * PI / 3, arc_center=center,
                   color=GREEN_D, stroke_width=9)
        self.play(Create(arco))
        self.wait(0.4)
        nota = Text("l'arco dove l'ascissa è minore di 1/2", font_size=21,
                    color=GREEN_D, slant=ITALIC)
        nota.next_to(circle, DOWN, buff=0.55)
        self.play(FadeIn(nota))
        self.wait(0.6)

        sol = MathTex(r"\tfrac{\pi}{3} + 2k\pi < x < \tfrac{5\pi}{3} + 2k\pi",
                      color=BLACK, font_size=32)
        sol.next_to(nota, DOWN, buff=0.5)
        self.play(Write(sol))
        box = SurroundingRectangle(sol, color=GREEN_D, buff=0.22,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(2.5)


class TangenteMaggiore(Scene):
    """Disequazione tan x > 1, con periodo π."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Disequazione: tan x > 1", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        R = 1.9
        center = UP * 1.4
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=3).move_to(center)
        cx = Line(center + LEFT * (R + 0.5), center + RIGHT * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        cy = Line(center + DOWN * (R + 0.5), center + UP * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        self.play(Create(cx), Create(cy), Create(circle))

        # Confine: tan x = 1 -> π/4 (e 5π/4); asintoti a π/2 (e 3π/2)
        a_start1, a_end1 = PI / 4, PI / 2
        a_start2, a_end2 = 5 * PI / 4, 3 * PI / 2
        # Bisettrice (tan = 1)
        bis = Line(punto(center, R, 5 * PI / 4), punto(center, R, PI / 4),
                   color=DARK_GRAY, stroke_width=2)
        self.play(Create(bis))

        e1 = estremo_aperto(punto(center, R, a_start1), GREEN_D)
        e2 = estremo_aperto(punto(center, R, a_start2), GREEN_D)
        l1 = MathTex(r"\tfrac{\pi}{4}", color=BLACK, font_size=26).next_to(e1, UR, buff=0.05)
        l2 = MathTex(r"\tfrac{5\pi}{4}", color=BLACK, font_size=26).next_to(e2, DL, buff=0.05)
        self.play(FadeIn(e1), FadeIn(e2), Write(l1), Write(l2))

        # Due archi: (π/4, π/2) e (5π/4, 3π/2), asintoti esclusi
        arco1 = Arc(radius=R, start_angle=a_start1, angle=a_end1 - a_start1,
                    arc_center=center, color=GREEN_D, stroke_width=9)
        arco2 = Arc(radius=R, start_angle=a_start2, angle=a_end2 - a_start2,
                    arc_center=center, color=GREEN_D, stroke_width=9)
        self.play(Create(arco1), Create(arco2))
        self.wait(0.4)

        nota = Text("periodo π: gli archi si ripetono ogni mezzo giro", font_size=20,
                    color=DARK_GRAY, slant=ITALIC)
        nota.next_to(circle, DOWN, buff=0.55)
        self.play(FadeIn(nota))
        self.wait(0.5)

        sol = MathTex(r"\tfrac{\pi}{4} + k\pi < x < \tfrac{\pi}{2} + k\pi",
                      color=BLACK, font_size=32)
        sol.next_to(nota, DOWN, buff=0.5)
        self.play(Write(sol))
        box = SurroundingRectangle(sol, color=GREEN_D, buff=0.22,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(2.5)


class DisequazioneRiconducibile(Scene):
    """Disequazione di secondo grado riconducibile per sostituzione."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Disequazione Riconducibile", font_size=30, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        eq = MathTex(r"2\sin^2 x - \sin x - 1 \geq 0", color=BLACK, font_size=36)
        eq.next_to(title, DOWN, buff=0.55)
        self.play(Write(eq))
        self.wait(0.5)

        sost = MathTex(r"t = \sin x:\quad 2t^2 - t - 1 \geq 0", color=DARK_BLUE, font_size=32)
        sost.next_to(eq, DOWN, buff=0.5)
        self.play(Write(sost))
        self.wait(0.4)

        fatt = MathTex(r"(2t + 1)(t - 1) \geq 0", color=BLACK, font_size=32)
        fatt.next_to(sost, DOWN, buff=0.45)
        self.play(Write(fatt))

        # Studio del segno: parabola verso l'alto, >=0 esternamente
        segno = MathTex(r"t \leq -\tfrac{1}{2} \quad\lor\quad t \geq 1",
                        color=BLACK, font_size=32)
        segno.next_to(fatt, DOWN, buff=0.45)
        self.play(Write(segno))
        self.wait(0.7)

        # Ritorno a sin x
        ritorno = Text("Torno a sin x:", font_size=23, color=DARK_GRAY, weight=BOLD)
        ritorno.next_to(segno, DOWN, buff=0.55)
        self.play(FadeIn(ritorno))

        s1 = MathTex(r"\sin x \geq 1 \;\Rightarrow\; x = \tfrac{\pi}{2} + 2k\pi",
                     color=BLACK, font_size=28)
        s2 = MathTex(r"\sin x \leq -\tfrac{1}{2} \;\Rightarrow\; "
                     r"\tfrac{7\pi}{6} + 2k\pi \leq x \leq \tfrac{11\pi}{6} + 2k\pi",
                     color=BLACK, font_size=25)
        sols = VGroup(s1, s2).arrange(DOWN, buff=0.4)
        sols.next_to(ritorno, DOWN, buff=0.4)
        self.play(Write(s1))
        self.play(Write(s2))
        box = SurroundingRectangle(sols, color=GREEN_D, buff=0.22,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(2.5)

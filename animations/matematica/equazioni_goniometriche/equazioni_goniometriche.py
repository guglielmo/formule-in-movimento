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


class SenoElementare(Scene):
    """Equazione elementare sin x = 1/2 sulla circonferenza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Equazione: sin x = 1/2", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        # Circonferenza
        R = 2.0
        center = UP * 1.3
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        cx = Line(center + LEFT * (R + 0.5), center + RIGHT * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        cy = Line(center + DOWN * (R + 0.5), center + UP * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        self.play(Create(cx), Create(cy), Create(circle))

        # Retta orizzontale sin x = 1/2  (altezza y = R/2)
        k = 0.5
        retta = DashedLine(center + LEFT * (R + 0.4) + UP * R * k,
                           center + RIGHT * (R + 0.4) + UP * R * k,
                           color=RED_D, stroke_width=3)
        retta_lab = MathTex(r"\sin x = \tfrac{1}{2}", color=RED_D, font_size=28)
        retta_lab.next_to(retta, RIGHT, buff=0.1)
        self.play(Create(retta), Write(retta_lab))
        self.wait(0.4)

        # Due intersezioni: π/6 e 5π/6
        a1, a2 = PI / 6, 5 * PI / 6
        P1, P2 = punto(center, R, a1), punto(center, R, a2)
        d1, d2 = Dot(P1, color=RED_D), Dot(P2, color=RED_D)
        r1 = Line(center, P1, color=BLACK, stroke_width=3)
        r2 = Line(center, P2, color=BLACK, stroke_width=3)
        l1 = MathTex(r"\tfrac{\pi}{6}", color=BLACK, font_size=28).next_to(d1, UR, buff=0.05)
        l2 = MathTex(r"\tfrac{5\pi}{6}", color=BLACK, font_size=28).next_to(d2, UL, buff=0.05)
        self.play(Create(r1), Create(r2), FadeIn(d1), FadeIn(d2), Write(l1), Write(l2))
        self.wait(0.8)

        # Soluzione generale
        sol = VGroup(
            MathTex(r"x = \tfrac{\pi}{6} + 2k\pi", color=BLACK, font_size=32),
            MathTex(r"x = \tfrac{5\pi}{6} + 2k\pi", color=BLACK, font_size=32),
        ).arrange(DOWN, buff=0.35)
        sol.next_to(circle, DOWN, buff=0.7)
        self.play(Write(sol[0]))
        self.play(Write(sol[1]))
        box = SurroundingRectangle(sol, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        kappa = MathTex(r"k \in \mathbb{Z}", color=DARK_GRAY, font_size=26)
        kappa.next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(kappa))
        self.wait(2.5)


class CosenoElementare(Scene):
    """Equazione elementare cos x = 1/2 sulla circonferenza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Equazione: cos x = 1/2", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        R = 2.0
        center = UP * 1.3
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        cx = Line(center + LEFT * (R + 0.5), center + RIGHT * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        cy = Line(center + DOWN * (R + 0.5), center + UP * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        self.play(Create(cx), Create(cy), Create(circle))

        # Retta verticale cos x = 1/2 (ascissa x = R/2)
        k = 0.5
        retta = DashedLine(center + RIGHT * R * k + DOWN * (R + 0.4),
                           center + RIGHT * R * k + UP * (R + 0.4),
                           color=BLUE_D, stroke_width=3)
        retta_lab = MathTex(r"\cos x = \tfrac{1}{2}", color=BLUE_D, font_size=28)
        retta_lab.next_to(retta, UP, buff=0.1)
        self.play(Create(retta), Write(retta_lab))
        self.wait(0.4)

        # Due intersezioni simmetriche: ±π/3
        a1, a2 = PI / 3, -PI / 3
        P1, P2 = punto(center, R, a1), punto(center, R, a2)
        d1, d2 = Dot(P1, color=BLUE_D), Dot(P2, color=BLUE_D)
        r1 = Line(center, P1, color=BLACK, stroke_width=3)
        r2 = Line(center, P2, color=BLACK, stroke_width=3)
        l1 = MathTex(r"\tfrac{\pi}{3}", color=BLACK, font_size=28).next_to(d1, UR, buff=0.05)
        l2 = MathTex(r"-\tfrac{\pi}{3}", color=BLACK, font_size=28).next_to(d2, DR, buff=0.05)
        self.play(Create(r1), Create(r2), FadeIn(d1), FadeIn(d2), Write(l1), Write(l2))
        self.wait(0.8)

        sol = MathTex(r"x = \pm\tfrac{\pi}{3} + 2k\pi", color=BLACK, font_size=36)
        sol.next_to(circle, DOWN, buff=0.8)
        self.play(Write(sol))
        box = SurroundingRectangle(sol, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        kappa = MathTex(r"k \in \mathbb{Z}", color=DARK_GRAY, font_size=26)
        kappa.next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(kappa))
        self.wait(2.5)


class TangenteElementare(Scene):
    """Equazione elementare tan x = 1, con periodo π."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Equazione: tan x = 1", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        R = 1.9
        center = UP * 1.4
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        cx = Line(center + LEFT * (R + 0.5), center + RIGHT * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        cy = Line(center + DOWN * (R + 0.5), center + UP * (R + 0.5),
                  color=DARK_GRAY, stroke_width=1.5)
        self.play(Create(cx), Create(cy), Create(circle))

        # tan x = 1 -> due punti diametralmente opposti: π/4 e 5π/4
        a1, a2 = PI / 4, 5 * PI / 4
        P1, P2 = punto(center, R, a1), punto(center, R, a2)
        retta = Line(P2, P1, color=GREEN_D, stroke_width=4)
        d1, d2 = Dot(P1, color=GREEN_D), Dot(P2, color=GREEN_D)
        l1 = MathTex(r"\tfrac{\pi}{4}", color=BLACK, font_size=28).next_to(d1, UR, buff=0.05)
        l2 = MathTex(r"\tfrac{5\pi}{4}", color=BLACK, font_size=28).next_to(d2, DL, buff=0.05)
        self.play(Create(retta), FadeIn(d1), FadeIn(d2), Write(l1), Write(l2))
        self.wait(0.6)

        nota = Text("I due punti distano π: un solo periodo", font_size=22,
                    color=DARK_GRAY, slant=ITALIC)
        nota.next_to(circle, DOWN, buff=0.6)
        self.play(FadeIn(nota))
        self.wait(0.5)

        sol = MathTex(r"x = \tfrac{\pi}{4} + k\pi", color=BLACK, font_size=36)
        sol.next_to(nota, DOWN, buff=0.5)
        self.play(Write(sol))
        box = SurroundingRectangle(sol, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        kappa = MathTex(r"k \in \mathbb{Z}", color=DARK_GRAY, font_size=26)
        kappa.next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(kappa))
        self.wait(2.5)


class EquazioneRiconducibile(Scene):
    """Equazione di secondo grado riconducibile a elementari per sostituzione."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Equazione Riconducibile", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        eq = MathTex(r"2\sin^2 x - \sin x - 1 = 0", color=BLACK, font_size=38)
        eq.next_to(title, DOWN, buff=0.6)
        self.play(Write(eq))
        self.wait(0.6)

        # Sostituzione t = sin x
        sost = MathTex(r"\text{pongo } t = \sin x:\quad 2t^2 - t - 1 = 0",
                       color=DARK_BLUE, font_size=32)
        sost.next_to(eq, DOWN, buff=0.6)
        self.play(Write(sost))
        self.wait(0.6)

        # Risoluzione: (2t+1)(t-1)=0
        fatt = MathTex(r"(2t + 1)(t - 1) = 0", color=BLACK, font_size=32)
        fatt.next_to(sost, DOWN, buff=0.5)
        self.play(Write(fatt))
        radici = MathTex(r"t = -\tfrac{1}{2} \quad\lor\quad t = 1", color=BLACK, font_size=32)
        radici.next_to(fatt, DOWN, buff=0.45)
        self.play(Write(radici))
        self.wait(0.8)

        # Torno alla variabile x
        ritorno = Text("Torno a sin x:", font_size=24, color=DARK_GRAY, weight=BOLD)
        ritorno.next_to(radici, DOWN, buff=0.6)
        self.play(FadeIn(ritorno))

        s1 = MathTex(r"\sin x = 1 \;\Rightarrow\; x = \tfrac{\pi}{2} + 2k\pi",
                     color=BLACK, font_size=30)
        s2 = MathTex(r"\sin x = -\tfrac{1}{2} \;\Rightarrow\; "
                     r"x = \tfrac{7\pi}{6} + 2k\pi \;\lor\; x = \tfrac{11\pi}{6} + 2k\pi",
                     color=BLACK, font_size=26)
        sols = VGroup(s1, s2).arrange(DOWN, buff=0.4)
        sols.next_to(ritorno, DOWN, buff=0.4)
        self.play(Write(s1))
        self.play(Write(s2))
        box = SurroundingRectangle(sols, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(2.5)


class SchemaRiepilogo(Scene):
    """Schema riassuntivo delle equazioni elementari."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Schema Riassuntivo", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        header = [r"\text{equazione}", r"\text{soluzioni}"]
        rows = [
            [r"\sin x = k", r"x = \alpha + 2k\pi \,\lor\, x = \pi - \alpha + 2k\pi"],
            [r"\cos x = k", r"x = \pm\alpha + 2k\pi"],
            [r"\tan x = k", r"x = \alpha + k\pi"],
        ]
        table = MobjectTable(
            [[MathTex(c, font_size=26, color=BLACK) for c in row] for row in rows],
            col_labels=[MathTex(h, font_size=28, color=DARK_BLUE) for h in header],
            include_outer_lines=True,
            line_config={"color": DARK_GRAY, "stroke_width": 2},
        )
        table.scale_to_fit_width(7.4)
        table.next_to(title, DOWN, buff=0.8)
        colori = [RED_D, BLUE_D, GREEN_D]
        for i, col in enumerate(colori):
            table.get_rows()[i + 1][0].set_color(col)

        self.play(Create(table.get_horizontal_lines()),
                  Create(table.get_vertical_lines()))
        self.play(Write(table.get_labels()))
        self.play(LaggedStart(
            *[Write(table.get_rows()[i + 1]) for i in range(len(rows))],
            lag_ratio=0.3, run_time=3,
        ))
        self.wait(1.0)

        nota = VGroup(
            MathTex(r"\alpha = \arcsin k,\ \arccos k,\ \arctan k", color=DARK_GRAY, font_size=26),
            Text("Le altre equazioni si riconducono a queste", font_size=22,
                 color=GREEN_D, weight=BOLD, slant=ITALIC),
        ).arrange(DOWN, buff=0.3)
        nota.next_to(table, DOWN, buff=0.6)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

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


class CirconferenzaGoniometrica(Scene):
    """Seno e coseno come coordinate del punto sulla circonferenza unitaria."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Seno e Coseno", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("Le coordinate sulla circonferenza unitaria",
                        font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.4)

        # Sistema di riferimento e circonferenza di raggio 1 (R = unità grafica)
        R = 2.2
        center = UP * 1.2
        x_axis = Line(center + LEFT * (R + 0.7), center + RIGHT * (R + 0.7),
                      color=DARK_GRAY, stroke_width=2)
        y_axis = Line(center + DOWN * (R + 0.7), center + UP * (R + 0.7),
                      color=DARK_GRAY, stroke_width=2)
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        self.play(Create(x_axis), Create(y_axis))
        self.play(Create(circle))
        self.wait(0.3)

        # Punto P all'angolo alpha
        alpha = 52 * DEGREES
        P = punto(center, R, alpha)
        radius = Line(center, P, color=BLACK, stroke_width=5)
        dot = Dot(P, color=BLACK)
        # Angolo al centro
        ang = Arc(radius=0.55, start_angle=0, angle=alpha, arc_center=center,
                  color=GREEN_D, stroke_width=4)
        ang_lab = MathTex(r"\alpha", color=GREEN_D, font_size=32)
        ang_lab.move_to(center + 1.0 * np.array([np.cos(alpha / 2), np.sin(alpha / 2), 0]))
        p_lab = MathTex("P", color=BLACK, font_size=32).next_to(dot, UR, buff=0.1)
        self.play(Create(radius), FadeIn(dot), Create(ang), Write(ang_lab), Write(p_lab))
        self.wait(0.6)

        # Proiezioni: coseno sull'asse x, seno sull'asse y
        Px = np.array([P[0], center[1], 0])  # piede sull'asse x
        Py = np.array([center[0], P[1], 0])  # piede sull'asse y

        cos_seg = Line(center, Px, color=BLUE_D, stroke_width=7)
        sin_seg = Line(center, Py, color=RED_D, stroke_width=7)
        proj_v = DashedLine(P, Px, color=BLUE_D, stroke_width=3)
        proj_h = DashedLine(P, Py, color=RED_D, stroke_width=3)

        self.play(Create(proj_v), Create(cos_seg))
        cos_lab = MathTex(r"\cos\alpha", color=BLUE_D, font_size=30)
        cos_lab.next_to(cos_seg, DOWN, buff=0.2)
        self.play(Write(cos_lab))
        self.wait(0.4)

        self.play(Create(proj_h), Create(sin_seg))
        sin_lab = MathTex(r"\sin\alpha", color=RED_D, font_size=30)
        sin_lab.next_to(sin_seg, LEFT, buff=0.2)
        self.play(Write(sin_lab))
        self.wait(0.8)

        # Definizione: le coordinate di P
        defin = MathTex(r"P = (\,", r"\cos\alpha", r",\,", r"\sin\alpha", r"\,)",
                        font_size=44)
        defin.set_color(BLACK)
        defin[1].set_color(BLUE_D)
        defin[3].set_color(RED_D)
        defin.next_to(circle, DOWN, buff=0.9)
        self.play(Write(defin))
        box = SurroundingRectangle(defin, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(1.5)

        nota = Text("Coseno → ascissa,  Seno → ordinata", font_size=23,
                    color=DARK_GRAY, slant=ITALIC)
        nota.next_to(defin, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class SenoCosenoInMovimento(Scene):
    """Al variare dell'angolo, seno e coseno oscillano tra -1 e 1."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Al variare dell'angolo", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        R = 2.0
        center = UP * 1.3
        x_axis = Line(center + LEFT * (R + 0.6), center + RIGHT * (R + 0.6),
                      color=DARK_GRAY, stroke_width=2)
        y_axis = Line(center + DOWN * (R + 0.6), center + UP * (R + 0.6),
                      color=DARK_GRAY, stroke_width=2)
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        self.play(Create(x_axis), Create(y_axis), Create(circle))

        # Tracker dell'angolo
        theta = ValueTracker(35 * DEGREES)

        radius = always_redraw(
            lambda: Line(center, punto(center, R, theta.get_value()),
                         color=BLACK, stroke_width=5)
        )
        dot = always_redraw(
            lambda: Dot(punto(center, R, theta.get_value()), color=BLACK)
        )
        cos_seg = always_redraw(
            lambda: Line(
                center,
                np.array([punto(center, R, theta.get_value())[0], center[1], 0]),
                color=BLUE_D, stroke_width=7,
            )
        )
        sin_seg = always_redraw(
            lambda: Line(
                np.array([punto(center, R, theta.get_value())[0], center[1], 0]),
                punto(center, R, theta.get_value()),
                color=RED_D, stroke_width=7,
            )
        )
        self.play(Create(radius), FadeIn(dot), Create(cos_seg), Create(sin_seg))

        # Valori numerici aggiornati in tempo reale
        cos_val = always_redraw(
            lambda: MathTex(
                r"\cos\alpha = " + f"{np.cos(theta.get_value()):.2f}",
                color=BLUE_D, font_size=34,
            ).next_to(circle, DOWN, buff=0.8)
        )
        sin_val = always_redraw(
            lambda: MathTex(
                r"\sin\alpha = " + f"{np.sin(theta.get_value()):.2f}",
                color=RED_D, font_size=34,
            ).next_to(cos_val, DOWN, buff=0.35)
        )
        self.play(FadeIn(cos_val), FadeIn(sin_val))
        self.wait(0.5)

        # Giro completo: i valori oscillano tra -1 e 1
        self.play(theta.animate.set_value(35 * DEGREES + TAU),
                  run_time=6, rate_func=linear)
        self.wait(0.5)

        nota = VGroup(
            Text("Entrambi restano sempre", font_size=23, color=DARK_GRAY),
            MathTex(r"-1 \leq \sin\alpha,\ \cos\alpha \leq 1",
                    color=BLACK, font_size=34),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(sin_val, DOWN, buff=0.55)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class Tangente(Scene):
    """La tangente: rapporto seno/coseno e segmento sulla retta x = 1."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("La Tangente", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        # Definizione come rapporto
        defin = MathTex(r"\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha}",
                        color=BLACK, font_size=46)
        defin.next_to(title, DOWN, buff=0.5)
        self.play(Write(defin))
        self.wait(1)

        # Interpretazione geometrica
        R = 1.9
        center = DOWN * 0.3
        x_axis = Line(center + LEFT * (R + 0.5), center + RIGHT * (R + 1.7),
                      color=DARK_GRAY, stroke_width=2)
        y_axis = Line(center + DOWN * (R + 0.5), center + UP * (R + 1.6),
                      color=DARK_GRAY, stroke_width=2)
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        self.play(Create(x_axis), Create(y_axis), Create(circle))

        # Retta tangente verticale x = 1 (cioè a distanza R dal centro)
        tan_line = DashedLine(center + RIGHT * R + DOWN * (R + 0.3),
                              center + RIGHT * R + UP * (R + 1.5),
                              color=DARK_GRAY, stroke_width=2)
        self.play(Create(tan_line))

        # Angolo e raggio prolungato fino alla retta x = 1
        alpha = 40 * DEGREES
        P = punto(center, R, alpha)
        # Intersezione della retta OP con x = 1: y = R * tan(alpha)
        T = center + RIGHT * R + UP * (R * np.tan(alpha))
        ray = Line(center, T, color=BLACK, stroke_width=5)
        dotP = Dot(P, color=BLACK)
        ang = Arc(radius=0.5, start_angle=0, angle=alpha, arc_center=center,
                  color=GREEN_D, stroke_width=4)
        ang_lab = MathTex(r"\alpha", color=GREEN_D, font_size=30)
        ang_lab.move_to(center + 0.9 * np.array([np.cos(alpha / 2), np.sin(alpha / 2), 0]))
        self.play(Create(ray), FadeIn(dotP), Create(ang), Write(ang_lab))

        # Il segmento della tangente sulla retta x = 1
        tan_seg = Line(center + RIGHT * R, T, color=GREEN_D, stroke_width=8)
        tan_lab = MathTex(r"\tan\alpha", color=GREEN_D, font_size=30)
        tan_lab.next_to(tan_seg, RIGHT, buff=0.2)
        self.play(Create(tan_seg), Write(tan_lab))
        self.wait(1)

        nota = VGroup(
            Text("Non esiste quando cos α = 0", font_size=22, color=DARK_GRAY),
            MathTex(r"\alpha = 90^\circ,\ 270^\circ \ \dots", color=BLACK, font_size=30),
        ).arrange(DOWN, buff=0.2)
        nota.next_to(circle, DOWN, buff=0.6)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class RelazioneFondamentale(Scene):
    """sin²α + cos²α = 1 dal teorema di Pitagora sulla circonferenza unitaria."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Relazione Fondamentale", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("Pitagora sulla circonferenza unitaria",
                        font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        R = 2.1
        center = UP * 1.1
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        self.play(Create(circle))

        # Triangolo rettangolo: raggio (1), coseno (cateto orizz.), seno (cateto vert.)
        alpha = 48 * DEGREES
        P = punto(center, R, alpha)
        Px = np.array([P[0], center[1], 0])

        cos_seg = Line(center, Px, color=BLUE_D, stroke_width=7)
        sin_seg = Line(Px, P, color=RED_D, stroke_width=7)
        ipot = Line(center, P, color=BLACK, stroke_width=5)
        dot = Dot(P, color=BLACK)
        # Angolo retto
        sq = Square(side_length=0.3, color=DARK_GRAY, stroke_width=3)
        sq.move_to(Px + LEFT * 0.15 + UP * 0.15)

        cos_lab = MathTex(r"\cos\alpha", color=BLUE_D, font_size=28).next_to(cos_seg, DOWN, buff=0.15)
        sin_lab = MathTex(r"\sin\alpha", color=RED_D, font_size=28).next_to(sin_seg, RIGHT, buff=0.15)
        ipo_lab = MathTex(r"1", color=BLACK, font_size=30)
        ipo_lab.move_to(center + 0.55 * (P - center) + UP * 0.3 + LEFT * 0.25)

        self.play(Create(ipot), FadeIn(dot), Write(ipo_lab))
        self.play(Create(cos_seg), Write(cos_lab))
        self.play(Create(sin_seg), Write(sin_lab), Create(sq))
        self.wait(1)

        # Teorema di Pitagora -> relazione fondamentale
        pit = MathTex(r"\cos^2\alpha + \sin^2\alpha = 1", font_size=46)
        pit.set_color(BLACK)
        pit.next_to(circle, DOWN, buff=0.85)
        self.play(Write(pit))
        box = SurroundingRectangle(pit, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(1.5)

        nota = Text("Vale per ogni angolo α", font_size=24, color=DARK_GRAY,
                    slant=ITALIC, weight=BOLD)
        nota.next_to(pit, DOWN, buff=0.55)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class ValoriNotevoli(Scene):
    """Tabella dei valori di seno, coseno e tangente per gli angoli notevoli."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Valori Notevoli", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.4)

        # Intestazioni e righe della tabella
        header = [r"\alpha", r"\sin\alpha", r"\cos\alpha", r"\tan\alpha"]
        rows = [
            [r"0^\circ", r"0", r"1", r"0"],
            [r"30^\circ", r"\tfrac{1}{2}", r"\tfrac{\sqrt{3}}{2}", r"\tfrac{\sqrt{3}}{3}"],
            [r"45^\circ", r"\tfrac{\sqrt{2}}{2}", r"\tfrac{\sqrt{2}}{2}", r"1"],
            [r"60^\circ", r"\tfrac{\sqrt{3}}{2}", r"\tfrac{1}{2}", r"\sqrt{3}"],
            [r"90^\circ", r"1", r"0", r"\nexists"],
        ]

        table = MobjectTable(
            [[MathTex(c, font_size=30, color=BLACK) for c in row] for row in rows],
            col_labels=[MathTex(h, font_size=32, color=DARK_BLUE) for h in header],
            include_outer_lines=True,
            line_config={"color": DARK_GRAY, "stroke_width": 2},
        )
        table.scale_to_fit_width(6.8)
        table.next_to(title, DOWN, buff=0.7)
        # Disegno la griglia, le intestazioni e poi le righe una a una
        self.play(Create(table.get_horizontal_lines()),
                  Create(table.get_vertical_lines()))
        self.play(Write(table.get_labels()))
        self.wait(0.3)
        self.play(LaggedStart(
            *[Write(table.get_rows()[i + 1]) for i in range(len(rows))],
            lag_ratio=0.3, run_time=3,
        ))
        self.wait(1.5)

        nota = VGroup(
            Text("Da ricordare a memoria!", font_size=26, color=GREEN_D, weight=BOLD),
            MathTex(r"\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha}",
                    color=DARK_GRAY, font_size=32),
        ).arrange(DOWN, buff=0.3)
        nota.next_to(table, DOWN, buff=0.7)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

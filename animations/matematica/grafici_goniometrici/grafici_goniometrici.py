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


def etichette_pi(ax, valori, y_buff=0.25):
    """Etichette in multipli di π posizionate sotto l'asse x degli `ax`."""
    grp = VGroup()
    for x, tex in valori:
        lab = MathTex(tex, color=DARK_GRAY, font_size=26)
        lab.next_to(ax.c2p(x, 0), DOWN, buff=y_buff)
        grp.add(lab)
    return grp


class GraficoSeno(Scene):
    """Il grafico del seno dedotto dalla circonferenza unitaria."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Il Grafico del Seno", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        # Circonferenza unitaria in alto
        cR = 1.25
        cc = UP * 3.7
        circle = Circle(radius=cR, color=DARK_GRAY, stroke_width=3).move_to(cc)
        cx = Line(cc + LEFT * (cR + 0.3), cc + RIGHT * (cR + 0.3),
                  color=DARK_GRAY, stroke_width=1.5)
        cy = Line(cc + DOWN * (cR + 0.3), cc + UP * (cR + 0.3),
                  color=DARK_GRAY, stroke_width=1.5)
        self.play(Create(cx), Create(cy), Create(circle))

        # Assi del grafico: x da 0 a 2π, y da -1.5 a 1.5
        ax = Axes(
            x_range=[0, 2 * PI + 0.3, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=6.8,
            y_length=2.8,
            axis_config={"color": DARK_BLUE, "include_tip": True, "stroke_width": 2},
            tips=True,
        )
        ax.move_to(DOWN * 2.0)
        x_labels = etichette_pi(ax, [
            (PI / 2, r"\tfrac{\pi}{2}"), (PI, r"\pi"),
            (3 * PI / 2, r"\tfrac{3\pi}{2}"), (2 * PI, r"2\pi"),
        ])
        self.play(Create(ax), Write(x_labels))

        # Tracker dell'angolo
        t = ValueTracker(0.0)

        cdot = always_redraw(
            lambda: Dot(cc + cR * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]),
                        color=RED_D, radius=0.06)
        )
        cradius = always_redraw(
            lambda: Line(cc, cc + cR * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]),
                         color=BLACK, stroke_width=3)
        )
        # Proiezione verticale = seno
        cproj = always_redraw(
            lambda: Line(
                cc + cR * np.cos(t.get_value()) * RIGHT,
                cc + cR * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]),
                color=RED_D, stroke_width=5,
            )
        )
        # Curva del seno che cresce con t
        curva = always_redraw(
            lambda: ax.plot(np.sin, x_range=[0, max(t.get_value(), 0.001)],
                            color=RED_D, stroke_width=5)
        )
        gdot = always_redraw(
            lambda: Dot(ax.c2p(t.get_value(), np.sin(t.get_value())),
                        color=RED_D, radius=0.06)
        )
        self.play(Create(cradius), FadeIn(cdot), Create(cproj))
        self.add(curva, gdot)
        self.wait(0.3)

        # Un giro completo: la curva si disegna
        self.play(t.animate.set_value(2 * PI), run_time=7, rate_func=linear)
        self.wait(0.5)

        # Caratteristiche
        nota = VGroup(
            MathTex(r"y = \sin x", color=RED_D, font_size=36),
            Text("periodo 2π,  valori in [−1, 1]", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(ax, DOWN, buff=0.6)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class GraficoCoseno(Scene):
    """Il grafico del coseno: un seno sfasato di π/2."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Il Grafico del Coseno", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        ax = Axes(
            x_range=[0, 2 * PI + 0.3, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=6.8,
            y_length=3.2,
            axis_config={"color": DARK_BLUE, "include_tip": True, "stroke_width": 2},
            tips=True,
        )
        ax.move_to(UP * 0.8)
        x_labels = etichette_pi(ax, [
            (PI / 2, r"\tfrac{\pi}{2}"), (PI, r"\pi"),
            (3 * PI / 2, r"\tfrac{3\pi}{2}"), (2 * PI, r"2\pi"),
        ])
        self.play(Create(ax), Write(x_labels))

        # Seno tratteggiato di riferimento
        seno = ax.plot(np.sin, x_range=[0, 2 * PI], color=RED_D, stroke_width=3)
        seno_dash = DashedVMobject(seno, num_dashes=40)
        seno_lab = MathTex(r"y=\sin x", color=RED_D, font_size=26)
        seno_lab.next_to(ax.c2p(2 * PI, 0), UR, buff=0.1)
        self.play(Create(seno_dash), Write(seno_lab))
        self.wait(0.4)

        # Coseno pieno
        coseno = ax.plot(np.cos, x_range=[0, 2 * PI], color=BLUE_D, stroke_width=5)
        self.play(Create(coseno), run_time=2.5)
        cos_lab = MathTex(r"y=\cos x", color=BLUE_D, font_size=30)
        cos_lab.next_to(ax.c2p(0, 1), UP, buff=0.15)
        self.play(Write(cos_lab))
        self.wait(0.8)

        # Relazione di sfasamento
        rel = MathTex(r"\cos x = \sin\!\left(x + \tfrac{\pi}{2}\right)",
                      color=BLACK, font_size=36)
        rel.next_to(ax, DOWN, buff=0.7)
        self.play(Write(rel))
        box = SurroundingRectangle(rel, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(1)

        nota = Text("Stessa forma del seno, anticipata di π/2",
                    font_size=22, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(rel, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class GraficoTangente(Scene):
    """Il grafico della tangente, con gli asintoti verticali."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Il Grafico della Tangente", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        ax = Axes(
            x_range=[-PI / 2 - 0.2, 3 * PI / 2 + 0.2, PI / 2],
            y_range=[-5, 5, 2],
            x_length=6.6,
            y_length=6.0,
            axis_config={"color": DARK_BLUE, "include_tip": True, "stroke_width": 2},
            tips=True,
        )
        ax.move_to(DOWN * 0.4)
        x_labels = etichette_pi(ax, [
            (-PI / 2, r"-\tfrac{\pi}{2}"), (PI / 2, r"\tfrac{\pi}{2}"),
            (PI, r"\pi"), (3 * PI / 2, r"\tfrac{3\pi}{2}"),
        ], y_buff=0.2)
        self.play(Create(ax), Write(x_labels))

        # Asintoti verticali dove cos x = 0
        asintoti = VGroup()
        for xa in (-PI / 2, PI / 2, 3 * PI / 2):
            asint = DashedLine(ax.c2p(xa, -5), ax.c2p(xa, 5),
                               color=DARK_GRAY, stroke_width=2)
            asintoti.add(asint)
        self.play(Create(asintoti))
        self.wait(0.3)

        # Rami della tangente (lontano dagli asintoti, per restare nel riquadro)
        d = 0.2  # tan(π/2 - 0.2) ≈ 5
        ramo1 = ax.plot(np.tan, x_range=[-PI / 2 + d, PI / 2 - d],
                        color=GREEN_D, stroke_width=5)
        ramo2 = ax.plot(np.tan, x_range=[PI / 2 + d, 3 * PI / 2 - d],
                        color=GREEN_D, stroke_width=5)
        self.play(Create(ramo1), run_time=1.8)
        self.play(Create(ramo2), run_time=1.8)
        tan_lab = MathTex(r"y=\tan x", color=GREEN_D, font_size=32)
        tan_lab.next_to(title, DOWN, buff=0.3)
        self.play(Write(tan_lab))
        self.wait(0.8)

        nota = VGroup(
            Text("Periodo π", font_size=24, color=DARK_GRAY, weight=BOLD),
            Text("Asintoti dove cos x = 0", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.2)
        nota.next_to(ax, DOWN, buff=0.45)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class PeriodicitaSimmetrie(Scene):
    """Periodicità e simmetrie delle funzioni goniometriche."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Periodicità e Simmetrie", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.4)

        # Periodicità
        h1 = Text("Periodicità", font_size=28, color=DARK_BLUE, weight=BOLD)
        h1.next_to(title, DOWN, buff=0.6)
        self.play(FadeIn(h1))
        p1 = MathTex(r"\sin(x + 2\pi) = \sin x", color=RED_D, font_size=34)
        p2 = MathTex(r"\cos(x + 2\pi) = \cos x", color=BLUE_D, font_size=34)
        p3 = MathTex(r"\tan(x + \pi) = \tan x", color=GREEN_D, font_size=34)
        per = VGroup(p1, p2, p3).arrange(DOWN, buff=0.35)
        per.next_to(h1, DOWN, buff=0.45)
        self.play(LaggedStart(Write(p1), Write(p2), Write(p3), lag_ratio=0.4))
        self.wait(1.2)

        # Simmetrie (parità)
        h2 = Text("Simmetrie", font_size=28, color=DARK_BLUE, weight=BOLD)
        h2.next_to(per, DOWN, buff=0.7)
        self.play(FadeIn(h2))

        s1 = MathTex(r"\sin(-x) = -\sin x", color=RED_D, font_size=34)
        s1_lab = Text("dispari (simmetria rispetto all'origine)",
                      font_size=20, color=DARK_GRAY)
        s2 = MathTex(r"\cos(-x) = \cos x", color=BLUE_D, font_size=34)
        s2_lab = Text("pari (simmetria rispetto all'asse y)",
                      font_size=20, color=DARK_GRAY)
        sim = VGroup(
            VGroup(s1, s1_lab).arrange(DOWN, buff=0.12),
            VGroup(s2, s2_lab).arrange(DOWN, buff=0.12),
        ).arrange(DOWN, buff=0.5)
        sim.next_to(h2, DOWN, buff=0.45)
        self.play(FadeIn(sim[0], shift=UP * 0.2))
        self.wait(0.6)
        self.play(FadeIn(sim[1], shift=UP * 0.2))
        self.wait(2.5)


class Caratteristiche(Scene):
    """Tabella riassuntiva: dominio, codominio e periodo."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Caratteristiche a Confronto", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.4)

        header = [r"", r"\text{dominio}", r"\text{codominio}", r"\text{periodo}"]
        rows = [
            [r"\sin x", r"\mathbb{R}", r"[-1,\,1]", r"2\pi"],
            [r"\cos x", r"\mathbb{R}", r"[-1,\,1]", r"2\pi"],
            [r"\tan x", r"x \neq \tfrac{\pi}{2}+k\pi", r"\mathbb{R}", r"\pi"],
        ]

        table = MobjectTable(
            [[MathTex(c, font_size=28, color=BLACK) for c in row] for row in rows],
            col_labels=[MathTex(h, font_size=30, color=DARK_BLUE) for h in header],
            include_outer_lines=True,
            line_config={"color": DARK_GRAY, "stroke_width": 2},
        )
        table.scale_to_fit_width(7.2)
        table.next_to(title, DOWN, buff=0.8)
        # Colora la prima colonna (i nomi delle funzioni)
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
        self.wait(1.5)

        nota = Text("Tre funzioni, una sola circonferenza",
                    font_size=24, color=GREEN_D, weight=BOLD, slant=ITALIC)
        nota.next_to(table, DOWN, buff=0.8)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

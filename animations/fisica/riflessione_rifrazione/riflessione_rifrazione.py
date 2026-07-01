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


def dir_ang(angle):
    """Versore (x, y, 0) all'angolo `angle` (in radianti)."""
    return np.array([np.cos(angle), np.sin(angle), 0.0])


class Riflessione(Scene):
    """Legge della riflessione: angolo di incidenza = angolo di riflessione."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("La Riflessione", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        O = UP * 1.6
        L = 2.3
        theta = 50 * DEGREES

        # Superficie riflettente e normale
        surface = Line(O + LEFT * 3, O + RIGHT * 3, color=BLACK, stroke_width=5)
        normal = DashedLine(O, O + UP * 2.6, color=DARK_GRAY, stroke_width=2)
        n_lab = Text("normale", font_size=20, color=DARK_GRAY).next_to(normal, UP, buff=0.1)
        self.play(Create(surface), Create(normal), Write(n_lab))
        self.wait(0.3)

        # Raggio incidente e riflesso
        inc_start = O + L * dir_ang(PI / 2 + theta)
        refl_end = O + L * dir_ang(PI / 2 - theta)
        incidente = Arrow(inc_start, O, color=RED_D, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.13)
        riflesso = Arrow(O, refl_end, color=BLUE_D, buff=0, stroke_width=5,
                         max_tip_length_to_length_ratio=0.13)
        i_lab = Text("incidente", font_size=20, color=RED_D).next_to(inc_start, LEFT, buff=0.1)
        r_lab = Text("riflesso", font_size=20, color=BLUE_D).next_to(refl_end, RIGHT, buff=0.1)
        self.play(GrowArrow(incidente), Write(i_lab))
        self.play(GrowArrow(riflesso), Write(r_lab))
        self.wait(0.4)

        # Angoli
        arc_i = Arc(radius=0.7, start_angle=PI / 2, angle=theta, arc_center=O,
                    color=RED_D, stroke_width=4)
        arc_r = Arc(radius=0.7, start_angle=PI / 2 - theta, angle=theta, arc_center=O,
                    color=BLUE_D, stroke_width=4)
        li = MathTex(r"\theta_i", color=RED_D, font_size=30).move_to(O + 1.1 * dir_ang(PI / 2 + theta / 2))
        lr = MathTex(r"\theta_r", color=BLUE_D, font_size=30).move_to(O + 1.1 * dir_ang(PI / 2 - theta / 2))
        self.play(Create(arc_i), Create(arc_r), Write(li), Write(lr))
        self.wait(0.8)

        # Legge
        legge = MathTex(r"\theta_i = \theta_r", color=BLACK, font_size=52)
        legge.next_to(surface, DOWN, buff=1.0)
        self.play(Write(legge))
        box = SurroundingRectangle(legge, color=GREEN_D, buff=0.28,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        nota = Text("Gli angoli si misurano dalla normale", font_size=21,
                    color=DARK_GRAY, slant=ITALIC)
        nota.next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class Rifrazione(Scene):
    """La rifrazione e la legge di Snell."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("La Rifrazione", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        O = UP * 1.4
        L = 2.3
        t1 = 45 * DEGREES
        n1, n2 = 1.0, 1.5
        t2 = np.arcsin(np.sin(t1) * n1 / n2)  # legge di Snell

        # Interfaccia: mezzo 1 sopra (aria), mezzo 2 sotto (acqua)
        acqua = Rectangle(width=6.4, height=2.6, color=BLUE_D, fill_opacity=0.12,
                          stroke_width=0).move_to(O + DOWN * 1.3)
        surface = Line(O + LEFT * 3.2, O + RIGHT * 3.2, color=BLACK, stroke_width=4)
        normal = DashedLine(O + DOWN * 2.2, O + UP * 2.2, color=DARK_GRAY, stroke_width=2)
        m1 = MathTex(r"n_1\ (\text{aria})", color=DARK_GRAY, font_size=24).move_to(O + UP * 1.6 + RIGHT * 2.0)
        m2 = MathTex(r"n_2\ (\text{acqua})", color=DARK_BLUE, font_size=24).move_to(O + DOWN * 1.9 + RIGHT * 1.8)
        self.play(FadeIn(acqua), Create(surface), Create(normal))
        self.play(Write(m1), Write(m2))
        self.wait(0.3)

        # Raggi: incidente (mezzo1) e rifratto (mezzo2, piega verso la normale)
        inc_start = O + L * dir_ang(PI / 2 + t1)
        rifr_end = O + L * dir_ang(-PI / 2 + t2)
        incidente = Arrow(inc_start, O, color=RED_D, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.13)
        rifratto = Arrow(O, rifr_end, color=RED_D, buff=0, stroke_width=5,
                         max_tip_length_to_length_ratio=0.13)
        self.play(GrowArrow(incidente))
        self.play(GrowArrow(rifratto))

        arc_1 = Arc(radius=0.7, start_angle=PI / 2, angle=t1, arc_center=O,
                    color=RED_D, stroke_width=4)
        arc_2 = Arc(radius=0.7, start_angle=-PI / 2, angle=t2, arc_center=O,
                    color=DARK_BLUE, stroke_width=4)
        l1 = MathTex(r"\theta_1", color=RED_D, font_size=30).move_to(O + 1.15 * dir_ang(PI / 2 + t1 / 2))
        l2 = MathTex(r"\theta_2", color=DARK_BLUE, font_size=30).move_to(O + 1.15 * dir_ang(-PI / 2 + t2 / 2))
        self.play(Create(arc_1), Create(arc_2), Write(l1), Write(l2))
        self.wait(0.8)

        # Legge di Snell
        snell = MathTex(r"n_1\,\sin\theta_1 = n_2\,\sin\theta_2", color=BLACK, font_size=42)
        snell.next_to(acqua, DOWN, buff=0.7)
        self.play(Write(snell))
        box = SurroundingRectangle(snell, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        nota = Text("Entrando in un mezzo più denso, il raggio si avvicina alla normale",
                    font_size=19, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(box, DOWN, buff=0.45)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class IndiceRifrazione(Scene):
    """L'indice di rifrazione n = c/v e i valori per alcuni mezzi."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("L'Indice di Rifrazione", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        formula = MathTex(r"n = \dfrac{c}{v}", color=BLACK, font_size=52)
        formula.next_to(title, DOWN, buff=0.6)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.28,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        legenda = VGroup(
            MathTex(r"c = \text{velocità della luce nel vuoto}", color=DARK_GRAY, font_size=24),
            MathTex(r"v = \text{velocità della luce nel mezzo}", color=DARK_GRAY, font_size=24),
        ).arrange(DOWN, buff=0.25)
        legenda.next_to(box, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(m) for m in legenda], lag_ratio=0.3))
        self.wait(0.6)

        # Tabella di valori
        mezzi = [("Vuoto / aria", "1,00"), ("Acqua", "1,33"),
                 ("Vetro", "1,50"), ("Diamante", "2,42")]
        righe = VGroup()
        for nome, val in mezzi:
            n = Text(nome, font_size=24, color=BLACK)
            v = Text(val, font_size=24, color=DARK_BLUE, weight=BOLD)
            righe.add(VGroup(n, v).arrange(RIGHT, buff=0.8))
        righe.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        righe.next_to(legenda, DOWN, buff=0.7)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in righe], lag_ratio=0.25))
        self.wait(0.8)

        nota = Text("n più grande → luce più lenta → maggiore deviazione",
                    font_size=20, color=GREEN_D, weight=BOLD, slant=ITALIC)
        nota.next_to(righe, DOWN, buff=0.6)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class RiflessioneTotale(Scene):
    """Riflessione totale e angolo limite."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Riflessione Totale", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("dal mezzo più denso a quello meno denso",
                        font_size=21, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        O = UP * 1.2
        L = 2.2
        # Oltre l'angolo limite: il raggio resta nel mezzo (riflessione totale)
        t = 60 * DEGREES

        acqua = Rectangle(width=6.4, height=2.4, color=BLUE_D, fill_opacity=0.12,
                          stroke_width=0).move_to(O + UP * 1.2)
        surface = Line(O + LEFT * 3.2, O + RIGHT * 3.2, color=BLACK, stroke_width=4)
        normal = DashedLine(O + DOWN * 2.0, O + UP * 2.0, color=DARK_GRAY, stroke_width=2)
        m1 = MathTex(r"n_1\ (\text{acqua})", color=DARK_BLUE, font_size=22).move_to(O + UP * 1.7 + RIGHT * 1.9)
        m2 = MathTex(r"n_2\ (\text{aria})", color=DARK_GRAY, font_size=22).move_to(O + DOWN * 1.6 + RIGHT * 1.9)
        self.play(FadeIn(acqua), Create(surface), Create(normal), Write(m1), Write(m2))

        # Raggio incidente dall'alto (nel mezzo denso) e raggio totalmente riflesso
        inc_start = O + L * dir_ang(PI / 2 + t)
        refl_end = O + L * dir_ang(PI / 2 - t)
        incidente = Arrow(inc_start, O, color=RED_D, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.13)
        riflesso = Arrow(O, refl_end, color=RED_D, buff=0, stroke_width=5,
                         max_tip_length_to_length_ratio=0.13)
        self.play(GrowArrow(incidente))
        self.play(GrowArrow(riflesso))
        self.wait(0.4)

        # Formula dell'angolo limite
        formula = MathTex(r"\sin\theta_L = \dfrac{n_2}{n_1}", color=BLACK, font_size=44)
        formula.next_to(surface, DOWN, buff=0.9)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        nota = VGroup(
            Text("Oltre l'angolo limite θ_L la luce è tutta riflessa",
                 font_size=20, color=DARK_GRAY),
            Text("È il principio delle fibre ottiche", font_size=20,
                 color=GREEN_D, weight=BOLD, slant=ITALIC),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class Applicazioni(Scene):
    """Riepilogo e applicazioni della riflessione e rifrazione."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Riepilogo e Applicazioni", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        leggi = VGroup(
            MathTex(r"\theta_i = \theta_r", color=BLACK, font_size=34),
            MathTex(r"n_1\,\sin\theta_1 = n_2\,\sin\theta_2", color=BLACK, font_size=34),
            MathTex(r"\sin\theta_L = \dfrac{n_2}{n_1}", color=BLACK, font_size=34),
        ).arrange(DOWN, buff=0.45)
        leggi.next_to(title, DOWN, buff=0.7)
        etich = VGroup(
            Text("riflessione", font_size=20, color=DARK_GRAY).next_to(leggi[0], RIGHT, buff=0.4),
            Text("rifrazione (Snell)", font_size=20, color=DARK_GRAY).next_to(leggi[1], RIGHT, buff=0.4),
            Text("angolo limite", font_size=20, color=DARK_GRAY).next_to(leggi[2], RIGHT, buff=0.4),
        )
        for f, e in zip(leggi, etich):
            self.play(Write(f), FadeIn(e))
            self.wait(0.2)
        self.wait(0.5)

        h = Text("Dove le incontriamo:", font_size=24, color=DARK_BLUE, weight=BOLD)
        app = VGroup(
            Text("• specchi e periscopi", font_size=22, color=DARK_GRAY),
            Text("• lenti e occhiali", font_size=22, color=DARK_GRAY),
            Text("• fibre ottiche", font_size=22, color=DARK_GRAY),
            Text("• miraggi e la cannuccia \"spezzata\"", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        gruppo = VGroup(h, app).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        gruppo.next_to(leggi, DOWN, buff=0.9)
        self.play(FadeIn(h))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in app], lag_ratio=0.3))
        self.wait(2.5)

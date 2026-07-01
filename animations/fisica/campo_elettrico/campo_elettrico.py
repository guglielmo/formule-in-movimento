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


def carica(segno, color, pos, radius=0.4, font_size=40):
    """Pallino con il simbolo + o − che rappresenta una carica."""
    c = Circle(radius=radius, color=color, fill_opacity=0.9, stroke_width=0).move_to(pos)
    simbolo = MathTex(segno, color=WHITE, font_size=font_size).move_to(pos)
    return VGroup(c, simbolo)


class CampoElettrico(Scene):
    """Il campo elettrico come forza per unità di carica: E = F/q."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Il Campo Elettrico", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("come una carica modifica lo spazio intorno a sé",
                        font_size=22, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        # Carica sorgente e carica di prova
        Q = carica("+", RED_D, LEFT * 1.8 + UP * 1.7)
        q = carica("+", GREEN_D, RIGHT * 1.4 + UP * 1.7, radius=0.28, font_size=30)
        Q_lab = MathTex("Q", color=RED_D, font_size=28).next_to(Q, DOWN, buff=0.2)
        q_lab = MathTex("q", color=GREEN_D, font_size=26).next_to(q, DOWN, buff=0.2)
        forza = Arrow(q.get_center(), q.get_center() + RIGHT * 1.2, color=DARK_GRAY,
                      buff=0.35, stroke_width=5)
        f_lab = MathTex(r"\vec{F}", color=DARK_GRAY, font_size=28).next_to(forza, UP, buff=0.1)
        self.play(FadeIn(Q, scale=0.5), Write(Q_lab))
        self.play(FadeIn(q, scale=0.5), Write(q_lab))
        self.play(GrowArrow(forza), Write(f_lab))
        self.wait(0.6)

        # Definizione
        defin = MathTex(r"\vec{E} = \dfrac{\vec{F}}{q}", color=BLACK, font_size=52)
        defin.next_to(Q, DOWN, buff=1.6).set_x(0)
        self.play(Write(defin))
        box = SurroundingRectangle(defin, color=GREEN_D, buff=0.3,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        unita = MathTex(r"[E] = \dfrac{\text{N}}{\text{C}}", color=DARK_BLUE, font_size=32)
        unita.next_to(box, DOWN, buff=0.45)
        self.play(Write(unita))
        self.wait(0.6)

        nota = VGroup(
            Text("Il campo esiste anche senza la carica di prova:", font_size=20, color=DARK_GRAY),
            Text("descrive lo spazio attorno alla sorgente Q", font_size=20,
                 color=GREEN_D, weight=BOLD, slant=ITALIC),
        ).arrange(DOWN, buff=0.2)
        nota.next_to(unita, DOWN, buff=0.55)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class CampoCaricaPuntiforme(Scene):
    """Il campo di una carica puntiforme: E = kQ/r², radiale."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Campo di una Carica Puntiforme", font_size=30,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        center = UP * 1.7
        Q = carica("+", RED_D, center)
        self.play(FadeIn(Q, scale=0.5))

        # Vettori campo radiali (uscenti)
        frecce = VGroup()
        for i in range(8):
            ang = i * 45 * DEGREES
            start = center + 0.5 * dir_ang(ang)
            end = center + 1.7 * dir_ang(ang)
            frecce.add(Arrow(start, end, color=DARK_BLUE, buff=0, stroke_width=4,
                             max_tip_length_to_length_ratio=0.3))
        self.play(LaggedStart(*[GrowArrow(f) for f in frecce], lag_ratio=0.1))
        self.wait(0.6)

        # La formula
        formula = MathTex(r"E = k\,\dfrac{Q}{r^2}", color=BLACK, font_size=50)
        formula.next_to(Q, DOWN, buff=2.1).set_x(0)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.28,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.5)

        nota = VGroup(
            Text("Il campo punta lontano dalle cariche positive", font_size=20, color=DARK_GRAY),
            Text("e verso le cariche negative", font_size=20, color=DARK_GRAY),
            Text("e diminuisce col quadrato della distanza", font_size=20,
                 color=GREEN_D, weight=BOLD, slant=ITALIC),
        ).arrange(DOWN, buff=0.2)
        nota.next_to(box, DOWN, buff=0.55)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class LineeDiCampo(Scene):
    """Le linee di campo: uscenti dal positivo, entranti nel negativo."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Le Linee di Campo", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        # Carica positiva: linee uscenti
        cp = LEFT * 1.9 + UP * 1.3
        Qp = carica("+", RED_D, cp, radius=0.32, font_size=32)
        linee_p = VGroup()
        for i in range(8):
            ang = i * 45 * DEGREES
            linee_p.add(Arrow(cp + 0.35 * dir_ang(ang), cp + 1.3 * dir_ang(ang),
                              color=DARK_BLUE, buff=0, stroke_width=3,
                              max_tip_length_to_length_ratio=0.35))
        lab_p = Text("uscenti", font_size=20, color=RED_D).next_to(Qp, DOWN, buff=1.15)

        # Carica negativa: linee entranti
        cn = RIGHT * 1.9 + UP * 1.3
        Qn = carica("-", BLUE_D, cn, radius=0.32, font_size=32)
        linee_n = VGroup()
        for i in range(8):
            ang = i * 45 * DEGREES
            linee_n.add(Arrow(cn + 1.3 * dir_ang(ang), cn + 0.35 * dir_ang(ang),
                              color=DARK_BLUE, buff=0, stroke_width=3,
                              max_tip_length_to_length_ratio=0.35))
        lab_n = Text("entranti", font_size=20, color=BLUE_D).next_to(Qn, DOWN, buff=1.15)

        self.play(FadeIn(Qp, scale=0.5), FadeIn(Qn, scale=0.5))
        self.play(LaggedStart(*[GrowArrow(f) for f in linee_p], lag_ratio=0.08),
                  LaggedStart(*[GrowArrow(f) for f in linee_n], lag_ratio=0.08))
        self.play(Write(lab_p), Write(lab_n))
        self.wait(0.8)

        # Le regole
        h = Text("Le regole:", font_size=24, color=DARK_GRAY, weight=BOLD)
        regole = VGroup(
            Text("• escono dal +, entrano nel −", font_size=22, color=DARK_GRAY),
            Text("• più fitte dove il campo è intenso", font_size=22, color=DARK_GRAY),
            Text("• non si incrociano mai", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        gruppo = VGroup(h, regole).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        gruppo.next_to(title, DOWN, buff=0.2).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(h))
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in regole], lag_ratio=0.3))
        self.wait(2.5)


class DipoloElettrico(Scene):
    """Le linee di campo di un dipolo elettrico."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Il Dipolo Elettrico", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("una carica + e una − vicine", font_size=22, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        # Le due cariche
        P = LEFT * 1.6 + DOWN * 0.3
        N = RIGHT * 1.6 + DOWN * 0.3
        Qp = carica("+", RED_D, P, radius=0.34, font_size=32)
        Qn = carica("-", BLUE_D, N, radius=0.34, font_size=32)
        self.play(FadeIn(Qp, scale=0.5), FadeIn(Qn, scale=0.5))

        # Linee di campo curve dal + al − (sopra, in asse, sotto)
        linee = VGroup()
        for angolo in (-2.4, -1.2, 0.0, 1.2, 2.4):
            arco = ArcBetweenPoints(P + 0.4 * RIGHT, N + 0.4 * LEFT, angle=angolo,
                                    color=DARK_BLUE, stroke_width=3)
            arco.add_tip(tip_length=0.18)
            linee.add(arco)
        self.play(LaggedStart(*[Create(l) for l in linee], lag_ratio=0.2))
        self.wait(0.8)

        nota = VGroup(
            Text("Le linee vanno sempre dal + al −", font_size=22,
                 color=GREEN_D, weight=BOLD),
            Text("curvandosi con continuità nello spazio", font_size=20,
                 color=DARK_GRAY, slant=ITALIC),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(Qp, DOWN, buff=1.9).set_x(0)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class ForzaSuCarica(Scene):
    """La forza su una carica immersa in un campo: F = qE. Riepilogo."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Forza su una Carica nel Campo", font_size=30,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        # Nota una carica q in un campo E
        formula = MathTex(r"\vec{F} = q\,\vec{E}", color=BLACK, font_size=56)
        formula.next_to(title, DOWN, buff=0.7)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.3,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.5)

        spieg = VGroup(
            Text("Nota il campo E, la forza su q è immediata.", font_size=21, color=DARK_GRAY),
            Text("Carica positiva → forza nel verso di E", font_size=21, color=RED_D),
            Text("Carica negativa → forza opposta a E", font_size=21, color=BLUE_D),
        ).arrange(DOWN, buff=0.25)
        spieg.next_to(box, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in spieg], lag_ratio=0.3))
        self.wait(0.8)

        # Riepilogo delle due lezioni
        h = Text("In sintesi:", font_size=24, color=DARK_BLUE, weight=BOLD)
        rec = VGroup(
            MathTex(r"F = k\,\dfrac{q_1 q_2}{r^2}", color=BLACK, font_size=32),
            MathTex(r"E = \dfrac{F}{q} = k\,\dfrac{Q}{r^2}", color=BLACK, font_size=32),
            MathTex(r"\vec{F} = q\,\vec{E}", color=BLACK, font_size=32),
        ).arrange(DOWN, buff=0.35)
        gruppo = VGroup(h, rec).arrange(DOWN, buff=0.35)
        gruppo.next_to(spieg, DOWN, buff=0.7)
        self.play(FadeIn(h))
        self.play(LaggedStart(*[Write(m) for m in rec], lag_ratio=0.3))
        self.wait(2.5)

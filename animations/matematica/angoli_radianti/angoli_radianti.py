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


class DefinizioneRadiante(Scene):
    """Che cos'è un radiante: l'angolo sotteso da un arco lungo come il raggio."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Il Radiante", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.4)

        subtitle = Text("L'angolo che misura l'arco", font_size=26, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.5)

        # Circonferenza con il suo centro
        R = 2.0
        center = UP * 1.0
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=4).move_to(center)
        dot = Dot(center, color=BLACK)
        self.play(Create(circle), FadeIn(dot))

        # Raggio orizzontale di riferimento
        r1 = Line(center, center + RIGHT * R, color=DARK_BLUE, stroke_width=5)
        r1_lab = MathTex("r", color=DARK_BLUE, font_size=34).next_to(r1, DOWN, buff=0.15)
        self.play(Create(r1), Write(r1_lab))
        self.wait(0.5)

        # Arco lungo quanto il raggio -> angolo di 1 radiante
        theta = 1.0  # 1 radiante (in radianti)
        arc = Arc(radius=R, start_angle=0, angle=theta, arc_center=center,
                  color=RED_D, stroke_width=8)
        r2 = Line(center, center + R * np.array([np.cos(theta), np.sin(theta), 0]),
                  color=DARK_BLUE, stroke_width=5)
        arc_lab = MathTex("r", color=RED_D, font_size=34)
        arc_lab.move_to(center + (R + 0.45) * np.array([np.cos(theta / 2), np.sin(theta / 2), 0]))
        self.play(Create(arc))
        self.play(Create(r2), Write(arc_lab))
        self.wait(0.4)

        # L'angolo al centro
        ang = Arc(radius=0.55, start_angle=0, angle=theta, arc_center=center,
                  color=GREEN_D, stroke_width=4)
        ang_lab = MathTex(r"1\,\text{rad}", color=GREEN_D, font_size=30)
        ang_lab.move_to(center + 1.25 * np.array([np.cos(theta / 2), np.sin(theta / 2), 0]))
        self.play(Create(ang), Write(ang_lab))
        self.wait(1)

        # Definizione a parole
        defin = VGroup(
            Text("Arco lungo come il raggio", font_size=24, color=BLACK),
            Text("= 1 radiante", font_size=28, color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.2)
        defin.next_to(circle, DOWN, buff=0.55)
        self.play(FadeIn(defin, shift=UP * 0.2))
        self.wait(1.5)

        # Il giro completo
        giro_lab = Text("Un giro completo:", font_size=24, color=BLACK)
        giro_eq = MathTex(r"360^\circ = 2\pi\,\text{rad}", color=DARK_BLUE, font_size=40)
        giro = VGroup(giro_lab, giro_eq).arrange(DOWN, buff=0.25)
        giro.next_to(defin, DOWN, buff=0.5)
        self.play(FadeIn(giro_lab))
        self.play(Write(giro_eq))
        box = SurroundingRectangle(giro_eq, color=DARK_BLUE, buff=0.25,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Create(box))
        self.wait(2.5)


class ConversioneGradiRadianti(Scene):
    """Dalla relazione 180° = π si ricavano le due formule di conversione."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Gradi e Radianti", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.4)

        # Relazione fondamentale
        rel = MathTex(r"180^\circ = \pi\,\text{rad}", color=DARK_BLUE, font_size=50)
        rel.next_to(title, DOWN, buff=0.5)
        self.play(Write(rel))
        rel_box = SurroundingRectangle(rel, color=DARK_BLUE, buff=0.25,
                                       corner_radius=0.15, stroke_width=4)
        self.play(Create(rel_box))
        self.wait(1)

        # Le due formule di conversione
        f_label = Text("Le due conversioni:", font_size=24, color=BLACK, weight=BOLD)
        f1 = MathTex(r"\alpha_{rad} = \alpha_{gradi}\cdot \dfrac{\pi}{180^\circ}",
                     color=BLACK, font_size=36)
        f2 = MathTex(r"\alpha_{gradi} = \alpha_{rad}\cdot \dfrac{180^\circ}{\pi}",
                     color=BLACK, font_size=36)
        formulas = VGroup(f_label, f1, f2).arrange(DOWN, buff=0.4)
        formulas.next_to(rel_box, DOWN, buff=0.6)
        self.play(FadeIn(f_label))
        self.play(Write(f1))
        self.play(Write(f2))
        self.wait(2)

        # Esempio concreto: 60°
        self.play(FadeOut(formulas))
        ex_label = Text("Esempio: converto 60°", font_size=26, color=DARK_BLUE, weight=BOLD)
        ex_label.next_to(rel_box, DOWN, buff=0.7)
        self.play(FadeIn(ex_label))

        ex = MathTex(r"60^\circ \cdot \dfrac{\pi}{180^\circ}", "=", r"\dfrac{\pi}{3}",
                     color=BLACK, font_size=44)
        ex[2].set_color(GREEN_D)
        ex.next_to(ex_label, DOWN, buff=0.5)
        self.play(Write(ex))
        ex_box = SurroundingRectangle(ex[2], color=GREEN_D, buff=0.2,
                                      corner_radius=0.15, stroke_width=4)
        self.play(Create(ex_box))
        self.wait(1.5)

        # Tabella degli angoli notevoli
        tab_title = Text("Angoli notevoli:", font_size=24, color=BLACK, weight=BOLD)
        tab_title.next_to(ex, DOWN, buff=0.7)
        self.play(FadeIn(tab_title))

        m30 = MathTex(r"30^\circ = \tfrac{\pi}{6}", color=BLACK, font_size=34)
        m45 = MathTex(r"45^\circ = \tfrac{\pi}{4}", color=BLACK, font_size=34)
        m90 = MathTex(r"90^\circ = \tfrac{\pi}{2}", color=BLACK, font_size=34)
        m360 = MathTex(r"360^\circ = 2\pi", color=BLACK, font_size=34)
        row1 = VGroup(m30, m45).arrange(RIGHT, buff=1.0)
        row2 = VGroup(m90, m360).arrange(RIGHT, buff=1.0)
        table = VGroup(row1, row2).arrange(DOWN, buff=0.5)
        table.next_to(tab_title, DOWN, buff=0.45)
        self.play(LaggedStart(*[Write(m) for m in (m30, m45, m90, m360)], lag_ratio=0.3))
        self.wait(2.5)


class ArcoESettore(Scene):
    """In radianti arco e area del settore hanno formule semplici."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Arco e Settore Circolare", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("Perché i radianti sono comodi", font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        # Circonferenza e settore
        R = 2.0
        center = UP * 1.2
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=3).move_to(center)
        self.play(Create(circle))

        start = 0.35
        theta = PI / 3  # ampiezza del settore (60°)
        sector = AnnularSector(outer_radius=R, inner_radius=0, angle=theta, start_angle=start,
                               arc_center=center, color=BLUE_D, fill_opacity=0.3, stroke_width=0)
        r1 = Line(center, center + R * np.array([np.cos(start), np.sin(start), 0]),
                  color=DARK_BLUE, stroke_width=4)
        r2 = Line(center, center + R * np.array([np.cos(start + theta), np.sin(start + theta), 0]),
                  color=DARK_BLUE, stroke_width=4)
        arc = Arc(radius=R, start_angle=start, angle=theta, arc_center=center,
                  color=RED_D, stroke_width=8)
        self.play(FadeIn(sector), Create(r1), Create(r2))
        self.play(Create(arc))

        # Angolo al centro e raggio
        ang = Arc(radius=0.5, start_angle=start, angle=theta, arc_center=center,
                  color=GREEN_D, stroke_width=4)
        ang_lab = MathTex(r"\theta", color=GREEN_D, font_size=34)
        ang_lab.move_to(center + 0.95 * np.array([np.cos(start + theta / 2), np.sin(start + theta / 2), 0]))
        r_lab = MathTex("r", color=DARK_BLUE, font_size=30).next_to(r1, DOWN, buff=0.1)
        self.play(Create(ang), Write(ang_lab), Write(r_lab))
        self.wait(1)

        # Le formule
        f1 = MathTex(r"\text{arco}:\quad \ell = r\,\theta", color=RED_D, font_size=40)
        f2 = MathTex(r"\text{settore}:\quad A = \tfrac{1}{2}\,r^{2}\,\theta", color=BLUE_D, font_size=40)
        formulas = VGroup(f1, f2).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        formulas.next_to(circle, DOWN, buff=0.8)
        self.play(Write(f1))
        self.wait(0.5)
        self.play(Write(f2))
        self.wait(1)

        nota = Text("θ va espresso in radianti!", font_size=24, color=DARK_GRAY,
                    weight=BOLD, slant=ITALIC)
        nota.next_to(formulas, DOWN, buff=0.55)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class DeterminazionePrincipale(Scene):
    """Riportare un angolo qualsiasi nell'intervallo [0, 2π)."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Determinazione Principale", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = MathTex(r"\text{riportare l'angolo in } [0,\,2\pi)",
                           color=DARK_BLUE, font_size=32)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.5)

        # Idea: angoli che differiscono di un giro coincidono
        concept = MathTex(r"\alpha \;\;\text{e}\;\; \alpha + 2k\pi \;\;\longrightarrow\;\; \text{stessa posizione}",
                          color=BLACK, font_size=28)
        concept.next_to(subtitle, DOWN, buff=0.5)
        self.play(Write(concept))
        self.wait(1.5)

        # Circonferenza: ruoto di 7π/3 (più di un giro)
        R = 1.7
        center = DOWN * 0.6
        circle = Circle(radius=R, color=DARK_GRAY, stroke_width=3).move_to(center)
        dot = Dot(center, color=BLACK)
        self.play(Create(circle), FadeIn(dot))

        radius = Line(center, center + RIGHT * R, color=DARK_BLUE, stroke_width=5)
        self.play(Create(radius))
        self.wait(0.3)

        # Una rotazione di 7π/3 = un giro intero + π/3
        self.play(Rotate(radius, angle=7 * PI / 3, about_point=center,
                         rate_func=linear), run_time=2.5)
        self.wait(0.5)

        # Evidenzio la posizione finale (π/3)
        end_lab = MathTex(r"\tfrac{\pi}{3}", color=GREEN_D, font_size=36)
        end_lab.move_to(center + (R + 0.55) * np.array([np.cos(PI / 3), np.sin(PI / 3), 0]))
        self.play(Write(end_lab))
        self.wait(0.5)

        # Il calcolo
        calc1 = MathTex(r"\dfrac{7\pi}{3} = 2\pi + \dfrac{\pi}{3}", color=BLACK, font_size=38)
        calc2 = MathTex(r"\Rightarrow\quad \dfrac{\pi}{3}", color=GREEN_D, font_size=46)
        calc = VGroup(calc1, calc2).arrange(DOWN, buff=0.4)
        calc.next_to(circle, DOWN, buff=0.7)
        self.play(Write(calc1))
        self.wait(0.8)
        self.play(Write(calc2))
        sol_box = SurroundingRectangle(calc2, color=GREEN_D, buff=0.2,
                                       corner_radius=0.15, stroke_width=4)
        self.play(Create(sol_box))
        self.wait(1.5)

        # Regola operativa
        nota = VGroup(
            Text("Si aggiunge o si toglie 2π", font_size=23, color=DARK_GRAY),
            Text("finché l'angolo è in [0, 2π)", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.15)
        nota.next_to(calc, DOWN, buff=0.55)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

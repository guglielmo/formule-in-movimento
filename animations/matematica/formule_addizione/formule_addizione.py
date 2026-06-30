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


class AttenzioneErrore(Scene):
    """L'errore tipico: cos(α+β) non è cos α + cos β."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Attenzione all'errore!", font_size=38, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        # L'uguaglianza sbagliata
        sbagliato = MathTex(r"\cos(\alpha + \beta)", r"=", r"\cos\alpha + \cos\beta",
                            color=BLACK, font_size=44)
        sbagliato.next_to(title, DOWN, buff=0.8)
        self.play(Write(sbagliato))
        self.wait(0.6)

        # Barriamo l'uguale e mettiamo il diverso
        cross = Line(sbagliato[1].get_corner(DL), sbagliato[1].get_corner(UR),
                     color=RED_D, stroke_width=6)
        diverso = MathTex(r"\neq", color=RED_D, font_size=48)
        diverso.move_to(sbagliato[1])
        self.play(Create(cross))
        self.wait(0.3)
        self.play(FadeOut(sbagliato[1]), FadeOut(cross), FadeIn(diverso))
        self.wait(0.8)

        # Controesempio numerico
        h = Text("Controesempio con α = 60°, β = 30°:", font_size=24,
                 color=DARK_BLUE, weight=BOLD)
        h.next_to(sbagliato, DOWN, buff=0.8)
        self.play(FadeIn(h))

        c1 = MathTex(r"\cos(60^\circ + 30^\circ) = \cos 90^\circ = 0",
                     color=BLACK, font_size=34)
        c2 = MathTex(r"\cos 60^\circ + \cos 30^\circ = \tfrac{1}{2} + \tfrac{\sqrt{3}}{2}"
                     r"\approx 1.37", color=BLACK, font_size=34)
        conti = VGroup(c1, c2).arrange(DOWN, buff=0.5)
        conti.next_to(h, DOWN, buff=0.5)
        self.play(Write(c1))
        self.wait(0.4)
        self.play(Write(c2))
        self.wait(0.8)

        concl = Text("0 ≠ 1.37  →  servono le formule di addizione",
                     font_size=24, color=GREEN_D, weight=BOLD)
        concl.next_to(conti, DOWN, buff=0.7)
        self.play(FadeIn(concl, shift=UP * 0.2))
        self.wait(2.5)


class FormuleCoseno(Scene):
    """Coseno della somma e della differenza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Coseno di Somma e Differenza", font_size=32,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        f_somma = MathTex(r"\cos(\alpha + \beta) = \cos\alpha\,\cos\beta - \sin\alpha\,\sin\beta",
                          color=BLACK, font_size=34)
        f_diff = MathTex(r"\cos(\alpha - \beta) = \cos\alpha\,\cos\beta + \sin\alpha\,\sin\beta",
                         color=BLACK, font_size=34)
        formule = VGroup(f_somma, f_diff).arrange(DOWN, buff=0.9)
        formule.next_to(title, DOWN, buff=1.0)
        self.play(Write(f_somma))
        self.wait(0.6)
        self.play(Write(f_diff))
        self.wait(0.6)

        box1 = SurroundingRectangle(f_somma, color=BLUE_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)
        box2 = SurroundingRectangle(f_diff, color=BLUE_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)
        self.play(Create(box1), Create(box2))
        self.wait(0.8)

        nota = VGroup(
            Text("Il segno si INVERTE:", font_size=26, color=RED_D, weight=BOLD),
            Text("somma → meno,  differenza → più", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(formule, DOWN, buff=1.0)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class FormuleSeno(Scene):
    """Seno della somma e della differenza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Seno di Somma e Differenza", font_size=32,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        f_somma = MathTex(r"\sin(\alpha + \beta) = \sin\alpha\,\cos\beta + \cos\alpha\,\sin\beta",
                          color=BLACK, font_size=34)
        f_diff = MathTex(r"\sin(\alpha - \beta) = \sin\alpha\,\cos\beta - \cos\alpha\,\sin\beta",
                         color=BLACK, font_size=34)
        formule = VGroup(f_somma, f_diff).arrange(DOWN, buff=0.9)
        formule.next_to(title, DOWN, buff=1.0)
        self.play(Write(f_somma))
        self.wait(0.6)
        self.play(Write(f_diff))
        self.wait(0.6)

        box1 = SurroundingRectangle(f_somma, color=RED_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)
        box2 = SurroundingRectangle(f_diff, color=RED_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)
        self.play(Create(box1), Create(box2))
        self.wait(0.8)

        nota = VGroup(
            Text("Il segno si CONSERVA:", font_size=26, color=GREEN_D, weight=BOLD),
            Text("somma → più,  differenza → meno", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.25)
        nota.next_to(formule, DOWN, buff=1.0)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class FormuleTangente(Scene):
    """Tangente della somma e della differenza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Tangente di Somma e Differenza", font_size=30,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        f_somma = MathTex(
            r"\tan(\alpha + \beta) = \dfrac{\tan\alpha + \tan\beta}{1 - \tan\alpha\,\tan\beta}",
            color=BLACK, font_size=40)
        f_diff = MathTex(
            r"\tan(\alpha - \beta) = \dfrac{\tan\alpha - \tan\beta}{1 + \tan\alpha\,\tan\beta}",
            color=BLACK, font_size=40)
        formule = VGroup(f_somma, f_diff).arrange(DOWN, buff=1.0)
        formule.next_to(title, DOWN, buff=1.0)
        self.play(Write(f_somma))
        self.wait(0.6)
        self.play(Write(f_diff))
        self.wait(0.6)

        box1 = SurroundingRectangle(f_somma, color=GREEN_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)
        box2 = SurroundingRectangle(f_diff, color=GREEN_D, buff=0.25,
                                    corner_radius=0.15, stroke_width=4)
        self.play(Create(box1), Create(box2))
        self.wait(0.8)

        nota = Text("Segni opposti tra numeratore e denominatore",
                    font_size=22, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(formule, DOWN, buff=0.9)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class Esempio(Scene):
    """Applicazione: calcolare cos 75° = cos(45° + 30°)."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio: calcoliamo cos 75°", font_size=32,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        # Scomposizione in angoli notevoli
        step0 = MathTex(r"75^\circ = 45^\circ + 30^\circ", color=DARK_BLUE, font_size=36)
        step0.next_to(title, DOWN, buff=0.6)
        self.play(Write(step0))
        self.wait(0.6)

        step1 = MathTex(r"\cos 75^\circ = \cos(45^\circ + 30^\circ)",
                        color=BLACK, font_size=34)
        step2 = MathTex(r"= \cos 45^\circ \cos 30^\circ - \sin 45^\circ \sin 30^\circ",
                        color=BLACK, font_size=32)
        step3 = MathTex(r"= \dfrac{\sqrt{2}}{2}\cdot\dfrac{\sqrt{3}}{2}"
                        r" - \dfrac{\sqrt{2}}{2}\cdot\dfrac{1}{2}",
                        color=BLACK, font_size=32)
        step4 = MathTex(r"= \dfrac{\sqrt{6}}{4} - \dfrac{\sqrt{2}}{4}",
                        color=BLACK, font_size=34)

        passi = VGroup(step1, step2, step3, step4).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        passi.next_to(step0, DOWN, buff=0.6)
        for s in passi:
            self.play(Write(s))
            self.wait(0.4)
        self.wait(0.5)

        # Risultato finale
        ris = MathTex(r"\cos 75^\circ = \dfrac{\sqrt{6} - \sqrt{2}}{4}",
                      color=GREEN_D, font_size=44)
        ris.next_to(passi, DOWN, buff=0.7)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)

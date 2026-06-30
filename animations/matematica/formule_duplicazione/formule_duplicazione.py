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


class DaAddizioneADuplicazione(Scene):
    """Le formule di duplicazione nascono ponendo β = α in quelle di addizione."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Da Addizione a Duplicazione", font_size=32,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = MathTex(r"\text{poniamo } \beta = \alpha", color=DARK_BLUE, font_size=34)
        subtitle.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.6)

        # Seno
        s1 = MathTex(r"\sin(\alpha + \beta) = \sin\alpha\cos\beta + \cos\alpha\sin\beta",
                     color=BLACK, font_size=30)
        s2 = MathTex(r"\sin(2\alpha) = \sin\alpha\cos\alpha + \cos\alpha\sin\alpha",
                     color=BLACK, font_size=30)
        s3 = MathTex(r"\sin(2\alpha) = 2\sin\alpha\cos\alpha", color=BLACK, font_size=34)
        seno = VGroup(s1, s2, s3).arrange(DOWN, buff=0.35)
        seno.next_to(subtitle, DOWN, buff=0.6)
        self.play(Write(s1))
        self.play(TransformMatchingShapes(s1.copy(), s2))
        self.play(Write(s3))
        box_s = SurroundingRectangle(s3, color=RED_D, buff=0.2,
                                     corner_radius=0.12, stroke_width=4)
        self.play(Create(box_s))
        self.wait(1)

        # Coseno
        c1 = MathTex(r"\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta",
                     color=BLACK, font_size=30)
        c2 = MathTex(r"\cos(2\alpha) = \cos^2\alpha - \sin^2\alpha", color=BLACK, font_size=34)
        coseno = VGroup(c1, c2).arrange(DOWN, buff=0.35)
        coseno.next_to(seno, DOWN, buff=0.8)
        self.play(Write(c1))
        self.play(Write(c2))
        box_c = SurroundingRectangle(c2, color=BLUE_D, buff=0.2,
                                     corner_radius=0.12, stroke_width=4)
        self.play(Create(box_c))
        self.wait(2.5)


class FormuleDuplicazione(Scene):
    """Riepilogo delle formule di duplicazione, con le tre forme del coseno."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Formule di Duplicazione", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        seno = MathTex(r"\sin 2\alpha = 2\sin\alpha\cos\alpha", color=RED_D, font_size=36)

        cos_title = Text("Il coseno ha tre forme equivalenti:", font_size=22,
                         color=DARK_GRAY)
        cos1 = MathTex(r"\cos 2\alpha = \cos^2\alpha - \sin^2\alpha", color=BLUE_D, font_size=32)
        cos2 = MathTex(r"\cos 2\alpha = 2\cos^2\alpha - 1", color=BLUE_D, font_size=32)
        cos3 = MathTex(r"\cos 2\alpha = 1 - 2\sin^2\alpha", color=BLUE_D, font_size=32)
        cosgruppo = VGroup(cos1, cos2, cos3).arrange(DOWN, buff=0.3)

        tan = MathTex(r"\tan 2\alpha = \dfrac{2\tan\alpha}{1 - \tan^2\alpha}",
                      color=GREEN_D, font_size=36)

        blocco = VGroup(seno, cos_title, cosgruppo, tan).arrange(DOWN, buff=0.55)
        blocco.next_to(title, DOWN, buff=0.7)

        self.play(Write(seno))
        self.wait(0.4)
        self.play(FadeIn(cos_title))
        self.play(LaggedStart(Write(cos1), Write(cos2), Write(cos3), lag_ratio=0.4))
        self.wait(0.4)
        self.play(Write(tan))
        self.wait(0.8)

        nota = Text("Le tre forme del coseno si ottengono con sin²+cos²=1",
                    font_size=20, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(blocco, DOWN, buff=0.6)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class EsempioDuplicazione(Scene):
    """Esempio: noto sin α = 3/5, calcolare sin 2α e cos 2α."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio di Duplicazione", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"\sin\alpha = \tfrac{3}{5}, \quad \alpha \text{ acuto}",
                       color=DARK_BLUE, font_size=34)
        dati.next_to(title, DOWN, buff=0.5)
        self.play(Write(dati))
        self.wait(0.5)

        # Prima il coseno con la relazione fondamentale
        cos_step = VGroup(
            Text("Trovo il coseno:", font_size=22, color=DARK_GRAY, weight=BOLD),
            MathTex(r"\cos\alpha = \sqrt{1 - \tfrac{9}{25}} = \tfrac{4}{5}",
                    color=BLACK, font_size=32),
        ).arrange(DOWN, buff=0.25)
        cos_step.next_to(dati, DOWN, buff=0.6)
        self.play(FadeIn(cos_step[0]))
        self.play(Write(cos_step[1]))
        self.wait(0.8)

        # sin 2α
        s = MathTex(r"\sin 2\alpha = 2\cdot\tfrac{3}{5}\cdot\tfrac{4}{5} = \tfrac{24}{25}",
                    color=BLACK, font_size=34)
        s.next_to(cos_step, DOWN, buff=0.7)
        self.play(Write(s))
        box_s = SurroundingRectangle(s, color=RED_D, buff=0.18,
                                     corner_radius=0.12, stroke_width=4)
        self.play(Create(box_s))
        self.wait(0.6)

        # cos 2α
        c = MathTex(r"\cos 2\alpha = 1 - 2\cdot\tfrac{9}{25} = \tfrac{7}{25}",
                    color=BLACK, font_size=34)
        c.next_to(s, DOWN, buff=0.7)
        self.play(Write(c))
        box_c = SurroundingRectangle(c, color=BLUE_D, buff=0.18,
                                     corner_radius=0.12, stroke_width=4)
        self.play(Create(box_c))
        self.wait(2.5)


class FormuleBisezione(Scene):
    """Le formule di bisezione: seno, coseno e tangente dell'angolo metà."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Formule di Bisezione", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("dall'angolo α all'angolo metà α/2", font_size=22,
                        color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.5)

        seno = MathTex(r"\sin\dfrac{\alpha}{2} = \pm\sqrt{\dfrac{1 - \cos\alpha}{2}}",
                       color=RED_D, font_size=36)
        coseno = MathTex(r"\cos\dfrac{\alpha}{2} = \pm\sqrt{\dfrac{1 + \cos\alpha}{2}}",
                         color=BLUE_D, font_size=36)
        tan = MathTex(r"\tan\dfrac{\alpha}{2} = \pm\sqrt{\dfrac{1 - \cos\alpha}{1 + \cos\alpha}}"
                      r" = \dfrac{1 - \cos\alpha}{\sin\alpha}",
                      color=GREEN_D, font_size=32)
        blocco = VGroup(seno, coseno, tan).arrange(DOWN, buff=0.7)
        blocco.next_to(subtitle, DOWN, buff=0.8)

        self.play(Write(seno))
        self.wait(0.4)
        self.play(Write(coseno))
        self.wait(0.4)
        self.play(Write(tan))
        self.wait(0.8)

        nota = VGroup(
            Text("Il segno dipende dal quadrante di α/2", font_size=21, color=DARK_GRAY),
            Text("Si ricavano dalle forme di cos 2α", font_size=21,
                 color=DARK_GRAY, slant=ITALIC),
        ).arrange(DOWN, buff=0.2)
        nota.next_to(blocco, DOWN, buff=0.7)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)


class EsempioBisezione(Scene):
    """Esempio: calcolare cos 15° come coseno della metà di 30°."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio: calcoliamo cos 15°", font_size=32,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        step0 = MathTex(r"15^\circ = \dfrac{30^\circ}{2}", color=DARK_BLUE, font_size=36)
        step0.next_to(title, DOWN, buff=0.6)
        self.play(Write(step0))
        self.wait(0.5)

        step1 = MathTex(r"\cos 15^\circ = \sqrt{\dfrac{1 + \cos 30^\circ}{2}}",
                        color=BLACK, font_size=34)
        step2 = MathTex(r"= \sqrt{\dfrac{1 + \tfrac{\sqrt{3}}{2}}{2}}"
                        r" = \sqrt{\dfrac{2 + \sqrt{3}}{4}}",
                        color=BLACK, font_size=32)
        step3 = MathTex(r"= \dfrac{\sqrt{2 + \sqrt{3}}}{2} \approx 0.966",
                        color=BLACK, font_size=34)
        passi = VGroup(step1, step2, step3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        passi.next_to(step0, DOWN, buff=0.7)
        for s in passi:
            self.play(Write(s))
            self.wait(0.5)
        self.wait(0.5)

        nota = Text("(segno + perché 15° è nel primo quadrante)",
                    font_size=22, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(passi, DOWN, buff=0.7)
        self.play(FadeIn(nota, shift=UP * 0.2))

        box = SurroundingRectangle(step3, color=GREEN_D, buff=0.2,
                                   corner_radius=0.12, stroke_width=5)
        self.play(Create(box))
        self.wait(2.5)

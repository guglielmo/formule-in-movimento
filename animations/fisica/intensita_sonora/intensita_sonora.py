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


class IntensitaSonora(Scene):
    """Definizione di intensità sonora: potenza per unità di area."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Intensità Sonora", font_size=40, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("quanta energia attraversa una superficie",
                        font_size=23, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.4)

        # Sorgente che emette verso una superficie
        sorgente = Dot(LEFT * 2.2 + UP * 1.8, color=RED_D, radius=0.12)
        s_lab = Text("sorgente", font_size=20, color=DARK_GRAY).next_to(sorgente, LEFT, buff=0.15)
        area = Square(side_length=1.6, color=BLUE_D, fill_opacity=0.15, stroke_width=4)
        area.move_to(RIGHT * 1.8 + UP * 1.8)
        a_lab = MathTex("A", color=BLUE_D, font_size=32).move_to(area.get_center())
        frecce = VGroup(*[
            Arrow(sorgente.get_center(), area.get_left() + UP * dy + RIGHT * 0.1,
                  color=RED_D, stroke_width=3, buff=0.2, max_tip_length_to_length_ratio=0.1)
            for dy in (-0.5, 0, 0.5)
        ])
        self.play(FadeIn(sorgente), Write(s_lab), Create(area), Write(a_lab))
        self.play(LaggedStart(*[GrowArrow(f) for f in frecce], lag_ratio=0.2))
        self.wait(0.6)

        # Definizione
        defin = MathTex(r"I = \dfrac{P}{A}", color=BLACK, font_size=56)
        defin.next_to(area, DOWN, buff=1.3)
        self.play(Write(defin))
        box = SurroundingRectangle(defin, color=GREEN_D, buff=0.3,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.6)

        legenda = VGroup(
            MathTex(r"P = \text{potenza (W)}", color=DARK_GRAY, font_size=28),
            MathTex(r"A = \text{area (m}^2)", color=DARK_GRAY, font_size=28),
            MathTex(r"I \;\to\; \text{W/m}^2", color=DARK_BLUE, font_size=30),
        ).arrange(DOWN, buff=0.3)
        legenda.next_to(box, DOWN, buff=0.6)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in legenda], lag_ratio=0.3))
        self.wait(2.5)


class PropagazioneSferica(Scene):
    """L'intensità diminuisce con il quadrato della distanza."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("La Legge dell'Inverso del Quadrato", font_size=30,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        # Sorgente puntiforme con fronti d'onda sferici
        center = UP * 1.6
        sorgente = Dot(center, color=RED_D, radius=0.13)
        fronti = VGroup(*[
            Circle(radius=r, color=BLUE_D, stroke_width=3).move_to(center)
            for r in (0.8, 1.6, 2.4)
        ])
        self.play(FadeIn(sorgente))
        self.play(LaggedStart(*[Create(c) for c in fronti], lag_ratio=0.4))
        self.wait(0.4)

        # La stessa potenza si distribuisce su sfere sempre più grandi
        nota = Text("la stessa energia su sfere sempre più grandi",
                    font_size=21, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(fronti, DOWN, buff=0.5)
        self.play(FadeIn(nota))
        self.wait(0.5)

        formula = MathTex(r"I = \dfrac{P}{4\pi r^2}", color=BLACK, font_size=50)
        formula.next_to(nota, DOWN, buff=0.6)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.28,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.6)

        # Conseguenza: distanza doppia, intensità un quarto
        cons = VGroup(
            Text("Distanza doppia", font_size=24, color=DARK_BLUE, weight=BOLD),
            MathTex(r"r \to 2r \quad\Rightarrow\quad I \to \dfrac{I}{4}",
                    color=BLACK, font_size=34),
        ).arrange(DOWN, buff=0.3)
        cons.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(cons[0]))
        self.play(Write(cons[1]))
        self.wait(2.5)


class LivelloIntensita(Scene):
    """Il livello di intensità sonora in decibel."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Livello di Intensità Sonora", font_size=32,
                     color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        subtitle = Text("l'orecchio percepisce in scala logaritmica",
                        font_size=22, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.5)

        # La formula del decibel
        formula = MathTex(r"\beta = 10\,\log_{10}\!\left(\dfrac{I}{I_0}\right)",
                          color=BLACK, font_size=48)
        formula.next_to(subtitle, DOWN, buff=0.7)
        self.play(Write(formula))
        box = SurroundingRectangle(formula, color=GREEN_D, buff=0.28,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        unita = MathTex(r"[\beta] = \text{decibel (dB)}", color=DARK_BLUE, font_size=30)
        unita.next_to(box, DOWN, buff=0.35)
        self.play(FadeIn(unita))
        self.wait(0.6)

        # La soglia di udibilità
        soglia = VGroup(
            Text("Soglia di udibilità:", font_size=24, color=DARK_GRAY, weight=BOLD),
            MathTex(r"I_0 = 10^{-12}\ \text{W/m}^2", color=BLACK, font_size=34),
            MathTex(r"\Rightarrow\; \beta = 0\ \text{dB}", color=GREEN_D, font_size=32),
        ).arrange(DOWN, buff=0.3)
        soglia.next_to(unita, DOWN, buff=0.7)
        self.play(FadeIn(soglia[0]))
        self.play(Write(soglia[1]))
        self.play(Write(soglia[2]))
        self.wait(0.6)

        nota = Text("Il logaritmo comprime un enorme intervallo di intensità",
                    font_size=20, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(soglia, DOWN, buff=0.6)
        self.play(FadeIn(nota))
        self.wait(2.5)


class EsempioDecibel(Scene):
    """Esempio: calcolare i decibel di un suono e l'effetto del raddoppio."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("Esempio in Decibel", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        dati = MathTex(r"I = 10^{-6}\ \text{W/m}^2", color=DARK_BLUE, font_size=34)
        dati.next_to(title, DOWN, buff=0.6)
        self.play(Write(dati))
        self.wait(0.4)

        s1 = MathTex(r"\beta = 10\,\log_{10}\!\left(\dfrac{10^{-6}}{10^{-12}}\right)",
                     color=BLACK, font_size=34)
        s2 = MathTex(r"\beta = 10\,\log_{10}\!\left(10^{6}\right)", color=BLACK, font_size=34)
        s3 = MathTex(r"\beta = 10 \cdot 6", color=BLACK, font_size=34)
        passi = VGroup(s1, s2, s3).arrange(DOWN, buff=0.45)
        passi.next_to(dati, DOWN, buff=0.6)
        for s in passi:
            self.play(Write(s))
            self.wait(0.35)

        ris = MathTex(r"\beta = 60\ \text{dB}", color=GREEN_D, font_size=48)
        ris.next_to(passi, DOWN, buff=0.6)
        self.play(Write(ris))
        box = SurroundingRectangle(ris, color=GREEN_D, buff=0.25,
                                   corner_radius=0.15, stroke_width=5)
        self.play(Create(box))
        self.wait(0.8)

        # Curiosità: raddoppiare l'intensità aggiunge ~3 dB
        extra = VGroup(
            Text("Raddoppiare l'intensità:", font_size=23, color=DARK_BLUE, weight=BOLD),
            MathTex(r"10\,\log_{10} 2 \approx 3\ \text{dB in più}",
                    color=BLACK, font_size=30),
        ).arrange(DOWN, buff=0.25)
        extra.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(extra[0]))
        self.play(Write(extra[1]))
        self.wait(2.5)


class ScalaDecibel(Scene):
    """Una scala dei suoni comuni in decibel."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        title = Text("La Scala dei Decibel", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.4)

        suoni = [
            ("Silenzio / soglia", "0 dB", GREEN_D),
            ("Sussurro", "30 dB", GREEN_D),
            ("Conversazione", "60 dB", DARK_BLUE),
            ("Traffico intenso", "80 dB", DARK_BLUE),
            ("Concerto rock", "110 dB", RED_D),
            ("Soglia del dolore", "130 dB", RED_D),
        ]

        righe = VGroup()
        for nome, valore, col in suoni:
            n = Text(nome, font_size=24, color=BLACK)
            v = Text(valore, font_size=24, color=col, weight=BOLD)
            riga = VGroup(n, v).arrange(RIGHT, buff=0.6)
            righe.add(riga)
        righe.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        righe.next_to(title, DOWN, buff=0.8)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in righe], lag_ratio=0.25))
        self.wait(1.0)

        nota = VGroup(
            Text("Ogni +10 dB = intensità ×10", font_size=24, color=GREEN_D, weight=BOLD),
            Text("Oltre 85 dB prolungati: rischio per l'udito", font_size=21,
                 color=DARK_GRAY, slant=ITALIC),
        ).arrange(DOWN, buff=0.3)
        nota.next_to(righe, DOWN, buff=0.8)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

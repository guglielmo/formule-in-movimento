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


class DefinizioneLogaritmo(Scene):
    """Introduce la definizione di logaritmo a partire dall'esponenziale."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Che cos'è un Logaritmo?", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Partiamo da una domanda: a quale esponente elevare 2 per ottenere 8?
        domanda = VGroup(
            Text("A quale esponente elevare 2", font_size=26, color=DARK_BLUE),
            Text("per ottenere 8?", font_size=26, color=DARK_BLUE),
        ).arrange(DOWN, buff=0.15)
        domanda.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(domanda, shift=UP * 0.2))
        self.wait(1)

        # L'incognita è l'esponente
        eq_question = MathTex("2^{?}", "=", "8", color=BLACK, font_size=72)
        eq_question.next_to(domanda, DOWN, buff=0.6)
        self.play(Write(eq_question))
        self.wait(1.5)

        # La risposta è 3
        eq_answer = MathTex("2^{3}", "=", "8", color=BLACK, font_size=72)
        eq_answer.move_to(eq_question)
        self.play(TransformMatchingTex(eq_question, eq_answer))
        self.wait(1)

        # Quell'esponente si chiama logaritmo
        log_eq = MathTex(r"\log_{2} 8", "=", "3", color=GREEN_D, font_size=72)
        log_eq.next_to(eq_answer, DOWN, buff=0.8)
        freccia = Text("si scrive", font_size=24, color=DARK_GRAY, slant=ITALIC)
        freccia.next_to(eq_answer, DOWN, buff=0.25)
        self.play(FadeIn(freccia))
        self.play(Write(log_eq))
        self.wait(2)

        # Definizione generale: log_a b = c  <=>  a^c = b
        self.play(
            FadeOut(domanda), FadeOut(freccia),
            FadeOut(eq_answer), FadeOut(log_eq),
        )
        self.wait(0.3)

        defn_label = Text("In generale:", font_size=26, color=DARK_BLUE, weight=BOLD)
        defn_label.next_to(title, DOWN, buff=0.6)
        self.play(FadeIn(defn_label))

        defn = MathTex(
            r"\log_{a} b = c", r"\quad\Longleftrightarrow\quad", r"a^{c} = b",
            color=BLACK, font_size=52,
        )
        defn.next_to(defn_label, DOWN, buff=0.6)
        self.play(Write(defn))
        self.wait(1.5)

        # Frase chiave
        frase = VGroup(
            Text("Il logaritmo è l'esponente", font_size=28, color=GREEN_D, weight=BOLD),
            Text("da dare alla base", font_size=28, color=GREEN_D, weight=BOLD),
            Text("per ottenere l'argomento.", font_size=28, color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.18)
        frase.next_to(defn, DOWN, buff=0.7)
        box = SurroundingRectangle(frase, color=GREEN_D, buff=0.3, corner_radius=0.15, stroke_width=4)
        self.play(FadeIn(frase, shift=UP * 0.2), Create(box))
        self.wait(1.5)

        # Condizioni di esistenza
        cond = MathTex(r"a > 0,\quad a \neq 1,\quad b > 0", color=DARK_GRAY, font_size=36)
        cond.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(cond, shift=UP * 0.2))
        self.wait(2.5)


class LogaritmoInversaEsponenziale(Scene):
    """Mostra la funzione logaritmica come inversa dell'esponenziale (simmetria su y=x)."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("L'Inversa dell'Esponenziale", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Le due funzioni
        leggi = VGroup(
            MathTex(r"y = 2^x", color=RED_D, font_size=40),
            MathTex(r"y = \log_{2} x", color=BLUE_D, font_size=40),
        ).arrange(RIGHT, buff=0.8)
        leggi.next_to(title, DOWN, buff=0.4)
        self.play(Write(leggi[0]))
        self.play(Write(leggi[1]))
        self.wait(1)

        # Assi (scala uguale sui due assi per mostrare la simmetria)
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=6.5,
            y_length=6.5,
            axis_config={"color": DARK_GRAY, "include_tip": True,
                         "tip_width": 0.15, "tip_height": 0.15},
        )
        axes.next_to(leggi, DOWN, buff=0.5)

        x_label = Text("x", font_size=24, color=DARK_GRAY).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("y", font_size=24, color=DARK_GRAY).next_to(axes.y_axis, UP, buff=0.1)
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # Bisettrice y = x (asse di simmetria)
        bisettrice = DashedLine(
            axes.c2p(-4, -4), axes.c2p(4, 4),
            color=DARK_GRAY, stroke_width=2,
        )
        bis_label = MathTex("y = x", color=DARK_GRAY, font_size=30)
        bis_label.next_to(axes.c2p(3, 3), UR, buff=0.05)
        self.play(Create(bisettrice), FadeIn(bis_label))
        self.wait(0.5)

        # Curva esponenziale
        exp_curve = axes.plot(lambda x: 2 ** x, x_range=[-4, 2], color=RED_D, stroke_width=5)
        self.play(Create(exp_curve), run_time=1.5)
        self.wait(0.5)

        # Curva logaritmica (riflessione rispetto a y=x)
        log_curve = axes.plot(
            lambda x: np.log(x) / np.log(2),
            x_range=[0.0625, 4], color=BLUE_D, stroke_width=5,
        )
        self.play(Create(log_curve), run_time=1.5)
        self.wait(1)

        # Messaggio: una è il riflesso dell'altra rispetto a y = x
        msg = VGroup(
            Text("Una è il riflesso dell'altra", font_size=25, color=GREEN_D, weight=BOLD),
            Text("rispetto alla retta y = x", font_size=25, color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        msg.next_to(axes, DOWN, buff=0.4)
        self.play(FadeIn(msg, shift=UP * 0.2))
        self.wait(2.5)


class ProprietaLogaritmi(Scene):
    """Le proprietà fondamentali dei logaritmi."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Proprietà dei Logaritmi", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        subtitle = Text("Trasformano prodotti in somme", font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1)

        # Le proprietà fondamentali
        regole = [
            ("Logaritmo del prodotto", r"\log_a (x \cdot y) = \log_a x + \log_a y"),
            ("Logaritmo del quoziente", r"\log_a \frac{x}{y} = \log_a x - \log_a y"),
            ("Logaritmo della potenza", r"\log_a x^n = n \cdot \log_a x"),
            ("Casi particolari", r"\log_a 1 = 0 \qquad \log_a a = 1"),
        ]

        blocchi = VGroup()
        for nome, formula in regole:
            etichetta = Text(nome, font_size=24, color=DARK_GRAY, weight=BOLD)
            espressione = MathTex(formula, color=BLACK, font_size=42)
            blocco = VGroup(etichetta, espressione).arrange(DOWN, buff=0.2)
            blocchi.add(blocco)

        blocchi.arrange(DOWN, buff=0.55)
        blocchi.next_to(subtitle, DOWN, buff=0.6)

        for blocco in blocchi:
            self.play(FadeIn(blocco, shift=DOWN * 0.3))
            self.wait(0.7)

        self.wait(1.5)

        # Nota finale
        nota = Text(
            "Valgono per ogni base ammessa (a > 0, a ≠ 1)",
            font_size=23, color=GREEN_D, weight=BOLD, slant=ITALIC,
        )
        nota.next_to(blocchi, DOWN, buff=0.55)
        box = SurroundingRectangle(nota, color=GREEN_D, buff=0.25, corner_radius=0.15, stroke_width=4)
        self.play(FadeIn(nota, shift=UP * 0.2), Create(box))
        self.wait(2.5)


class CambiamentoDiBase(Scene):
    """La formula del cambiamento di base."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Cambiamento di Base", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Problema: la calcolatrice ha solo log in base 10 (o e)
        problema = VGroup(
            Text("La calcolatrice conosce solo", font_size=24, color=DARK_BLUE),
            Text("log in base 10 (e in base e).", font_size=24, color=DARK_BLUE),
            Text("Come calcolo un logaritmo", font_size=24, color=DARK_GRAY),
            Text("in un'altra base?", font_size=24, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.15)
        problema.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(problema, shift=UP * 0.2))
        self.wait(2)

        self.play(FadeOut(problema))
        self.wait(0.3)

        # La formula del cambiamento di base
        formula_label = Text("Formula del cambiamento di base:", font_size=25, color=DARK_BLUE, weight=BOLD)
        formula_label.next_to(title, DOWN, buff=0.6)
        self.play(FadeIn(formula_label))

        formula = MathTex(r"\log_a b = \frac{\log_c b}{\log_c a}", color=BLACK, font_size=60)
        formula.next_to(formula_label, DOWN, buff=0.6)
        box = SurroundingRectangle(formula, color=DARK_BLUE, buff=0.3, corner_radius=0.15, stroke_width=4)
        self.play(Write(formula), Create(box))
        self.wait(1)

        nota = Text("c è una base qualsiasi a nostra scelta", font_size=22, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(box, DOWN, buff=0.4)
        self.play(FadeIn(nota))
        self.wait(2)

        # Esempio numerico: log_2 8 usando i logaritmi in base 10
        self.play(FadeOut(nota))
        esempio_label = Text("Esempio:", font_size=24, color=DARK_GRAY, weight=BOLD)
        esempio_label.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(esempio_label))

        ex1 = MathTex(r"\log_2 8 = \frac{\log 8}{\log 2}", color=BLACK, font_size=52)
        ex1.next_to(esempio_label, DOWN, buff=0.5)
        self.play(Write(ex1))
        self.wait(1.5)

        ex2 = MathTex(r"= \frac{0{,}903}{0{,}301} = 3", color=GREEN_D, font_size=52)
        ex2.next_to(ex1, DOWN, buff=0.4)
        self.play(Write(ex2))
        self.wait(1)

        # Verifica
        verifica_eq = MathTex(r"2^3 = 8", color=GREEN_D, font_size=44)
        verifica_check = Text("✓", font_size=44, color=GREEN_D)
        verifica = VGroup(verifica_eq, verifica_check).arrange(RIGHT, buff=0.25)
        verifica.next_to(ex2, DOWN, buff=0.6)
        self.play(FadeIn(verifica, shift=UP * 0.2))
        self.wait(2.5)

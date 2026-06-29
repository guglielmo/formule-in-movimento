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


class EquazioneElementare(Scene):
    """Il caso elementare: log_a x = b, risolto con la definizione di logaritmo."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Equazioni Logaritmiche", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        subtitle = Text("Il caso elementare", font_size=26, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.5)

        # Promemoria: l'argomento deve essere positivo (condizione di esistenza)
        ce = Text("Ricorda: l'argomento dev'essere positivo (x > 0)", font_size=22,
                  color=DARK_GRAY, slant=ITALIC)
        ce.next_to(subtitle, DOWN, buff=0.4)
        self.play(FadeIn(ce))
        self.wait(1)

        # Equazione di partenza
        eq1 = MathTex(r"\log_{2} x", "=", "3", color=BLACK, font_size=64)
        eq1.next_to(ce, DOWN, buff=0.8)
        self.play(Write(eq1))
        self.wait(1)

        # Passo: applico la definizione di logaritmo
        hint = Text("Applico la definizione di logaritmo", font_size=24, color=DARK_GRAY)
        hint.next_to(eq1, DOWN, buff=0.8)
        self.play(FadeIn(hint))
        self.wait(0.5)

        # log_2 x = 3  ->  x = 2^3
        eq2 = MathTex("x", "=", "2^{3}", color=BLACK, font_size=64)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1)

        # Calcolo
        hint2 = Text("Calcolo la potenza", font_size=24, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        eq3 = MathTex("x", "=", "8", color=GREEN_D, font_size=80)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3), FadeOut(hint))

        sol_box = SurroundingRectangle(eq3, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(sol_box))
        self.wait(0.5)

        # Verifica della condizione di esistenza
        verifica = Text("8 > 0  →  accettabile ✓", font_size=26, color=GREEN_D, weight=BOLD)
        verifica.next_to(sol_box, DOWN, buff=0.7)
        self.play(FadeIn(verifica, shift=UP * 0.2))
        self.wait(1.5)

        # Regola generale
        self.play(FadeOut(verifica))
        regola = MathTex(r"\log_{a} x = b \;\Longrightarrow\; x = a^{b}", color=DARK_BLUE, font_size=44)
        regola.next_to(sol_box, DOWN, buff=0.7)
        self.play(Write(regola))
        self.wait(2.5)


class MetodoConfronto(Scene):
    """Equazioni con un logaritmo per membro: stessa base -> confronto degli argomenti."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Metodo del Confronto", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Idea: stessa base -> confronto gli argomenti
        idea = MathTex(
            r"\log_{a} f(x) = \log_{a} g(x) \;\Longrightarrow\; f(x) = g(x)",
            color=BLACK, font_size=38,
        )
        idea.next_to(title, DOWN, buff=0.5)
        self.play(Write(idea))
        self.wait(1.5)

        self.play(idea.animate.scale(0.85).next_to(title, DOWN, buff=0.4))

        # Equazione
        eq1 = MathTex(r"\log_{2}(x+1)", "=", r"\log_{2}(2x-3)", color=BLACK, font_size=48)
        eq1.next_to(idea, DOWN, buff=0.7)
        self.play(Write(eq1))
        self.wait(1)

        # Condizioni di esistenza
        ce_label = Text("Condizioni di esistenza:", font_size=23, color=RED_D, weight=BOLD)
        ce = MathTex(r"x+1 > 0 \;\wedge\; 2x-3 > 0 \;\Rightarrow\; x > \tfrac{3}{2}",
                     color=RED_D, font_size=34)
        ce_group = VGroup(ce_label, ce).arrange(DOWN, buff=0.2)
        ce_group.next_to(eq1, DOWN, buff=0.6)
        self.play(FadeIn(ce_label))
        self.play(Write(ce))
        self.wait(1.5)

        # Confronto degli argomenti
        hint = Text("Stessa base: confronto gli argomenti", font_size=24, color=DARK_GRAY)
        hint.next_to(ce_group, DOWN, buff=0.6)
        self.play(FadeIn(hint))
        self.wait(0.5)

        eq2 = MathTex("x+1", "=", "2x-3", color=BLACK, font_size=52)
        eq2.next_to(hint, DOWN, buff=0.5)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait(1)

        # Risolvo l'equazione di primo grado
        eq3 = MathTex("x", "=", "4", color=GREEN_D, font_size=64)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(0.5)

        sol_box = SurroundingRectangle(eq3, color=GREEN_D, buff=0.35, corner_radius=0.2, stroke_width=5)
        self.play(Create(sol_box))

        # Verifica con le C.E.
        verifica = VGroup(
            MathTex(r"4 > \tfrac{3}{2}", color=GREEN_D, font_size=40),
            Text("✓", font_size=40, color=GREEN_D),
        ).arrange(RIGHT, buff=0.25)
        verifica.next_to(sol_box, DOWN, buff=0.5)
        self.play(FadeIn(verifica, shift=UP * 0.2))
        self.wait(2.5)


class UsoProprieta(Scene):
    """Più logaritmi: si usano le proprietà per ottenerne uno solo, poi si scartano le non accettabili."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Con le Proprietà dei Logaritmi", font_size=30, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Equazione con due logaritmi
        eq1 = MathTex(r"\log_{2} x", "+", r"\log_{2}(x-2)", "=", "3", color=BLACK, font_size=46)
        eq1.next_to(title, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1)

        # Condizioni di esistenza
        ce = MathTex(r"x > 0 \;\wedge\; x-2 > 0 \;\Rightarrow\; x > 2", color=RED_D, font_size=34)
        ce.next_to(eq1, DOWN, buff=0.45)
        self.play(Write(ce))
        self.wait(1.5)

        # Proprietà del prodotto: somma di logaritmi -> logaritmo del prodotto
        hint = Text("Somma di logaritmi → logaritmo del prodotto", font_size=22, color=DARK_GRAY)
        hint.next_to(ce, DOWN, buff=0.55)
        self.play(FadeIn(hint))
        self.wait(0.5)

        eq2 = MathTex(r"\log_{2}\big[x(x-2)\big]", "=", "3", color=BLACK, font_size=46)
        eq2.next_to(hint, DOWN, buff=0.5)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait(1.5)

        # Definizione -> elimino il logaritmo
        hint2 = Text("Applico la definizione", font_size=22, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        eq3 = MathTex("x(x-2)", "=", "2^{3}", color=BLACK, font_size=46)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1)

        # Equazione di secondo grado
        eq4 = MathTex("x^{2}-2x-8", "=", "0", color=BLACK, font_size=46)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1)

        # Soluzioni
        hint3 = Text("Risolvo l'equazione di secondo grado", font_size=22, color=DARK_GRAY)
        hint3.move_to(hint)
        self.play(Transform(hint, hint3))

        eq5 = MathTex("x = 4", r"\quad \vee \quad", "x = -2", color=BLACK, font_size=46)
        eq5.move_to(eq4)
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(1.5)

        # Scarto la soluzione non accettabile (C.E.: x > 2)
        hint4 = Text("x = -2 non rispetta x > 2: la scarto", font_size=22, color=RED_D)
        hint4.move_to(hint)
        self.play(Transform(hint, hint4))

        scarto = Line(
            eq5[2].get_corner(DL) + LEFT * 0.1,
            eq5[2].get_corner(UR) + RIGHT * 0.1,
            color=RED_D, stroke_width=5,
        )
        self.play(Create(scarto))
        self.wait(1.5)

        # Soluzione accettabile
        self.play(
            FadeOut(eq5[1]), FadeOut(eq5[2]), FadeOut(scarto), FadeOut(hint),
            eq5[0].animate.set_color(GREEN_D).scale(1.3).move_to(eq4),
        )
        sol_box = SurroundingRectangle(eq5[0], color=GREEN_D, buff=0.35, corner_radius=0.2, stroke_width=5)
        self.play(Create(sol_box))
        self.wait(2.5)


class VariabileAusiliaria(Scene):
    """Equazione di secondo grado nel logaritmo, risolta per sostituzione."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Variabile Ausiliaria", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        subtitle = Text("Quando il logaritmo compare al quadrato", font_size=23, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.5)

        # Equazione (logaritmi in base 10)
        eq1 = MathTex(r"(\log x)^{2}", "-", r"\log x", "-", "2", "=", "0", color=BLACK, font_size=48)
        eq1.next_to(subtitle, DOWN, buff=0.6)
        self.play(Write(eq1))
        self.wait(1)

        ce = Text("C.E.:  x > 0", font_size=22, color=RED_D, weight=BOLD)
        ce.next_to(eq1, DOWN, buff=0.5)
        self.play(FadeIn(ce))
        self.wait(1)

        # Sostituzione t = log x
        hint = Text("Pongo  t = log x", font_size=23, color=DARK_GRAY)
        hint.next_to(ce, DOWN, buff=0.5)
        self.play(FadeIn(hint))

        sost = MathTex(r"t = \log x", color=DARK_BLUE, font_size=40)
        sost.to_corner(UR, buff=0.5)
        sost_box = SurroundingRectangle(sost, color=DARK_BLUE, buff=0.2, corner_radius=0.1, stroke_width=4)
        self.play(FadeIn(sost), Create(sost_box))
        self.wait(0.5)

        # Equazione di secondo grado in t
        eq2 = MathTex("t^{2}", "-", "t", "-", "2", "=", "0", color=BLACK, font_size=52)
        eq2.next_to(hint, DOWN, buff=0.5)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait(1.5)

        # Soluzioni in t
        hint2 = Text("Risolvo in t", font_size=23, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        eq3 = MathTex("t = 2", r"\quad \vee \quad", "t = -1", color=BLACK, font_size=48)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)

        # Torno alla x: log x = 2  e  log x = -1
        hint3 = Text("Torno all'incognita: log x = t", font_size=23, color=DARK_GRAY)
        hint3.move_to(hint)
        self.play(Transform(hint, hint3))

        eq4 = MathTex(r"\log x = 2", r"\quad \vee \quad", r"\log x = -1", color=BLACK, font_size=44)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1.5)

        # Soluzioni finali (base 10): x = 100  e  x = 1/10
        hint4 = Text("Applico la definizione (base 10)", font_size=23, color=DARK_GRAY)
        hint4.move_to(hint)
        self.play(Transform(hint, hint4))

        eq5 = MathTex(r"x = 100", r"\quad \vee \quad", r"x = \tfrac{1}{10}", color=GREEN_D, font_size=52)
        eq5.move_to(eq4)
        self.play(TransformMatchingTex(eq4, eq5), FadeOut(hint))
        self.wait(0.5)

        sol_box = SurroundingRectangle(eq5, color=GREEN_D, buff=0.35, corner_radius=0.2, stroke_width=5)
        self.play(Create(sol_box))

        # Entrambe accettabili (x > 0)
        nota = Text("Entrambe positive → entrambe accettabili", font_size=23, color=GREEN_D, weight=BOLD)
        nota.next_to(sol_box, DOWN, buff=0.6)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

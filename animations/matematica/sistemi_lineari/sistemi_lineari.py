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

class IntroduzioneSistemi(Scene):
    """Introduzione ai sistemi di equazioni lineari."""

    def construct(self):
        self.camera.background_color = WHITE

        # Title at top with minimal buffer
        title = Text("Sistemi di Equazioni Lineari", font_size=30, color=BLACK, weight=BOLD, line_spacing=1.1)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        # Definition
        definition = Text("Cos'è un sistema?", font_size=30, color=DARK_BLUE, weight=BOLD)
        definition.next_to(title, DOWN, buff=1.0)
        self.play(FadeIn(definition))
        self.wait(0.5)

        # Example system
        system = MathTex(
            r"\begin{cases} 2x + y = 5 \\ x - y = 1 \end{cases}",
            color=BLACK,
            font_size=64
        )
        system.next_to(definition, DOWN, buff=0.8)
        self.play(Write(system))
        self.wait(2)

        # Explanation
        explanation = VGroup(
            Text("Due o più equazioni", font_size=28, color=DARK_GRAY),
            Text("da risolvere insieme", font_size=28, color=DARK_GRAY)
        ).arrange(DOWN, buff=0.3)
        explanation.next_to(system, DOWN, buff=0.8)
        self.play(FadeIn(explanation))
        self.wait(2)

        # Clear for methods
        self.play(FadeOut(system), FadeOut(explanation), FadeOut(definition))
        self.wait(0.5)

        # Methods section
        methods_header = Text("Metodi di Risoluzione", font_size=30, color=DARK_BLUE, weight=BOLD)
        methods_header.next_to(title, DOWN, buff=1.0)
        self.play(Write(methods_header))
        self.wait(0.5)

        # Methods list
        methods = VGroup(
            Text("1. Sostituzione", font_size=30, color=BLACK),
            Text("2. Confronto", font_size=30, color=BLACK),
            Text("3. Riduzione", font_size=30, color=BLACK),
            Text("4. Cramer", font_size=30, color=BLACK)
        ).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        methods.next_to(methods_header, DOWN, buff=0.8)

        for method in methods:
            self.play(FadeIn(method, shift=RIGHT*0.3))
            self.wait(0.4)

        self.wait(2)


class SostituzioneTeoriaEsempio(Scene):
    """Sostituzione: teoria + esempio semplice."""

    def construct(self):
        self.camera.background_color = WHITE

        # Title
        title = Text("Metodo di Sostituzione", font_size=33, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait()

        # Steps
        steps_header = Text("Procedimento", font_size=28, color=DARK_BLUE, weight=BOLD)
        steps_header.next_to(title, DOWN, buff=1.0)
        self.play(FadeIn(steps_header))

        steps = VGroup(
            Text("1. Isola una variabile", font_size=28, color=DARK_GRAY),
            Text("2. Sostituisci nell'altra", font_size=28, color=DARK_GRAY),
            Text("3. Risolvi", font_size=28, color=DARK_GRAY)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        steps.next_to(steps_header, DOWN, buff=1.0)

        for step in steps:
            self.play(FadeIn(step))
            self.wait(0.3)
        self.wait(1.0)

        # Fade out steps
        self.play(FadeOut(steps), FadeOut(steps_header))
        self.wait(0.3)

        # Example
        ex_label = Text("Esempio", font_size=28, color=DARK_BLUE, weight=BOLD)
        ex_label.next_to(title, DOWN, buff=1.0)
        self.play(FadeIn(ex_label))

        # System using separate equations for better control
        sys_eq1 = MathTex(r"y = 2x - 1", color=BLACK, font_size=52)
        sys_eq2 = MathTex(r"x + ", r"y", r" = 5", color=BLACK, font_size=52)

        system = VGroup(sys_eq1, sys_eq2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        # Add brace
        brace = MathTex(r"\begin{cases} \\ \\ \end{cases}", color=BLACK, font_size=52)
        brace.next_to(system, LEFT, buff=0.1)

        system_with_brace = VGroup(brace, system)
        system_with_brace.next_to(ex_label, DOWN, buff=0.6)

        self.play(Write(system_with_brace))
        self.wait(1)

        # Highlight y in the second equation (now it's index 1 because we split it)
        self.play(sys_eq2[1].animate.set_color(GREEN_D))
        self.wait(0.8)

        # Highlight the whole first equation
        self.play(sys_eq1.animate.set_color(GREEN_D))
        self.wait(1)

        # Explanation text
        explanation = VGroup(
            Text("Questo metodo è ideale quando una", font_size=24, color=DARK_BLUE),
            Text("variabile è già isolata o facilmente isolabile", font_size=24, color=DARK_BLUE)
        ).arrange(DOWN, buff=0.2)
        explanation.next_to(system_with_brace, DOWN, buff=0.5)

        self.play(FadeIn(explanation, shift=UP*0.2))
        self.wait(2.5)
        self.play(FadeOut(explanation))
        self.wait(0.3)

        # Update system reference for later use
        system = system_with_brace

        # Substitute
        step_text = Text("Sostituisci y nell'eq. 2 e risolvi", font_size=24, color=DARK_GRAY)
        step_text.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text))
        self.wait(1.0)

        # Split eq0 to highlight y
        eq0 = MathTex(r"x + ", r"y", r" = 5", color=BLACK, font_size=48)
        eq0.next_to(step_text, DOWN, buff=0.5)
        self.play(Write(eq0))
        self.wait(0.5)

        # Highlight y in eq0
        self.play(eq0[1].animate.set_color(GREEN_D))
        self.wait(0.5)

        # Split eq1 to highlight the substituted expression
        eq1 = MathTex(r"x + (", r"2x - 1", r") = 5", color=BLACK, font_size=48)
        eq1.next_to(eq0, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(0.3)

        # Highlight 2x - 1 in eq1 (the substituted part)
        self.play(eq1[1].animate.set_color(GREEN_D))
        self.wait(0.8)

        eq2 = MathTex(r"3x - 1 = 5", color=BLACK, font_size=48)
        eq2.next_to(eq1, DOWN, buff=0.5)
        self.play(Write(eq2))
        self.wait(0.5)

        eq3 = MathTex(r"3x = 6", color=BLACK, font_size=48)
        eq3.next_to(eq2, DOWN, buff=0.5)
        self.play(Write(eq3))
        self.wait(0.5)

        eq4 = MathTex(r"x = 2", color=GREEN_D, font_size=64)
        eq4.next_to(eq3, DOWN, buff=0.5)
        self.play(Write(eq4))
        self.wait(1.0)

        # Find y
        y_text = Text("Metti il valore di x nell'eq. 1, per trovare y", font_size=24, color=DARK_GRAY)
        y_text.next_to(eq4, DOWN, buff=0.6)
        self.play(FadeIn(y_text))
        self.wait(1.0)

        eq5 = MathTex(r"y = 2", r"x", r" - 1", color=BLACK, font_size=48)
        eq5.next_to(y_text, DOWN, buff=0.5)
        self.play(Write(eq5))
        self.wait(0.5)

        # Highlight x in eq5 (the part to substitute)
        self.play(eq5[1].animate.set_color(GREEN_D))
        self.wait(0.5)

        eq6 = MathTex(r"y = 2(", r"2", r") - 1", color=BLACK, font_size=48)
        eq6.next_to(eq5, DOWN, buff=0.5)
        self.play(Write(eq6))
        self.wait(0.5)

        # Highlight 2 in eq6 (the substituted part)
        self.play(eq6[1].animate.set_color(GREEN_D))
        self.wait(0.5)


        eq7 = MathTex(r"y = 3", color=GREEN_D, font_size=64)
        eq7.next_to(eq6, DOWN, buff=0.5)
        self.play(Write(eq7))
        self.wait(1.5)

        self.play(
            FadeOut(eq7), FadeOut(eq6), FadeOut(eq5), FadeOut(y_text),
            FadeOut(eq4), FadeOut(eq3), FadeOut(eq2), FadeOut(eq1), FadeOut(eq0), FadeOut(step_text)
        )
        # Transform back to black
        self.play(
            sys_eq1.animate.set_color(BLACK),
            sys_eq2[1].animate.set_color(BLACK)
        )

        self.wait(0.3)

        solution_text = Text("Soluzione", font_size=28, color=DARK_BLUE, weight=BOLD)
        solution_text.next_to(system, DOWN, buff=1.0)
        self.play(Write(solution_text))
        self.wait(0.3)

        solution = MathTex(r"x = 2, \quad y = 3", color=GREEN_D, font_size=52)
        solution.next_to(solution_text, DOWN, buff=1)
        self.play(Write(solution))
     
        box = SurroundingRectangle(solution, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(box))
        self.wait(2)


class SostituzioneEsempioAvanzato(Scene):
    """Sostituzione: esempio avanzato."""

    def construct(self):
        self.camera.background_color = WHITE

        title = Text("Sostituzione - Esempio 2", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        # System
        system = MathTex(
            r"\begin{cases} 2x + y = 7 \\ x - 2y = 1 \end{cases}",
            color=BLACK,
            font_size=56
        )
        system.next_to(title, DOWN, buff=0.6)
        self.play(Write(system))
        self.wait(1)

        # Isolate x from equation 2
        step_text = Text("Isola x dall'equazione 2:", font_size=24, color=DARK_GRAY)
        step_text.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        eq1 = MathTex(r"x = 1 + 2y", color=BLUE_D, font_size=54)
        eq1.next_to(step_text, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1.5)

        # Substitute
        step_text2 = Text("Sostituisci nell'equazione 1:", font_size=24, color=DARK_GRAY)
        step_text2.move_to(step_text)
        self.play(Transform(step_text, step_text2))
        self.wait(0.5)

        eq2 = MathTex(r"2(1 + 2y) + y = 7", color=BLACK, font_size=50)
        eq2.next_to(eq1, DOWN, buff=0.6)
        self.play(Write(eq2))
        self.wait(1.5)

        # Solve for y
        self.play(FadeOut(step_text), FadeOut(eq1))

        eq3 = MathTex(r"2 + 4y + y = 7", color=BLACK, font_size=50)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1)

        eq4 = MathTex(r"5y = 5", color=BLACK, font_size=50)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1)

        eq5 = MathTex(r"y = 1", color=GREEN_D, font_size=64)
        eq5.move_to(eq4)
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(1.5)

        # Find x
        x_text = Text("Sostituisci per trovare x:", font_size=24, color=DARK_GRAY)
        x_text.next_to(eq5, DOWN, buff=0.6)
        self.play(FadeIn(x_text))
        self.wait(0.5)

        eq6 = MathTex(r"x = 1 + 2(1) = 3", color=GREEN_D, font_size=64)
        eq6.next_to(x_text, DOWN, buff=0.5)
        self.play(Write(eq6))
        self.wait(1.5)

        # Solution
        self.play(FadeOut(eq5), FadeOut(eq6), FadeOut(system), FadeOut(x_text))

        solution = MathTex(r"x = 3, \quad y = 1", color=GREEN_D, font_size=72)
        solution.move_to(ORIGIN)
        self.play(Write(solution))

        box = SurroundingRectangle(solution, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(box))
        self.wait(2)


class ConfrontoTeoriaEsempio(Scene):
    """Confronto: teoria + esempio semplice."""

    def construct(self):
        self.camera.background_color = WHITE

        title = Text("Metodo del Confronto", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        # Steps
        steps_header = Text("Procedimento:", font_size=28, color=DARK_BLUE)
        steps_header.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(steps_header))

        steps = VGroup(
            Text("1. Isola stessa variabile", font_size=24, color=DARK_GRAY),
            Text("2. Uguaglia le espressioni", font_size=24, color=DARK_GRAY),
            Text("3. Risolvi", font_size=24, color=DARK_GRAY)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        steps.next_to(steps_header, DOWN, buff=0.4)

        for step in steps:
            self.play(FadeIn(step))
            self.wait(0.3)
        self.wait(1)
        self.play(FadeOut(steps), FadeOut(steps_header))
        self.wait(0.3)

        # Example
        ex_label = Text("Esempio:", font_size=28, color=DARK_BLUE, weight=BOLD)
        ex_label.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(ex_label))

        system = MathTex(
            r"\begin{cases} y = 3x - 2 \\ y = x + 4 \end{cases}",
            color=BLACK,
            font_size=56
        )
        system.next_to(ex_label, DOWN, buff=0.6)
        self.play(Write(system))
        self.wait(1)

        # Already isolated
        note = Text("y già isolata in entrambe!", font_size=26, color=GREEN_D)
        note.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(1.5)
        self.play(FadeOut(note))

        # Equate
        step_text = Text("Uguaglia le due espressioni:", font_size=24, color=DARK_GRAY)
        step_text.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        eq1 = MathTex(r"3x - 2 = x + 4", color=BLACK, font_size=52)
        eq1.next_to(step_text, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1.5)

        # Solve
        self.play(FadeOut(step_text))

        eq2 = MathTex(r"2x = 6", color=BLACK, font_size=52)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1)

        eq3 = MathTex(r"x = 3", color=GREEN_D, font_size=64)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)

        # Find y
        y_text = Text("Sostituisci per trovare y:", font_size=24, color=DARK_GRAY)
        y_text.next_to(eq3, DOWN, buff=0.6)
        self.play(FadeIn(y_text))
        self.wait(0.5)

        eq4 = MathTex(r"y = 3 + 4 = 7", color=GREEN_D, font_size=64)
        eq4.next_to(y_text, DOWN, buff=0.5)
        self.play(Write(eq4))
        self.wait(1.5)

        # Solution
        self.play(FadeOut(eq3), FadeOut(eq4), FadeOut(system), FadeOut(ex_label), FadeOut(y_text))

        solution = MathTex(r"x = 3, \quad y = 7", color=GREEN_D, font_size=72)
        solution.move_to(ORIGIN)
        self.play(Write(solution))

        box = SurroundingRectangle(solution, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(box))
        self.wait(2)


class ConfrontoEsempioAvanzato(Scene):
    """Confronto: esempio avanzato."""

    def construct(self):
        self.camera.background_color = WHITE

        title = Text("Confronto - Esempio 2", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        system = MathTex(
            r"\begin{cases} 2x + y = 8 \\ x + y = 5 \end{cases}",
            color=BLACK,
            font_size=56
        )
        system.next_to(title, DOWN, buff=0.6)
        self.play(Write(system))
        self.wait(1)

        # Isolate y from both
        step_text = Text("Isola y da entrambe:", font_size=24, color=DARK_GRAY)
        step_text.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        eqs = VGroup(
            MathTex(r"y = 8 - 2x", color=BLUE_D, font_size=50),
            MathTex(r"y = 5 - x", color=BLUE_D, font_size=50)
        ).arrange(DOWN, buff=0.5)
        eqs.next_to(step_text, DOWN, buff=0.5)

        self.play(Write(eqs[0]))
        self.wait(0.8)
        self.play(Write(eqs[1]))
        self.wait(1.5)

        # Equate
        self.play(FadeOut(step_text), FadeOut(eqs))

        step_text2 = Text("Uguaglia:", font_size=24, color=DARK_GRAY)
        step_text2.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text2))
        self.wait(0.5)

        eq1 = MathTex(r"8 - 2x = 5 - x", color=BLACK, font_size=50)
        eq1.next_to(step_text2, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1.5)

        # Solve
        self.play(FadeOut(step_text2))

        eq2 = MathTex(r"-x = -3", color=BLACK, font_size=50)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1)

        eq3 = MathTex(r"x = 3", color=GREEN_D, font_size=64)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)

        # Find y
        y_text = Text("Sostituisci per trovare y:", font_size=24, color=DARK_GRAY)
        y_text.next_to(eq3, DOWN, buff=0.6)
        self.play(FadeIn(y_text))
        self.wait(0.5)

        eq4 = MathTex(r"y = 5 - 3 = 2", color=GREEN_D, font_size=64)
        eq4.next_to(y_text, DOWN, buff=0.5)
        self.play(Write(eq4))
        self.wait(1.5)

        # Solution
        self.play(FadeOut(eq3), FadeOut(eq4), FadeOut(system), FadeOut(y_text))

        solution = MathTex(r"x = 3, \quad y = 2", color=GREEN_D, font_size=72)
        solution.move_to(ORIGIN)
        self.play(Write(solution))

        box = SurroundingRectangle(solution, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(box))
        self.wait(2)


class RiduzioneTeoriaEsempio(Scene):
    """Riduzione: teoria + esempio semplice."""

    def construct(self):
        self.camera.background_color = WHITE

        title = Text("Metodo di Riduzione", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        # Alternative name
        alt = Text("(Eliminazione)", font_size=24, color=DARK_GRAY, slant=ITALIC)
        alt.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(alt))

        # Concept
        concept = Text("Somma/sottrai le equazioni per", font_size=24, color=DARK_BLUE)
        concept.next_to(alt, DOWN, buff=0.5)
        self.play(FadeIn(concept))

        concept2 = Text("eliminare una variabile", font_size=24, color=DARK_BLUE)
        concept2.next_to(concept, DOWN, buff=0.3)
        self.play(FadeIn(concept2))
        self.wait(1.5)
        self.play(FadeOut(concept), FadeOut(concept2))

        # Example
        ex_label = Text("Esempio:", font_size=28, color=DARK_BLUE, weight=BOLD)
        ex_label.next_to(alt, DOWN, buff=0.5)
        self.play(FadeIn(ex_label))

        system = MathTex(
            r"\begin{cases} 2x + y = 7 \\ 3x - y = 8 \end{cases}",
            color=BLACK,
            font_size=56
        )
        system.next_to(ex_label, DOWN, buff=0.6)
        self.play(Write(system))
        self.wait(1)

        # Coefficients opposite
        note = Text("Coefficienti di y opposti!", font_size=26, color=GREEN_D)
        note.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(1.5)
        self.play(FadeOut(note))

        # Add equations
        step_text = Text("Somma le due equazioni:", font_size=24, color=DARK_GRAY)
        step_text.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        addition = VGroup(
            MathTex(r"2x + y = 7", color=BLACK, font_size=44),
            MathTex(r"+", color=BLACK, font_size=44),
            MathTex(r"3x - y = 8", color=BLACK, font_size=44),
            Line(LEFT * 2.5, RIGHT * 2.5, color=BLACK, stroke_width=3)
        ).arrange(DOWN, buff=0.3)
        addition.next_to(step_text, DOWN, buff=0.5)

        self.play(FadeIn(addition[0:3]))
        self.wait(0.8)
        self.play(Create(addition[3]))
        self.wait(0.5)

        result = MathTex(r"5x = 15", color=BLACK, font_size=52)
        result.next_to(addition[3], DOWN, buff=0.4)
        self.play(Write(result))
        self.wait(1.5)

        # Solve
        self.play(FadeOut(addition), FadeOut(step_text))

        eq1 = MathTex(r"x = 3", color=GREEN_D, font_size=64)
        eq1.move_to(result)
        self.play(TransformMatchingTex(result, eq1))
        self.wait(1.5)

        # Find y
        y_text = Text("Sostituisci per trovare y:", font_size=24, color=DARK_GRAY)
        y_text.next_to(eq1, DOWN, buff=0.6)
        self.play(FadeIn(y_text))
        self.wait(0.5)

        eq2 = MathTex(r"2(3) + y = 7", color=BLACK, font_size=50)
        eq2.next_to(y_text, DOWN, buff=0.5)
        self.play(Write(eq2))
        self.wait(1)

        eq3 = MathTex(r"y = 1", color=GREEN_D, font_size=64)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)

        # Solution
        self.play(FadeOut(eq1), FadeOut(eq3), FadeOut(system), FadeOut(ex_label), FadeOut(alt), FadeOut(y_text))

        solution = MathTex(r"x = 3, \quad y = 1", color=GREEN_D, font_size=72)
        solution.move_to(ORIGIN)
        self.play(Write(solution))

        box = SurroundingRectangle(solution, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(box))
        self.wait(2)


class RiduzioneEsempioAvanzato(Scene):
    """Riduzione: esempio avanzato."""

    def construct(self):
        self.camera.background_color = WHITE

        title = Text("Riduzione - Esempio 2", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        system = MathTex(
            r"\begin{cases} 3x + 2y = 12 \\ 2x + y = 7 \end{cases}",
            color=BLACK,
            font_size=56
        )
        system.next_to(title, DOWN, buff=0.6)
        self.play(Write(system))
        self.wait(1)

        # Multiply equation 2 by -2
        step_text = Text("Moltiplica eq. 2 per -2:", font_size=24, color=DARK_GRAY)
        step_text.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        eq1 = MathTex(r"-4x - 2y = -14", color=BLUE_D, font_size=50)
        eq1.next_to(step_text, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1.5)
        self.play(FadeOut(eq1))

        # Add equations
        step_text2 = Text("Somma le equazioni:", font_size=24, color=DARK_GRAY)
        step_text2.move_to(step_text)
        self.play(Transform(step_text, step_text2))
        self.wait(0.5)

        addition = VGroup(
            MathTex(r"3x + 2y = 12", color=BLACK, font_size=42),
            MathTex(r"+", color=BLACK, font_size=42),
            MathTex(r"-4x - 2y = -14", color=BLACK, font_size=42),
            Line(LEFT * 2.8, RIGHT * 2.8, color=BLACK, stroke_width=3)
        ).arrange(DOWN, buff=0.3)
        addition.next_to(step_text, DOWN, buff=0.5)

        self.play(FadeIn(addition[0:3]))
        self.wait(0.8)
        self.play(Create(addition[3]))
        self.wait(0.5)

        result = MathTex(r"-x = -2", color=BLACK, font_size=52)
        result.next_to(addition[3], DOWN, buff=0.4)
        self.play(Write(result))
        self.wait(1.5)

        # Solve
        self.play(FadeOut(addition), FadeOut(step_text))

        eq2 = MathTex(r"x = 2", color=GREEN_D, font_size=64)
        eq2.move_to(result)
        self.play(TransformMatchingTex(result, eq2))
        self.wait(1.5)

        # Find y
        y_text = Text("Sostituisci per trovare y:", font_size=24, color=DARK_GRAY)
        y_text.next_to(eq2, DOWN, buff=0.6)
        self.play(FadeIn(y_text))
        self.wait(0.5)

        eq3 = MathTex(r"2(2) + y = 7", color=BLACK, font_size=50)
        eq3.next_to(y_text, DOWN, buff=0.5)
        self.play(Write(eq3))
        self.wait(1)

        eq4 = MathTex(r"y = 3", color=GREEN_D, font_size=64)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1.5)

        # Solution
        self.play(FadeOut(eq2), FadeOut(eq4), FadeOut(system), FadeOut(y_text))

        solution = MathTex(r"x = 2, \quad y = 3", color=GREEN_D, font_size=72)
        solution.move_to(ORIGIN)
        self.play(Write(solution))

        box = SurroundingRectangle(solution, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(box))
        self.wait(2)


class CramerTeoriaEsempio(Scene):
    """Cramer: teoria + esempio."""

    def construct(self):
        self.camera.background_color = WHITE

        title = Text("Metodo di Cramer", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        # Theory
        theory_header = Text("Usa i determinanti:", font_size=28, color=DARK_BLUE)
        theory_header.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(theory_header))

        theory = VGroup(
            MathTex(r"\Delta = \begin{vmatrix} a & b \\ c & d \end{vmatrix}", color=BLACK, font_size=40),
            MathTex(r"x = \frac{\Delta_x}{\Delta}, \quad y = \frac{\Delta_y}{\Delta}", color=BLACK, font_size=36)
        ).arrange(DOWN, buff=0.4)
        theory.next_to(theory_header, DOWN, buff=0.5)

        for item in theory:
            self.play(FadeIn(item))
            self.wait(0.5)
        self.wait(1.5)
        self.play(FadeOut(theory), FadeOut(theory_header))

        # Example
        ex_label = Text("Esempio:", font_size=28, color=DARK_BLUE, weight=BOLD)
        ex_label.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(ex_label))

        system = MathTex(
            r"\begin{cases} 2x + 3y = 8 \\ x - y = 1 \end{cases}",
            color=BLACK,
            font_size=52
        )
        system.next_to(ex_label, DOWN, buff=0.6)
        self.play(Write(system))
        self.wait(1)

        # Calculate Δ
        step_text = Text("Calcola Δ:", font_size=24, color=DARK_GRAY)
        step_text.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        det_main = MathTex(
            r"\Delta = \begin{vmatrix} 2 & 3 \\ 1 & -1 \end{vmatrix} = -5",
            color=BLACK,
            font_size=44
        )
        det_main.next_to(step_text, DOWN, buff=0.5)
        self.play(Write(det_main))
        self.wait(1.5)
        self.play(FadeOut(step_text), FadeOut(det_main))

        # Calculate Δx
        step_text2 = Text("Calcola Δₓ:", font_size=24, color=DARK_GRAY)
        step_text2.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text2))
        self.wait(0.5)

        det_x = MathTex(
            r"\Delta_x = \begin{vmatrix} 8 & 3 \\ 1 & -1 \end{vmatrix} = -11",
            color=BLUE_D,
            font_size=44
        )
        det_x.next_to(step_text2, DOWN, buff=0.5)
        self.play(Write(det_x))
        self.wait(1)

        x_calc = MathTex(r"x = \frac{-11}{-5} = \frac{11}{5}", color=GREEN_D, font_size=48)
        x_calc.next_to(det_x, DOWN, buff=0.5)
        self.play(Write(x_calc))
        self.wait(1.5)

        self.play(FadeOut(step_text2), FadeOut(det_x), FadeOut(x_calc))

        # Calculate Δy
        step_text3 = Text("Calcola Δᵧ:", font_size=24, color=DARK_GRAY)
        step_text3.next_to(system, DOWN, buff=0.5)
        self.play(FadeIn(step_text3))
        self.wait(0.5)

        det_y = MathTex(
            r"\Delta_y = \begin{vmatrix} 2 & 8 \\ 1 & 1 \end{vmatrix} = -6",
            color=RED_D,
            font_size=44
        )
        det_y.next_to(step_text3, DOWN, buff=0.5)
        self.play(Write(det_y))
        self.wait(1)

        y_calc = MathTex(r"y = \frac{-6}{-5} = \frac{6}{5}", color=GREEN_D, font_size=48)
        y_calc.next_to(det_y, DOWN, buff=0.5)
        self.play(Write(y_calc))
        self.wait(1.5)

        # Solution
        self.play(FadeOut(step_text3), FadeOut(det_y), FadeOut(y_calc), FadeOut(system), FadeOut(ex_label))

        solution = MathTex(r"x = \frac{11}{5}, \quad y = \frac{6}{5}", color=GREEN_D, font_size=64)
        solution.move_to(ORIGIN)
        self.play(Write(solution))

        box = SurroundingRectangle(solution, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(box))
        self.wait(2)

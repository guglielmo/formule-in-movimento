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


class MonotoniaELogaritmo(Scene):
    """L'idea chiave: il verso della disuguaglianza dipende dalla base."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Disequazioni Logaritmiche", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        subtitle = Text("Tutto dipende dalla base", font_size=26, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.5)

        # Assi per i due logaritmi
        axes = Axes(
            x_range=[0, 8, 2],
            y_range=[-3, 3, 1],
            x_length=6.0,
            y_length=5.0,
            axis_config={"color": DARK_GRAY, "include_tip": True,
                         "tip_width": 0.15, "tip_height": 0.15},
        )
        axes.next_to(subtitle, DOWN, buff=0.5)
        x_label = Text("x", font_size=24, color=DARK_GRAY).next_to(axes.x_axis, RIGHT, buff=0.1)
        self.play(Create(axes), Write(x_label))
        self.wait(0.3)

        # log in base 2 (crescente) e in base 1/2 (decrescente)
        log2 = axes.plot(lambda x: np.log(x) / np.log(2), x_range=[0.12, 8], color=RED_D, stroke_width=5)
        log12 = axes.plot(lambda x: np.log(x) / np.log(0.5), x_range=[0.12, 8], color=BLUE_D, stroke_width=5)

        lab2 = MathTex(r"\log_{2} x", color=RED_D, font_size=32).next_to(axes.c2p(8, 3), LEFT, buff=0.1)
        lab12 = MathTex(r"\log_{1/2} x", color=BLUE_D, font_size=32).next_to(axes.c2p(8, -3), LEFT, buff=0.1)

        self.play(Create(log2), Write(lab2))
        self.play(Create(log12), Write(lab12))
        self.wait(1)

        cap = VGroup(
            Text("base > 1: crescente", font_size=24, color=RED_D, weight=BOLD),
            Text("0 < base < 1: decrescente", font_size=24, color=BLUE_D, weight=BOLD),
        ).arrange(DOWN, buff=0.2)
        cap.next_to(axes, DOWN, buff=0.4)
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.wait(2)

        # Passo alle due regole
        self.play(
            FadeOut(axes), FadeOut(x_label), FadeOut(log2), FadeOut(log12),
            FadeOut(lab2), FadeOut(lab12), FadeOut(cap),
        )
        self.wait(0.3)

        regola1_label = Text("Se base > 1 (crescente):", font_size=24, color=RED_D, weight=BOLD)
        regola1 = MathTex(
            r"\log_a f(x) > \log_a g(x) \;\Leftrightarrow\; f(x) > g(x)",
            color=BLACK, font_size=36,
        )
        verso1 = Text("stesso verso", font_size=22, color=RED_D, slant=ITALIC)
        blocco1 = VGroup(regola1_label, regola1, verso1).arrange(DOWN, buff=0.25)

        regola2_label = Text("Se 0 < base < 1 (decrescente):", font_size=24, color=BLUE_D, weight=BOLD)
        regola2 = MathTex(
            r"\log_a f(x) > \log_a g(x) \;\Leftrightarrow\; f(x) < g(x)",
            color=BLACK, font_size=36,
        )
        verso2 = Text("il verso si inverte!", font_size=22, color=BLUE_D, weight=BOLD, slant=ITALIC)
        blocco2 = VGroup(regola2_label, regola2, verso2).arrange(DOWN, buff=0.25)

        blocchi = VGroup(blocco1, blocco2).arrange(DOWN, buff=0.9)
        blocchi.next_to(subtitle, DOWN, buff=0.7)

        self.play(FadeIn(blocco1, shift=DOWN * 0.3))
        self.wait(1.5)
        self.play(FadeIn(blocco2, shift=DOWN * 0.3))

        box2 = SurroundingRectangle(blocco2, color=BLUE_D, buff=0.3, corner_radius=0.15, stroke_width=4)
        self.play(Create(box2))
        self.wait(2.5)


class DisequazioneCrescente(Scene):
    """Base maggiore di 1: il verso si conserva."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Base maggiore di 1", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        sub = Text("Il verso si conserva", font_size=24, color=RED_D, weight=BOLD)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(sub))
        self.wait(0.5)

        # Disequazione
        eq1 = MathTex(r"\log_{2}(2x-1)", ">", r"\log_{2}(x+3)", color=BLACK, font_size=44)
        eq1.next_to(sub, DOWN, buff=0.6)
        self.play(Write(eq1))
        self.wait(1)

        # Condizioni di esistenza
        ce_label = Text("Condizioni di esistenza:", font_size=22, color=RED_D, weight=BOLD)
        ce = MathTex(r"2x-1>0 \;\wedge\; x+3>0 \;\Rightarrow\; x>\tfrac{1}{2}", color=RED_D, font_size=32)
        ce_group = VGroup(ce_label, ce).arrange(DOWN, buff=0.2)
        ce_group.next_to(eq1, DOWN, buff=0.55)
        self.play(FadeIn(ce_label))
        self.play(Write(ce))
        self.wait(1.5)

        # Base 2 > 1: stesso verso
        hint = Text("Base 2 > 1: mantengo il verso", font_size=23, color=DARK_GRAY)
        hint.next_to(ce_group, DOWN, buff=0.55)
        self.play(FadeIn(hint))
        self.wait(0.5)

        eq2 = MathTex("2x-1", ">", "x+3", color=BLACK, font_size=48)
        eq2.next_to(hint, DOWN, buff=0.5)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait(1)

        eq3 = MathTex("x", ">", "4", color=BLACK, font_size=52)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)

        # Intersezione con le C.E.
        hint2 = Text("Interseco con le C.E.  (x > 1/2)", font_size=23, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        sol = MathTex("x > 4", color=GREEN_D, font_size=64)
        sol.move_to(eq3)
        self.play(TransformMatchingTex(eq3, sol), FadeOut(hint))
        sol_box = SurroundingRectangle(sol, color=GREEN_D, buff=0.35, corner_radius=0.2, stroke_width=5)
        self.play(Create(sol_box))
        self.wait(2.5)


class DisequazioneDecrescente(Scene):
    """Base tra 0 e 1: il verso si inverte."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Base tra 0 e 1", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        sub = Text("Attenzione: il verso si inverte!", font_size=24, color=BLUE_D, weight=BOLD)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(sub))
        self.wait(0.5)

        # Disequazione (stessi argomenti dell'esempio precedente, base 1/2)
        eq1 = MathTex(r"\log_{1/2}(2x-1)", ">", r"\log_{1/2}(x+3)", color=BLACK, font_size=42)
        eq1.next_to(sub, DOWN, buff=0.6)
        self.play(Write(eq1))
        self.wait(1)

        # Condizioni di esistenza (uguali a prima)
        ce_label = Text("Condizioni di esistenza:", font_size=22, color=RED_D, weight=BOLD)
        ce = MathTex(r"2x-1>0 \;\wedge\; x+3>0 \;\Rightarrow\; x>\tfrac{1}{2}", color=RED_D, font_size=32)
        ce_group = VGroup(ce_label, ce).arrange(DOWN, buff=0.2)
        ce_group.next_to(eq1, DOWN, buff=0.55)
        self.play(FadeIn(ce_label))
        self.play(Write(ce))
        self.wait(1.5)

        # Base 1/2 < 1: inverto il verso
        hint = Text("Base 1/2 < 1: INVERTO il verso", font_size=23, color=BLUE_D, weight=BOLD)
        hint.next_to(ce_group, DOWN, buff=0.55)
        self.play(FadeIn(hint))
        self.wait(0.5)

        # Il segno > diventa <
        eq2 = MathTex("2x-1", "<", "x+3", color=BLACK, font_size=48)
        eq2.next_to(hint, DOWN, buff=0.5)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        # Evidenzio il verso invertito
        self.play(Indicate(eq2[1], color=BLUE_D, scale_factor=1.6))
        self.wait(1.5)

        eq3 = MathTex("x", "<", "4", color=BLACK, font_size=52)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1)

        # Intersezione con le C.E. -> intervallo limitato
        hint2 = Text("Interseco con le C.E.  (x > 1/2)", font_size=23, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        sol = MathTex(r"\tfrac{1}{2} < x < 4", color=GREEN_D, font_size=60)
        sol.move_to(eq3)
        self.play(TransformMatchingTex(eq3, sol), FadeOut(hint))
        sol_box = SurroundingRectangle(sol, color=GREEN_D, buff=0.35, corner_radius=0.2, stroke_width=5)
        self.play(Create(sol_box))
        self.wait(2.5)


class EsempioCompleto(Scene):
    """Esempio con le proprietà: somma di logaritmi e disequazione di secondo grado."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Un Esempio Completo", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Disequazione con due logaritmi
        eq1 = MathTex(r"\log_{2} x", "+", r"\log_{2}(x-2)", "<", "3", color=BLACK, font_size=44)
        eq1.next_to(title, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(1)

        # C.E.
        ce = MathTex(r"x>0 \;\wedge\; x-2>0 \;\Rightarrow\; x>2", color=RED_D, font_size=32)
        ce.next_to(eq1, DOWN, buff=0.45)
        self.play(Write(ce))
        self.wait(1.5)

        # Proprietà del prodotto
        hint = Text("Proprietà del prodotto", font_size=22, color=DARK_GRAY)
        hint.next_to(ce, DOWN, buff=0.5)
        self.play(FadeIn(hint))

        eq2 = MathTex(r"\log_{2}\big[x(x-2)\big]", "<", "3", color=BLACK, font_size=44)
        eq2.next_to(hint, DOWN, buff=0.5)
        self.play(TransformMatchingTex(eq1.copy(), eq2))
        self.wait(1.5)

        # Base 2 > 1: stesso verso, applico la definizione
        hint2 = Text("Base 2 > 1: stesso verso", font_size=22, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        eq3 = MathTex("x(x-2)", "<", "2^{3}", color=BLACK, font_size=44)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1)

        eq4 = MathTex("x^{2}-2x-8", "<", "0", color=BLACK, font_size=44)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1)

        # Risolvo la disequazione di secondo grado
        hint3 = Text("Disequazione di 2° grado", font_size=22, color=DARK_GRAY)
        hint3.move_to(hint)
        self.play(Transform(hint, hint3))

        eq5 = MathTex("-2 < x < 4", color=BLACK, font_size=48)
        eq5.move_to(eq4)
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(1.5)

        # Intersezione con le C.E. (x > 2)
        hint4 = Text("Interseco con le C.E.  (x > 2)", font_size=22, color=DARK_GRAY)
        hint4.move_to(hint)
        self.play(Transform(hint, hint4))

        sol = MathTex("2 < x < 4", color=GREEN_D, font_size=60)
        sol.move_to(eq5)
        self.play(TransformMatchingTex(eq5, sol), FadeOut(hint))
        sol_box = SurroundingRectangle(sol, color=GREEN_D, buff=0.35, corner_radius=0.2, stroke_width=5)
        self.play(Create(sol_box))

        nota = Text("La C.E. taglia la parte x ≤ 2", font_size=22, color=DARK_GRAY, slant=ITALIC)
        nota.next_to(sol_box, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.wait(2.5)

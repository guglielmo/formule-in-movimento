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


class RipassoProprietaPotenze(Scene):
    """Ripasso delle proprietà delle potenze, indispensabili per gli esponenziali."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Proprietà delle Potenze", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        subtitle = Text("Il ripasso che serve per gli esponenziali", font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1)

        # Le cinque proprietà fondamentali, ciascuna con il nome e la formula
        regole = [
            ("Prodotto di potenze", r"a^m \cdot a^n = a^{m+n}"),
            ("Quoziente di potenze", r"\frac{a^m}{a^n} = a^{m-n}"),
            ("Potenza di potenza", r"\left(a^m\right)^n = a^{m \cdot n}"),
            ("Esponente zero", r"a^0 = 1"),
            ("Esponente negativo", r"a^{-n} = \frac{1}{a^n}"),
        ]

        blocchi = VGroup()
        for nome, formula in regole:
            etichetta = Text(nome, font_size=24, color=DARK_GRAY, weight=BOLD)
            espressione = MathTex(formula, color=BLACK, font_size=44)
            blocco = VGroup(etichetta, espressione).arrange(DOWN, buff=0.2)
            blocchi.add(blocco)

        blocchi.arrange(DOWN, buff=0.5)
        blocchi.next_to(subtitle, DOWN, buff=0.5)

        # Mostra le regole una per una
        for blocco in blocchi:
            self.play(FadeIn(blocco, shift=DOWN * 0.3))
            self.wait(0.6)

        self.wait(1.5)

        # Evidenzia che con a > 0 queste regole valgono per ogni esponente reale
        nota = Text(
            "Valgono per ogni esponente, se a > 0",
            font_size=24, color=GREEN_D, weight=BOLD, slant=ITALIC
        )
        nota.next_to(blocchi, DOWN, buff=0.5)
        box = SurroundingRectangle(nota, color=GREEN_D, buff=0.25, corner_radius=0.15, stroke_width=4)
        self.play(FadeIn(nota, shift=UP * 0.2), Create(box))
        self.wait(2.5)


class ModelloEsponenzialeCrescente(Scene):
    """Costruisce il modello di crescita esponenziale y = a^x con a > 1."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Modello Esponenziale", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Situazione concreta: una coltura di batteri che raddoppia ogni ora
        intro = VGroup(
            Text("Una coltura di batteri raddoppia ogni ora.", font_size=23, color=DARK_BLUE),
            Text("Partiamo da 1 batterio.", font_size=23, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.25)
        intro.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(intro, shift=UP * 0.2))
        self.wait(1.5)

        # Tabella dei valori: dopo x ore ci sono 2^x batteri
        tabella = VGroup(
            MathTex(r"x = 0 \;\Rightarrow\; 2^0 = 1", color=BLACK, font_size=40),
            MathTex(r"x = 1 \;\Rightarrow\; 2^1 = 2", color=BLACK, font_size=40),
            MathTex(r"x = 2 \;\Rightarrow\; 2^2 = 4", color=BLACK, font_size=40),
            MathTex(r"x = 3 \;\Rightarrow\; 2^3 = 8", color=BLACK, font_size=40),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        tabella.next_to(intro, DOWN, buff=0.5)

        for riga in tabella:
            self.play(FadeIn(riga, shift=RIGHT * 0.3))
            self.wait(0.4)
        self.wait(1)

        # Generalizzazione: la legge è y = 2^x
        legge = MathTex(r"y = 2^x", color=DARK_BLUE, font_size=64)
        legge.next_to(tabella, DOWN, buff=0.5)
        box = SurroundingRectangle(legge, color=DARK_BLUE, buff=0.25, corner_radius=0.15, stroke_width=5)
        self.play(Write(legge), Create(box))
        self.wait(2)

        # Transizione: passiamo al grafico
        legge_group = VGroup(legge, box)
        self.play(
            FadeOut(intro), FadeOut(tabella),
            legge_group.animate.next_to(title, DOWN, buff=0.4),
        )
        self.wait(0.5)

        # Grafico della crescita esponenziale
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 16, 4],
            x_length=6.0,
            y_length=6.5,
            axis_config={"color": DARK_BLUE, "include_tip": True,
                         "tip_width": 0.15, "tip_height": 0.15},
        )
        axes.next_to(legge_group, DOWN, buff=0.6)

        x_label = Text("x", font_size=26, color=DARK_BLUE).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("y", font_size=26, color=DARK_BLUE).next_to(axes.y_axis, UP, buff=0.1)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        curva = axes.plot(lambda x: 2 ** x, x_range=[0, 4], color=RED_D, stroke_width=5)
        self.play(Create(curva), run_time=2)
        self.wait(0.5)

        # Evidenzia alcuni punti della curva
        punti = VGroup()
        for x in [0, 1, 2, 3]:
            punti.add(Dot(axes.c2p(x, 2 ** x), color=RED_D, radius=0.08))
        self.play(LaggedStartMap(FadeIn, punti, scale=0.5, lag_ratio=0.3))
        self.wait(1)

        # Messaggio chiave: la crescita accelera sempre di più
        msg = Text("Cresce sempre più rapidamente!", font_size=26, color=GREEN_D, weight=BOLD)
        msg.next_to(axes, DOWN, buff=0.4)
        self.play(FadeIn(msg, shift=UP * 0.2))
        self.wait(2.5)


class EsponenzialeDecrescente(Scene):
    """Mostra l'esponenziale decrescente y = a^x con 0 < a < 1."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("L'Esponenziale Decrescente", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Situazione concreta: la quantità si dimezza ogni ora
        intro_text = Text("Ora la quantità si dimezza ogni ora.", font_size=23, color=DARK_BLUE)
        legge = MathTex(r"y = \left(\tfrac{1}{2}\right)^x", color=DARK_BLUE, font_size=52)
        intro = VGroup(intro_text, legge).arrange(DOWN, buff=0.35)
        intro.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(intro_text, shift=UP * 0.2))
        self.play(Write(legge))
        self.wait(1.5)

        # Tabella dei valori: i valori diminuiscono
        tabella = VGroup(
            MathTex(r"x = 0 \;\Rightarrow\; \left(\tfrac{1}{2}\right)^0 = 1", color=BLACK, font_size=36),
            MathTex(r"x = 1 \;\Rightarrow\; \left(\tfrac{1}{2}\right)^1 = \tfrac{1}{2}", color=BLACK, font_size=36),
            MathTex(r"x = 2 \;\Rightarrow\; \left(\tfrac{1}{2}\right)^2 = \tfrac{1}{4}", color=BLACK, font_size=36),
            MathTex(r"x = 3 \;\Rightarrow\; \left(\tfrac{1}{2}\right)^3 = \tfrac{1}{8}", color=BLACK, font_size=36),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        tabella.next_to(intro, DOWN, buff=0.5)

        for riga in tabella:
            self.play(FadeIn(riga, shift=RIGHT * 0.3))
            self.wait(0.4)
        self.wait(1)

        # Passa al grafico mantenendo la legge in alto
        self.play(
            FadeOut(tabella),
            FadeOut(intro_text),
            legge.animate.next_to(title, DOWN, buff=0.4),
        )
        self.wait(0.5)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.2, 0.5],
            x_length=6.0,
            y_length=6.5,
            axis_config={"color": DARK_BLUE, "include_tip": True,
                         "tip_width": 0.15, "tip_height": 0.15},
        )
        axes.next_to(legge, DOWN, buff=0.6)

        x_label = Text("x", font_size=26, color=DARK_BLUE).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("y", font_size=26, color=DARK_BLUE).next_to(axes.y_axis, UP, buff=0.1)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        curva = axes.plot(lambda x: 0.5 ** x, x_range=[0, 4], color=RED_D, stroke_width=5)
        self.play(Create(curva), run_time=2)
        self.wait(0.5)

        punti = VGroup()
        for x in [0, 1, 2, 3]:
            punti.add(Dot(axes.c2p(x, 0.5 ** x), color=RED_D, radius=0.08))
        self.play(LaggedStartMap(FadeIn, punti, scale=0.5, lag_ratio=0.3))
        self.wait(1)

        # Messaggio chiave: tende a zero ma non lo raggiunge mai
        msg = VGroup(
            Text("Decresce e si avvicina a zero", font_size=25, color=GREEN_D, weight=BOLD),
            Text("senza mai raggiungerlo.", font_size=25, color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.15)
        msg.next_to(axes, DOWN, buff=0.4)
        self.play(FadeIn(msg, shift=UP * 0.2))
        self.wait(2.5)


class EquazioniConfronto(Scene):
    """Equazioni esponenziali risolte con il metodo del confronto (stessa base)."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Equazioni con il Confronto", font_size=32, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Idea chiave del metodo
        idea_top = Text("Se le basi sono uguali...", font_size=25, color=DARK_BLUE)
        idea_mid = MathTex(r"a^{f(x)} = a^{g(x)} \;\Rightarrow\; f(x) = g(x)", color=BLACK, font_size=40)
        idea_bot = Text("...basta confrontare gli esponenti!", font_size=25, color=DARK_BLUE)
        idea = VGroup(idea_top, idea_mid, idea_bot).arrange(DOWN, buff=0.35)
        idea.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(idea_top, shift=UP * 0.2))
        self.play(Write(idea_mid))
        self.play(FadeIn(idea_bot, shift=UP * 0.2))
        self.wait(2)

        self.play(FadeOut(idea))
        self.wait(0.3)

        # Esempio guidato: 2^(x+1) = 8
        step = Text("Esempio:", font_size=26, color=DARK_GRAY, weight=BOLD)
        step.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(step))

        eq1 = MathTex("2^{x+1}", "=", "8", color=BLACK, font_size=64)
        eq1.next_to(step, DOWN, buff=0.6)
        self.play(Write(eq1))
        self.wait(1)

        # Passo 1: riscrivere 8 come potenza di 2
        hint = Text("Riscrivo 8 come potenza di 2", font_size=24, color=DARK_GRAY)
        hint.next_to(eq1, DOWN, buff=0.8)
        self.play(FadeIn(hint))
        self.wait(0.5)

        eq2 = MathTex("2^{x+1}", "=", "2^3", color=BLACK, font_size=64)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1)

        # Passo 2: stesse basi -> confronto gli esponenti
        hint2 = Text("Stessa base: confronto gli esponenti", font_size=24, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        # Evidenzia le due basi uguali
        base_sx = SurroundingRectangle(eq2[0][0], color=BLUE_D, buff=0.08)
        base_dx = SurroundingRectangle(eq2[2][0], color=BLUE_D, buff=0.08)
        self.play(Create(base_sx), Create(base_dx))
        self.wait(1)

        eq3 = MathTex("x+1", "=", "3", color=BLACK, font_size=64)
        eq3.move_to(eq2)
        self.play(
            TransformMatchingTex(eq2, eq3),
            FadeOut(base_sx), FadeOut(base_dx),
        )
        self.wait(1)

        # Passo 3: risolvo l'equazione di primo grado
        hint3 = Text("Risolvo l'equazione di primo grado", font_size=24, color=DARK_GRAY)
        hint3.move_to(hint)
        self.play(Transform(hint, hint3))
        self.wait(0.5)

        eq4 = MathTex("x", "=", "2", color=GREEN_D, font_size=80)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4), FadeOut(hint))

        sol_box = SurroundingRectangle(eq4, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(sol_box))

        sol_label = Text("Soluzione!", font_size=34, color=GREEN_D, weight=BOLD)
        sol_label.next_to(sol_box, DOWN, buff=0.7)
        self.play(FadeIn(sol_label, shift=UP * 0.3))
        self.wait(2.5)


class EquazioniVariabileAusiliaria(Scene):
    """Equazioni esponenziali risolte con la sostituzione di variabile ausiliaria."""

    def construct(self):
        # Tema chiaro
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Variabile Ausiliaria", font_size=34, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        subtitle = Text("Quando l'incognita compare due volte", font_size=24, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1)

        # Equazione di partenza: 4^x - 3·2^x - 4 = 0
        eq1 = MathTex("4^x", "-", "3 \\cdot 2^x", "-", "4", "=", "0", color=BLACK, font_size=54)
        eq1.next_to(subtitle, DOWN, buff=0.6)
        self.play(Write(eq1))
        self.wait(1.5)

        # Passo 1: noto che 4^x = (2^x)^2
        hint = Text("Riscrivo il primo termine come quadrato", font_size=23, color=DARK_GRAY)
        hint.next_to(eq1, DOWN, buff=0.7)
        self.play(FadeIn(hint))
        self.wait(0.5)

        eq2 = MathTex("(2^x)^2", "-", "3 \\cdot 2^x", "-", "4", "=", "0", color=BLACK, font_size=54)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1.5)

        # Passo 2: sostituzione t = 2^x
        hint2 = Text("Introduco la variabile ausiliaria t", font_size=23, color=DARK_GRAY)
        hint2.move_to(hint)
        self.play(Transform(hint, hint2))

        sost = MathTex(r"t = 2^x", color=DARK_BLUE, font_size=44)
        sost.to_corner(UR, buff=0.5)
        sost_box = SurroundingRectangle(sost, color=DARK_BLUE, buff=0.2, corner_radius=0.1, stroke_width=4)
        self.play(FadeIn(sost), Create(sost_box))
        self.wait(0.5)

        # L'equazione diventa di secondo grado in t
        eq3 = MathTex("t^2", "-", "3t", "-", "4", "=", "0", color=BLACK, font_size=60)
        eq3.move_to(eq2)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)

        # Passo 3: risolvo l'equazione di secondo grado
        hint3 = Text("Risolvo l'equazione di secondo grado", font_size=23, color=DARK_GRAY)
        hint3.move_to(hint)
        self.play(Transform(hint, hint3))
        self.wait(0.5)

        eq4 = MathTex("t = 4", r"\quad \vee \quad", "t = -1", color=BLACK, font_size=52)
        eq4.move_to(eq3)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1.5)

        # Passo 4: scarto la soluzione negativa (t deve essere positivo)
        hint4 = Text("t è sempre positivo: scarto t = -1", font_size=23, color=RED_D)
        hint4.move_to(hint)
        self.play(Transform(hint, hint4))

        scarto = Line(
            eq4[2].get_corner(DL) + LEFT * 0.1,
            eq4[2].get_corner(UR) + RIGHT * 0.1,
            color=RED_D, stroke_width=5,
        )
        self.play(Create(scarto))
        self.wait(1.5)

        # Passo 5: torno alla x con t = 4
        self.play(
            FadeOut(eq4[1]), FadeOut(eq4[2]), FadeOut(scarto),
            eq4[0].animate.move_to(eq3),
        )
        hint5 = Text("Torno all'incognita: ricavo x", font_size=23, color=DARK_GRAY)
        hint5.move_to(hint)
        self.play(Transform(hint, hint5))
        self.wait(0.5)

        eq5 = MathTex("2^x", "=", "4", color=BLACK, font_size=60)
        eq5.move_to(eq3)
        self.play(FadeOut(eq4[0]), FadeIn(eq5))
        self.wait(1)

        eq6 = MathTex("2^x", "=", "2^2", color=BLACK, font_size=60)
        eq6.move_to(eq5)
        self.play(TransformMatchingTex(eq5, eq6))
        self.wait(1)

        # Soluzione finale
        eq7 = MathTex("x", "=", "2", color=GREEN_D, font_size=80)
        eq7.move_to(eq6)
        self.play(
            TransformMatchingTex(eq6, eq7),
            FadeOut(hint), FadeOut(sost), FadeOut(sost_box),
        )

        sol_box = SurroundingRectangle(eq7, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(sol_box))

        sol_label = Text("Soluzione!", font_size=34, color=GREEN_D, weight=BOLD)
        sol_label.next_to(sol_box, DOWN, buff=0.7)
        self.play(FadeIn(sol_label, shift=UP * 0.3))
        self.wait(2.5)

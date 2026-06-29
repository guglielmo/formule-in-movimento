from manim import *
import sys, os
import numpy as np

# Rende importabile il package condiviso 'animations' (template, moduli, ...)
# calcolando la root del progetto: niente path hardcoded, funziona in locale e in CI.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from animations.vertical_template import VerticalTemplate


# ============================================================================
# Helper comuni
# ============================================================================

def titolo(testo, sottotitolo=None):
    """Crea un titolo (e sottotitolo) standard in alto, tema chiaro."""
    t = Text(testo, font_size=40, color=BLACK, weight=BOLD)
    t.to_edge(UP, buff=0.3)
    if sottotitolo:
        s = Text(sottotitolo, font_size=26, color=DARK_BLUE)
        s.next_to(t, DOWN, buff=0.2)
        return VGroup(t, s)
    return VGroup(t)


# ============================================================================
# 1. INTRODUZIONE: che cos'è un'onda
# ============================================================================

class IntroOnde(Scene):
    """Hook: un'onda trasporta energia, non materia."""

    def construct(self):
        self.camera.background_color = WHITE

        intestazione = titolo("Le Onde", "Che cos'è un'onda?")
        self.play(Write(intestazione))
        self.wait(0.5)

        # Onda viaggiante (trasversale)
        t = ValueTracker(0)
        A, k, w = 1.2, 2.0, 2.5
        centro_y = 1.5

        onda = always_redraw(
            lambda: FunctionGraph(
                lambda x: A * np.sin(k * x - w * t.get_value()),
                x_range=[-3.6, 3.6, 0.02],
                color=BLUE_D,
                stroke_width=6,
            ).move_to(UP * centro_y)
        )

        # Un punto che oscilla SOLO in verticale (x fisso): la materia non avanza
        x0 = 0.0
        punto = always_redraw(
            lambda: Dot(
                point=[x0, centro_y + A * np.sin(k * x0 - w * t.get_value()), 0],
                color=RED_D,
                radius=0.12,
            )
        )
        freccia_osc = always_redraw(
            lambda: DoubleArrow(
                start=[x0 + 0.6, centro_y - A, 0],
                end=[x0 + 0.6, centro_y + A, 0],
                color=RED_D,
                buff=0,
                stroke_width=3,
                tip_length=0.18,
            )
        )

        self.add(onda)
        self.play(FadeIn(punto), GrowFromCenter(freccia_osc))

        # Freccia di propagazione dell'onda (verso destra)
        freccia_prop = Arrow(
            start=[-1.0, centro_y - 2.3, 0],
            end=[1.0, centro_y - 2.3, 0],
            color=DARK_GRAY,
            buff=0,
        )
        etichetta_prop = Text("propagazione", font_size=24, color=DARK_GRAY)
        etichetta_prop.next_to(freccia_prop, DOWN, buff=0.15)
        self.play(GrowArrow(freccia_prop), FadeIn(etichetta_prop))

        self.play(t.animate.set_value(6), run_time=6, rate_func=linear)

        # Messaggio chiave
        msg = VGroup(
            Text("Un'onda è una perturbazione che si propaga", font_size=28, color=BLACK),
            Text("trasportando ENERGIA, non materia.", font_size=28, color=GREEN_D, weight=BOLD),
        ).arrange(DOWN, buff=0.25)
        msg.move_to(DOWN * 3.5)
        self.play(Write(msg))
        self.play(t.animate.set_value(10), run_time=4, rate_func=linear)
        self.wait(1)


# ============================================================================
# 2. ONDE TRASVERSALI vs LONGITUDINALI
# ============================================================================

class OndeTrasversaliLongitudinali(VerticalTemplate):
    """Confronto tra oscillazione perpendicolare e parallela alla propagazione."""

    def construct(self):
        self.setup_vertical_layout(
            title_text="Trasversali e Longitudinali",
            subtitle_text="Come oscillano le particelle?",
        )

        t = ValueTracker(0)
        base_xs = np.linspace(-3.2, 3.2, 26)
        k, w = 2.0, 2.5

        # --- BLOCCO ALTO: onda trasversale (oscillazione verticale) ---
        cy_top = self.top_block_center

        def trasversale():
            dots = VGroup()
            for bx in base_xs:
                dy = 0.6 * np.sin(k * bx - w * t.get_value())
                dots.add(Dot([bx, cy_top + dy, 0], radius=0.06, color=RED_D))
            return dots

        onda_t = always_redraw(trasversale)
        lab_t = Text("Trasversale", font_size=26, color=RED_D, weight=BOLD)
        lab_t.move_to([0, cy_top + 1.6, 0])
        sub_t = Text("oscillazione perpendicolare", font_size=20, color=DARK_GRAY)
        sub_t.move_to([0, cy_top - 1.5, 0])
        prop_t = Arrow([1.0, cy_top - 1.0, 0], [2.6, cy_top - 1.0, 0], color=DARK_GRAY, buff=0)
        osc_t = DoubleArrow([-2.6, cy_top - 0.7, 0], [-2.6, cy_top + 0.7, 0],
                            color=RED_D, buff=0, stroke_width=3, tip_length=0.16)

        self.play(FadeIn(lab_t), FadeIn(sub_t))
        self.add(onda_t)
        self.play(GrowArrow(prop_t), GrowFromCenter(osc_t))

        # --- BLOCCO BASSO: onda longitudinale (oscillazione orizzontale) ---
        cy_bot = self.bottom_block_center

        def longitudinale():
            dots = VGroup()
            for bx in base_xs:
                dx = 0.32 * np.sin(k * bx - w * t.get_value())
                dots.add(Dot([bx + dx, cy_bot, 0], radius=0.07, color=DARK_BLUE))
            return dots

        onda_l = always_redraw(longitudinale)
        lab_l = Text("Longitudinale", font_size=26, color=DARK_BLUE, weight=BOLD)
        lab_l.move_to([0, cy_bot + 1.4, 0])
        sub_l = Text("oscillazione parallela (compressioni)", font_size=20, color=DARK_GRAY)
        sub_l.move_to([0, cy_bot - 1.4, 0])
        prop_l = Arrow([1.0, cy_bot - 0.8, 0], [2.6, cy_bot - 0.8, 0], color=DARK_GRAY, buff=0)
        osc_l = DoubleArrow([-2.9, cy_bot + 0.7, 0], [-1.9, cy_bot + 0.7, 0],
                            color=DARK_BLUE, buff=0, stroke_width=3, tip_length=0.16)

        self.play(FadeIn(lab_l), FadeIn(sub_l))
        self.add(onda_l)
        self.play(GrowArrow(prop_l), GrowFromCenter(osc_l))

        self.play(t.animate.set_value(9), run_time=9, rate_func=linear)
        self.wait(1)


# ============================================================================
# 3. AMPIEZZA, LUNGHEZZA D'ONDA, PERIODO, FREQUENZA
# ============================================================================

class AmpiezzaFrequenza(Scene):
    """Grandezze caratteristiche di un'onda periodica."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Le grandezze di un'onda", "Ampiezza, lunghezza d'onda, frequenza")
        self.play(Write(intestazione))
        self.wait(0.3)

        A = 1.4
        k = 2 * PI / 3.0  # lunghezza d'onda = 3 unità
        centro_y = 1.2

        asse = Line([-3.6, centro_y, 0], [3.6, centro_y, 0], color=DARK_GRAY, stroke_width=2)
        onda = FunctionGraph(
            lambda x: A * np.sin(k * x),
            x_range=[-3.6, 3.6, 0.02],
            color=BLUE_D,
            stroke_width=6,
        ).move_to(UP * centro_y)
        self.play(Create(asse), Create(onda), run_time=2)

        # Ampiezza: dalla linea di equilibrio alla cresta
        x_cresta = (PI / 2) / k  # prima cresta
        amp = DoubleArrow(
            [x_cresta, centro_y, 0], [x_cresta, centro_y + A, 0],
            color=RED_D, buff=0, stroke_width=3, tip_length=0.18,
        )
        lab_amp = MathTex(r"A", color=RED_D, font_size=44).next_to(amp, RIGHT, buff=0.15)
        cap_amp = Text("ampiezza", font_size=22, color=RED_D).next_to(lab_amp, RIGHT, buff=0.1)
        self.play(GrowFromCenter(amp), Write(lab_amp), FadeIn(cap_amp))

        # Lunghezza d'onda: tra due creste consecutive
        x1 = x_cresta
        x2 = x_cresta + 3.0
        lam = DoubleArrow(
            [x1, centro_y + A + 0.4, 0], [x2, centro_y + A + 0.4, 0],
            color=GREEN_D, buff=0, stroke_width=3, tip_length=0.18,
        )
        lab_lam = MathTex(r"\lambda", color=GREEN_D, font_size=44).next_to(lam, UP, buff=0.1)
        self.play(GrowFromCenter(lam), Write(lab_lam))
        self.wait(0.5)

        # Relazioni fondamentali
        relazioni = VGroup(
            MathTex(r"T = \text{periodo}\ (\mathrm{s})", color=BLACK, font_size=40),
            MathTex(r"f = \frac{1}{T}\quad (\mathrm{Hz})", color=BLACK, font_size=40),
            MathTex(r"v = \lambda\, f = \frac{\lambda}{T}", color=DARK_BLUE, font_size=44),
        ).arrange(DOWN, buff=0.45)
        relazioni.move_to(DOWN * 3.6)
        box = SurroundingRectangle(relazioni[2], color=DARK_BLUE, buff=0.2, corner_radius=0.15)
        self.play(Write(relazioni[0]))
        self.play(Write(relazioni[1]))
        self.play(Write(relazioni[2]), Create(box))
        self.wait(1.5)


# ============================================================================
# 4. ESEMPI REALI: corde, suono, terremoti
# ============================================================================

class EsempiOnde(Scene):
    """Onde nella vita reale: corde, suono, terremoti."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Onde tutto intorno a noi", "Corde, suono, terremoti")
        self.play(Write(intestazione))
        self.wait(0.3)

        # --- Corde ---
        corda = FunctionGraph(lambda x: 0.4 * np.sin(2 * PI / 1.5 * x),
                              x_range=[-2.2, 2.2, 0.02], color=RED_D, stroke_width=5)
        corda.move_to([0, 3.4, 0])
        txt_corda = VGroup(
            Text("Corde", font_size=28, color=RED_D, weight=BOLD),
            Text("chitarra, violino — onde trasversali", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.1).move_to([0, 2.2, 0])
        self.play(Create(corda), Write(txt_corda))

        # --- Suono: fronti d'onda circolari ---
        cerchi = VGroup(*[
            Circle(radius=r, color=DARK_BLUE, stroke_width=3, stroke_opacity=max(0.2, 1 - 0.2 * i))
            for i, r in enumerate([0.5, 1.0, 1.5, 2.0])
        ])
        for c in cerchi:
            c.move_to([0, -0.2, 0])
        sorgente = Dot([0, -0.2, 0], color=DARK_BLUE, radius=0.1)
        txt_suono = VGroup(
            Text("Suono", font_size=28, color=DARK_BLUE, weight=BOLD),
            Text("compressioni dell'aria — onde longitudinali", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.1).move_to([0, -1.9, 0])
        self.play(FadeIn(sorgente))
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cerchi], lag_ratio=0.25))
        self.play(Write(txt_suono))

        # --- Terremoti ---
        suolo = Rectangle(width=5.0, height=1.2, color=DARK_GRAY, fill_color=GREY_BROWN,
                          fill_opacity=0.35, stroke_width=2).move_to([0, -4.3, 0])
        sisma = FunctionGraph(lambda x: 0.25 * np.sin(2 * PI / 0.8 * x),
                              x_range=[-2.3, 2.3, 0.02], color=GREEN_D, stroke_width=4)
        sisma.move_to([0, -4.3, 0])
        txt_terr = VGroup(
            Text("Terremoti", font_size=28, color=GREEN_D, weight=BOLD),
            Text("onde P (long.) e onde S (trasv.)", font_size=22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.1).move_to([0, -5.6, 0])
        self.play(FadeIn(suolo), Create(sisma))
        self.play(Write(txt_terr))
        self.wait(1.5)


# ============================================================================
# 5. ONDE PERIODICHE vs IMPULSIVE
# ============================================================================

class OndePeriodicheImpulsive(VerticalTemplate):
    """Un'onda che si ripete contro una singola perturbazione."""

    def construct(self):
        self.setup_vertical_layout(
            title_text="Periodiche e Impulsive",
            subtitle_text="Onda continua o singolo impulso",
        )

        t = ValueTracker(0)

        # --- BLOCCO ALTO: onda periodica ---
        cy_top = self.top_block_center
        periodica = always_redraw(
            lambda: FunctionGraph(
                lambda x: 0.8 * np.sin(3 * x - 3 * t.get_value()),
                x_range=[-3.4, 3.4, 0.02],
                color=BLUE_D,
                stroke_width=5,
            ).move_to(UP * cy_top)
        )
        lab_p = Text("Periodica", font_size=26, color=BLUE_D, weight=BOLD).move_to([0, cy_top + 1.6, 0])
        sub_p = Text("si ripete nel tempo e nello spazio", font_size=20, color=DARK_GRAY).move_to([0, cy_top - 1.6, 0])
        self.play(FadeIn(lab_p), FadeIn(sub_p))
        self.add(periodica)

        # --- BLOCCO BASSO: impulso singolo (gaussiano) che viaggia ---
        cy_bot = self.bottom_block_center

        def impulso_y():
            x0 = -3.0 + 1.0 * t.get_value()  # il picco avanza nel tempo
            g = FunctionGraph(
                lambda x: 1.0 * np.exp(-((x - x0) ** 2) / 0.15),
                x_range=[-3.4, 3.4, 0.02],
                color=RED_D,
                stroke_width=5,
            )
            g.shift(UP * cy_bot)
            return g

        onda_imp = always_redraw(impulso_y)
        linea_base = Line([-3.4, cy_bot, 0], [3.4, cy_bot, 0], color=DARK_GRAY, stroke_width=2)
        lab_i = Text("Impulsiva", font_size=26, color=RED_D, weight=BOLD).move_to([0, cy_bot + 1.6, 0])
        sub_i = Text("una singola perturbazione", font_size=20, color=DARK_GRAY).move_to([0, cy_bot - 1.4, 0])
        self.play(FadeIn(lab_i), FadeIn(sub_i), Create(linea_base))
        self.add(onda_imp)

        self.play(t.animate.set_value(6), run_time=7, rate_func=linear)
        self.wait(1)


# ============================================================================
# 6. ONDE COMPLESSE: somma di sinusoidi
# ============================================================================

class OndeComplesse(Scene):
    """Un'onda complessa è la somma di onde semplici."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("Onde complesse", "Somma di onde semplici")
        self.play(Write(intestazione))
        self.wait(0.3)

        def armonica(f, amp, colore, y):
            g = FunctionGraph(lambda x: amp * np.sin(f * x),
                              x_range=[-3.4, 3.4, 0.02], color=colore, stroke_width=4)
            g.move_to(UP * y)
            return g

        y1 = armonica(2.0, 0.7, BLUE_D, 3.3)
        lab1 = MathTex(r"y_1 = A_1\sin(k_1 x)", color=BLUE_D, font_size=34).next_to(y1, UP, buff=0.15)
        y2 = armonica(4.0, 0.45, GREEN_D, 1.2)
        lab2 = MathTex(r"y_2 = A_2\sin(k_2 x)", color=GREEN_D, font_size=34).next_to(y2, UP, buff=0.15)

        self.play(Create(y1), Write(lab1))
        self.play(Create(y2), Write(lab2))
        self.wait(0.5)

        # Onda risultante = somma
        somma = FunctionGraph(
            lambda x: 0.7 * np.sin(2.0 * x) + 0.45 * np.sin(4.0 * x),
            x_range=[-3.4, 3.4, 0.02], color=RED_D, stroke_width=6,
        ).move_to(DOWN * 2.6)
        lab_s = MathTex(r"y = y_1 + y_2", color=RED_D, font_size=40).next_to(somma, UP, buff=0.2)

        self.play(
            TransformFromCopy(VGroup(y1, y2), somma),
            Write(lab_s),
            run_time=2,
        )
        nota = Text("Qualsiasi onda complessa = somma di sinusoidi",
                    font_size=24, color=BLACK).move_to(DOWN * 5.4)
        self.play(FadeIn(nota))
        self.wait(1.5)


# ============================================================================
# 7. EQUAZIONE GENERALE DELL'ONDA E CALCOLO DELLA FASE
# ============================================================================

class EquazioneOnda(Scene):
    """Equazione dell'onda armonica e calcolo della fase con esempio numerico."""

    def construct(self):
        self.camera.background_color = WHITE
        intestazione = titolo("L'equazione dell'onda", "y(x, t) e la fase")
        self.play(Write(intestazione))
        self.wait(0.3)

        # Equazione generale
        eq = MathTex(r"y(x,t) = A\,\sin(kx - \omega t + \varphi_0)",
                     color=BLACK, font_size=46)
        eq.next_to(intestazione, DOWN, buff=0.6)
        box_eq = SurroundingRectangle(eq, color=DARK_BLUE, buff=0.25, corner_radius=0.15)
        self.play(Write(eq), Create(box_eq))

        # Legenda dei simboli
        legenda = VGroup(
            MathTex(r"A = \text{ampiezza}", color=BLACK, font_size=34),
            MathTex(r"k = \tfrac{2\pi}{\lambda} = \text{numero d'onda}", color=BLACK, font_size=34),
            MathTex(r"\omega = 2\pi f = \text{pulsazione}", color=BLACK, font_size=34),
            MathTex(r"\varphi_0 = \text{fase iniziale}", color=BLACK, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legenda.next_to(box_eq, DOWN, buff=0.5)
        self.play(LaggedStart(*[Write(r) for r in legenda], lag_ratio=0.3))
        self.wait(1)

        # La fase
        fase = MathTex(r"\varphi(x,t) = kx - \omega t + \varphi_0",
                       color=DARK_BLUE, font_size=42)
        fase.next_to(legenda, DOWN, buff=0.5)
        self.play(Write(fase))
        self.wait(0.8)

        # Esempio numerico
        self.play(
            FadeOut(legenda), FadeOut(eq), FadeOut(box_eq),
            fase.animate.next_to(intestazione, DOWN, buff=0.6),
        )

        dati = MathTex(
            r"k=\pi\,\tfrac{\mathrm{rad}}{\mathrm{m}},\ "
            r"\omega=4\pi\,\tfrac{\mathrm{rad}}{\mathrm{s}},\ "
            r"\varphi_0=0",
            color=BLACK, font_size=34,
        ).next_to(fase, DOWN, buff=0.5)
        cond = MathTex(r"x = 0{,}5\ \mathrm{m}, \quad t = 0{,}25\ \mathrm{s}",
                       color=BLACK, font_size=34).next_to(dati, DOWN, buff=0.3)
        self.play(Write(dati), Write(cond))
        self.wait(0.5)

        passo1 = MathTex(r"\varphi = \pi\cdot 0{,}5 - 4\pi\cdot 0{,}25 + 0",
                         color=BLACK, font_size=38).next_to(cond, DOWN, buff=0.5)
        passo2 = MathTex(r"\varphi = 0{,}5\pi - \pi = -\tfrac{\pi}{2}\ \mathrm{rad}",
                         color=BLACK, font_size=38).next_to(passo1, DOWN, buff=0.35)
        self.play(Write(passo1))
        self.play(Write(passo2))
        self.wait(0.5)

        # Valore dello spostamento
        ris = MathTex(r"y = A\sin\!\left(-\tfrac{\pi}{2}\right) = -A",
                      color=GREEN_D, font_size=46).next_to(passo2, DOWN, buff=0.5)
        box_ris = SurroundingRectangle(ris, color=GREEN_D, buff=0.25, corner_radius=0.15)
        self.play(Write(ris), Create(box_ris))
        self.wait(2)

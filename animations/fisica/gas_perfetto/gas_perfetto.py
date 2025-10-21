from manim import *
import sys
sys.path.insert(0, '/home/gu/projects/formule-in-movimento')
from animations.vertical_template import VerticalTemplate
from animations.gas_module import Gas

class TrasformazioneIsoterma(VerticalTemplate):
    """
    Trasformazione isoterma: temperatura costante (T = cost)
    Legge di Boyle: pV = costante
    """
    def construct(self):
        # Setup standard vertical layout
        self.setup_vertical_layout(
            title_text="Trasformazione Isoterma",
            subtitle_text="Temperatura costante (T = cost)"
        )

        # === TOP BLOCK: Physical Animation (Piston) ===
        animation_center_y = self.top_block_center

        # Contenitore (cilindro) - centered in top block
        container_height = 3.5
        container_width = 2.5
        container_bottom = animation_center_y - container_height / 2
        container_top = animation_center_y + container_height / 2

        # Pareti del contenitore (linee spesse)
        container_left = Line(
            start=LEFT * (container_width/2) + UP * container_bottom,
            end=LEFT * (container_width/2) + UP * container_top,
            color=DARK_BLUE,
            stroke_width=6
        )
        container_right = Line(
            start=RIGHT * (container_width/2) + UP * container_bottom,
            end=RIGHT * (container_width/2) + UP * container_top,
            color=DARK_BLUE,
            stroke_width=6
        )
        container_bottom_line = Line(
            start=LEFT * (container_width/2) + UP * container_bottom,
            end=RIGHT * (container_width/2) + UP * container_bottom,
            color=DARK_BLUE,
            stroke_width=6
        )

        # Pistone (mobile) - inizia a metà altezza
        piston_start_y = container_bottom + 2.5
        piston = Rectangle(
            height=0.15, width=container_width, color=RED_D, fill_opacity=1
        ).move_to(UP * piston_start_y)
        piston_rod = Rectangle(
            height=0.3, width=0.08, color=RED_D, fill_opacity=1
        ).next_to(piston, UP, buff=0)
        piston_group = VGroup(piston, piston_rod)

        # Gas usando il modulo Gas - temperatura costante (300K, colore blu)
        gas_height_start = piston_start_y - container_bottom - 0.15
        gas_center_y_start = container_bottom + gas_height_start / 2
        gas_width = container_width - 0.24  # Match container internal width

        gas = Gas(
            width=gas_width,
            height=gas_height_start,
            temperature=300,  # Isotherma: temperatura costante
            num_particles=30,
            particle_scale=2.0,
            center=np.array([0, gas_center_y_start, 0])
        )

        # Etichetta temperatura
        temp_label = MathTex("T = \\text{cost}", color=BLUE_D, font_size=32)
        temp_label.next_to(container_right, RIGHT, buff=0.4)

        # === BOTTOM BLOCK: Chart (Pressure vs Volume) ===
        # Create axes (without animation yet)
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5.0,
            y_length=4.0,
            axis_config={"color": DARK_BLUE, "include_tip": True,
                        "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(UP * self.bottom_block_center)

        x_label = Text("p", font_size=28, color=DARK_BLUE).next_to(
            axes.x_axis, RIGHT, buff=0.1
        )
        y_label = Text("V", font_size=28, color=DARK_BLUE).next_to(
            axes.y_axis, UP, buff=0.1
        )

        # Disegna schema fisico e assi insieme
        self.play(
            Create(container_left),
            Create(container_right),
            Create(container_bottom_line),
            Create(piston_group),
            FadeIn(gas),
            Write(temp_label),
            Create(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait(0.5)

        # Animazione: pistone si sposta (volume cambia, pressione cambia)
        # Curva iperbolica (legge di Boyle: pV = costante, con k = 4)
        # La curva parte da p basso (V alto) e va verso p alto (V basso)
        k = 4  # Costante pV
        p_start = 1.0  # Pressione iniziale (bassa) - V = 4/1 = 4
        p_end = 4.5    # Pressione finale (alta) - V = 4/4.5 ≈ 0.89

        pressure_curve = axes.plot(
            lambda p: k / p,  # Andamento iperbolico: V = k/p
            x_range=[p_start, p_end],  # Da p basso a p alto
            color=RED_D,
            stroke_width=4
        )

        # Punto che traccia la curva (inizia da p=1.0, V=4)
        dot = Dot(color=RED_D, radius=0.08).move_to(axes.c2p(p_start, k / p_start))

        # === FASE 1: Compressione (pistone scende, volume diminuisce, pressione aumenta) ===
        piston_compressed_y = container_bottom + 1.5
        gas_height_compressed = piston_compressed_y - container_bottom - 0.15

        # Animazione di compressione del gas
        def compress_gas(mob, alpha):
            current_height = interpolate(gas_height_start, gas_height_compressed, alpha)
            new_center_y = container_bottom + current_height / 2

            # Resize the gas container
            mob.resize(gas_width, current_height)

            # Move gas center (shift all particles)
            shift_amount = new_center_y - mob._container_center[1]
            for particle in mob.particles:
                particle.shift(UP * shift_amount)
            mob._container_center = np.array([0, new_center_y, 0])

        self.play(
            piston_group.animate.move_to(UP * piston_compressed_y),
            UpdateFromAlphaFunc(gas, compress_gas),
            Create(pressure_curve),
            MoveAlongPath(dot, pressure_curve),
            run_time=3,
            rate_func=linear
        )

        self.wait(0.5)

        # === FASE 2: Espansione (pistone sale, volume aumenta, pressione diminuisce) ===
        # Animazione di espansione del gas
        def expand_gas(mob, alpha):
            current_height = interpolate(gas_height_compressed, gas_height_start, alpha)
            new_center_y = container_bottom + current_height / 2

            # Resize the gas container
            mob.resize(gas_width, current_height)

            # Move gas center (shift all particles)
            shift_amount = new_center_y - mob._container_center[1]
            for particle in mob.particles:
                particle.shift(UP * shift_amount)
            mob._container_center = np.array([0, new_center_y, 0])

        # Crea un tracker per animare il punto lungo la curva al contrario
        pressure_tracker = ValueTracker(p_end)

        def update_dot(mob):
            p_val = pressure_tracker.get_value()
            mob.move_to(axes.c2p(p_val, k / p_val))

        dot.add_updater(update_dot)

        self.play(
            piston_group.animate.move_to(UP * piston_start_y),
            UpdateFromAlphaFunc(gas, expand_gas),
            pressure_tracker.animate.set_value(p_start),
            run_time=3,
            rate_func=linear
        )

        dot.remove_updater(update_dot)

        # Etichetta legge di Boyle
        boyle_law = MathTex("pV = \\text{cost}", color=BLACK, font_size=32)
        boyle_law.next_to(axes, DOWN, buff=0.4)
        self.play(Write(boyle_law))

        self.wait(1)


class TrasformazioneIsocora(VerticalTemplate):
    """
    Trasformazione isocora: volume costante (V = cost)
    Legge di Gay-Lussac (o prima legge di Volta): p/T = costante
    """
    def construct(self):
        # Setup standard vertical layout
        self.setup_vertical_layout(
            title_text="Trasformazione Isocora",
            subtitle_text="Volume costante (V = cost)"
        )

        # === TOP BLOCK: Physical Animation (Rigid Container) ===
        animation_center_y = self.top_block_center

        # Contenitore rigido (chiuso) - centered in top block
        container_height = 3.5
        container_width = 2.5
        container_bottom = animation_center_y - container_height / 2
        container_top = animation_center_y + container_height / 2

        # Pareti del contenitore (linee spesse)
        container_left = Line(
            start=LEFT * (container_width/2) + UP * container_bottom,
            end=LEFT * (container_width/2) + UP * container_top,
            color=DARK_BLUE,
            stroke_width=6
        )
        container_right = Line(
            start=RIGHT * (container_width/2) + UP * container_bottom,
            end=RIGHT * (container_width/2) + UP * container_top,
            color=DARK_BLUE,
            stroke_width=6
        )
        container_bottom_line = Line(
            start=LEFT * (container_width/2) + UP * container_bottom,
            end=RIGHT * (container_width/2) + UP * container_bottom,
            color=DARK_BLUE,
            stroke_width=6
        )

        # Coperchio fisso (linea spessa)
        lid = Line(
            start=LEFT * (container_width/2) + UP * container_top,
            end=RIGHT * (container_width/2) + UP * container_top,
            color=DARK_BLUE,
            stroke_width=6
        )

        # Gas usando il modulo Gas - volume costante, temperatura varia
        gas_width = container_width - 0.24
        gas_height = container_height - 0.24  # Riempie il contenitore (volume costante)

        gas = Gas(
            width=gas_width,
            height=gas_height,
            temperature=300,  # Temperatura iniziale (bassa)
            num_particles=30,
            particle_scale=2.0,
            center=np.array([0, animation_center_y, 0])
        )

        # Etichetta volume
        vol_label = MathTex("V = \\text{cost}", color=DARK_BLUE, font_size=32)
        vol_label.move_to(RIGHT * (container_width/2 + 0.8) + UP * animation_center_y)

        # === BOTTOM BLOCK: Chart (Pressure vs Temperature) ===
        # Create axes (without animation yet)
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5.0,
            y_length=4.0,
            axis_config={"color": DARK_BLUE, "include_tip": True,
                        "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(UP * self.bottom_block_center)

        x_label = Text("T", font_size=28, color=DARK_BLUE).next_to(
            axes.x_axis, RIGHT, buff=0.1
        )
        y_label = Text("p", font_size=28, color=DARK_BLUE).next_to(
            axes.y_axis, UP, buff=0.1
        )

        # Indicatore di calore (fiamma sotto il contenitore)
        flame = Polygon(
            UP * container_bottom + DOWN * 0.2 + LEFT * 0.3,
            UP * container_bottom + DOWN * 0.2 + RIGHT * 0.3,
            UP * container_bottom + DOWN * 0.6,
            color=RED_D, fill_opacity=0.7, stroke_width=0
        )
        heat_label = Text("Calore", font_size=24, color=RED_D)
        heat_label.next_to(flame, DOWN, buff=0.15)

        # Disegna schema e assi insieme
        self.play(
            Create(container_left),
            Create(container_right),
            Create(container_bottom_line),
            Create(lid),
            FadeIn(gas),
            Write(vol_label),
            Create(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait(0.5)

        # Aggiungi fiamma
        self.play(FadeIn(flame), Write(heat_label))

        # Animazione: riscaldamento, particelle si muovono più velocemente, pressione aumenta
        # Curva pressione crescente (lineare con temperatura)
        pressure_curve = axes.plot(
            lambda t: 1 + 0.7 * t,  # Andamento lineare
            x_range=[0, 4.5],
            color=RED_D,
            stroke_width=4
        )

        # Punto che traccia la curva
        dot = Dot(color=RED_D, radius=0.08).move_to(axes.c2p(0, 1))

        # Animazione simultanea: gas si riscalda (temperatura aumenta)
        # Usa ValueTracker per non sospendere l'updater del gas
        temp_tracker = ValueTracker(300)
        prev_temp = [300.0]  # Usa lista per modificare in closure

        def update_gas_temp(mob):
            new_temp = temp_tracker.get_value()

            # Solo aggiorna se temperatura è cambiata
            if abs(new_temp - prev_temp[0]) > 0.01:
                # Scala velocità basandosi sul cambio di temperatura
                temp_ratio = new_temp / prev_temp[0]
                for i in range(len(mob.velocities)):
                    mob.velocities[i] *= temp_ratio

                prev_temp[0] = new_temp
                mob.temperature = new_temp

                # Update particle colors
                new_color = mob._temperature_to_color()
                for particle in mob.particles:
                    particle.set_color(new_color)

        gas.add_updater(update_gas_temp)

        self.play(
            temp_tracker.animate.set_value(600),
            Create(pressure_curve),
            MoveAlongPath(dot, pressure_curve),
            run_time=4,
            rate_func=linear
        )

        gas.remove_updater(update_gas_temp)

        # Etichetta legge di Gay-Lussac
        gay_lussac_law = MathTex("\\frac{p}{T} = \\text{cost}", color=BLACK, font_size=32)
        gay_lussac_law.next_to(axes, DOWN, buff=0.4)
        self.play(Write(gay_lussac_law))

        self.wait(1)


class TrasformazioneIsobara(VerticalTemplate):
    """
    Trasformazione isobara: pressione costante (p = cost)
    Legge di Charles (o seconda legge di Volta): V/T = costante
    """
    def construct(self):
        # Setup standard vertical layout
        self.setup_vertical_layout(
            title_text="Trasformazione Isobara",
            subtitle_text="Pressione costante (p = cost)"
        )

        # === TOP BLOCK: Physical Animation (Piston with Weight) ===
        animation_center_y = self.top_block_center

        # Contenitore (cilindro) - centered in top block
        container_height = 3.5
        container_width = 2.5
        container_bottom = animation_center_y - container_height / 2
        container_top = animation_center_y + container_height / 2

        # Pareti del contenitore (linee spesse)
        container_left = Line(
            start=LEFT * (container_width/2) + UP * container_bottom,
            end=LEFT * (container_width/2) + UP * container_top,
            color=DARK_BLUE,
            stroke_width=6
        )
        container_right = Line(
            start=RIGHT * (container_width/2) + UP * container_bottom,
            end=RIGHT * (container_width/2) + UP * container_top,
            color=DARK_BLUE,
            stroke_width=6
        )
        container_bottom_line = Line(
            start=LEFT * (container_width/2) + UP * container_bottom,
            end=RIGHT * (container_width/2) + UP * container_bottom,
            color=DARK_BLUE,
            stroke_width=6
        )

        # Pistone (mobile) con peso sopra - inizia più basso
        piston_start_y = container_bottom + 1.8
        piston = Rectangle(
            height=0.15, width=container_width, color=GREEN_D, fill_opacity=1
        ).move_to(UP * piston_start_y)
        piston_rod = Rectangle(
            height=0.3, width=0.08, color=GREEN_D, fill_opacity=1
        ).next_to(piston, UP, buff=0)

        # Peso sopra il pistone (pressione costante)
        weight = Rectangle(
            height=0.3, width=0.6, color=DARK_GRAY, fill_opacity=1
        ).next_to(piston_rod, UP, buff=0)
        weight_label = Text("m", font_size=24, color=WHITE, weight=BOLD)
        weight_label.move_to(weight.get_center())

        piston_group = VGroup(piston, piston_rod, weight, weight_label)

        # Gas usando il modulo Gas - pressione costante, temperatura e volume variano
        gas_height_start = piston_start_y - container_bottom - 0.15
        gas_center_y_start = container_bottom + gas_height_start / 2
        gas_width = container_width - 0.24

        gas = Gas(
            width=gas_width,
            height=gas_height_start,
            temperature=300,  # Temperatura iniziale (bassa)
            num_particles=30,
            particle_scale=2.0,
            center=np.array([0, gas_center_y_start, 0])
        )

        # Etichetta pressione
        pressure_label = MathTex("p = \\text{cost}", color=GREEN_D, font_size=32)
        pressure_label.move_to(RIGHT * (container_width/2 + 0.8) + UP * animation_center_y)

        # === BOTTOM BLOCK: Chart (Volume vs Temperature) ===
        # Create axes (without animation yet)
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5.0,
            y_length=4.0,
            axis_config={"color": DARK_BLUE, "include_tip": True,
                        "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(UP * self.bottom_block_center)

        x_label = Text("T", font_size=28, color=DARK_BLUE).next_to(
            axes.x_axis, RIGHT, buff=0.1
        )
        y_label = Text("V", font_size=28, color=DARK_BLUE).next_to(
            axes.y_axis, UP, buff=0.1
        )

        # Indicatore di calore (fiamma sotto il contenitore)
        flame = Polygon(
            UP * container_bottom + DOWN * 0.08 + LEFT * 0.3,
            UP * container_bottom + DOWN * 0.08 + RIGHT * 0.3,
            UP * container_bottom + DOWN * 0.4,
            color=RED_D, fill_opacity=0.7, stroke_width=0
        )
        heat_label = Text("Calore", font_size=24, color=RED_D)
        heat_label.next_to(flame, DOWN, buff=0.15)

        # Disegna schema e assi insieme
        self.play(
            Create(container_left),
            Create(container_right),
            Create(container_bottom_line),
            Create(piston_group),
            FadeIn(gas),
            Write(pressure_label),
            Create(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait(0.5)

        # Aggiungi fiamma
        self.play(FadeIn(flame), Write(heat_label))

        # Animazione: riscaldamento, pistone sale, volume aumenta
        # Curva volume crescente (lineare con temperatura)
        volume_curve = axes.plot(
            lambda t: 1.5 + 0.6 * t,  # Andamento lineare
            x_range=[0, 4.5],
            color=GREEN_D,
            stroke_width=4
        )

        # Punto che traccia la curva
        dot = Dot(color=GREEN_D, radius=0.08).move_to(axes.c2p(0, 1.5))

        # Animazione simultanea: pistone sale, gas si espande e si riscalda
        piston_end_y = container_bottom + 3.2
        gas_height_end = piston_end_y - container_bottom - 0.15

        # Animazione che combina espansione del volume e aumento di temperatura
        def expand_and_heat_gas(mob, alpha):
            # Interpolazione altezza (volume)
            current_height = interpolate(gas_height_start, gas_height_end, alpha)
            new_center_y = container_bottom + current_height / 2

            # Resize the gas container
            mob.resize(gas_width, current_height)

            # Move gas center (shift all particles)
            shift_amount = new_center_y - mob._container_center[1]
            for particle in mob.particles:
                particle.shift(UP * shift_amount)
            mob._container_center = np.array([0, new_center_y, 0])

            # Interpolazione temperatura (300K → 600K)
            current_temp = interpolate(300, 600, alpha)
            mob.temperature = current_temp

            # Update particle colors
            interp_color = mob._temperature_to_color()
            for particle in mob.particles:
                particle.set_color(interp_color)

            # Rescale velocities based on temperature ratio (v ∝ T)
            velocity_scale = current_temp / 300
            base_speed = 0.15
            new_speed = base_speed * velocity_scale
            # Update velocities proportionally
            for i in range(len(mob.velocities)):
                current_speed = np.linalg.norm(mob.velocities[i][:2])
                if current_speed > 0:
                    mob.velocities[i] *= (new_speed / current_speed)

        self.play(
            piston_group.animate.move_to(UP * piston_end_y),
            UpdateFromAlphaFunc(gas, expand_and_heat_gas),
            Create(volume_curve),
            MoveAlongPath(dot, volume_curve),
            run_time=4,
            rate_func=linear
        )

        # Etichetta legge di Charles
        charles_law = MathTex("\\frac{V}{T} = \\text{cost}", color=BLACK, font_size=32)
        charles_law.next_to(axes, DOWN, buff=0.4)
        self.play(Write(charles_law))

        self.wait(1)


class LeggeDeiGasPerfetti(Scene):
    """
    Scena introduttiva che mostra la legge dei gas perfetti pV = nRT
    """
    def construct(self):
        # Sfondo bianco
        self.camera.background_color = WHITE

        # Titolo
        title = Text("Legge dei Gas Perfetti", font_size=44, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.5)

        self.play(Write(title))
        self.wait(0.5)

        # Equazione principale - componenti separati per animazioni individuali
        # Posizionata a metà distanza tra titolo e legenda
        equation = MathTex(
            "p", "V", "=", "n", "R", "T",
            font_size=96,
            color=DARK_BLUE
        )
        equation.move_to(UP * 2.4)

        self.play(Write(equation))
        self.wait(1)

        # Legenda delle variabili con animazioni sincronizzate
        legend_data = [
            ("p", "= pressione", RED_D, 0),      # indice 0 nell'equazione
            ("V", "= volume", GREEN_D, 1),       # indice 1
            ("n", "= numero di moli", BLUE_D, 3), # indice 3
            ("R", "= costante dei gas", DARK_GRAY, 4), # indice 4
            ("T", "= temperatura", RED_D, 5),    # indice 5
        ]

        # Crea tutti gli item della legenda
        legend_items = []
        for var, desc, color, eq_index in legend_data:
            var_text = MathTex(var, font_size=48, color=color)
            desc_text = Text(desc, font_size=36, color=BLACK)
            item = VGroup(var_text, desc_text).arrange(RIGHT, buff=0.3)
            legend_items.append((item, eq_index, color))

        # Organizza la legenda e centrala orizzontalmente
        legend = VGroup(*[item for item, _, _ in legend_items])
        legend.arrange(DOWN, buff=0.5)
        # Centra orizzontalmente (x=0) e posiziona verticalmente
        legend.move_to(ORIGIN)
        legend.shift(DOWN * 1.2)

        # Anima ogni item con la sua variabile corrispondente
        for item, eq_index, color in legend_items:
            # Anima: mostra la legenda E evidenzia la variabile nell'equazione
            self.play(
                Write(item),
                equation[eq_index].animate.scale(1.3).set_color(color),
                run_time=0.8
            )
            self.play(
                equation[eq_index].animate.scale(1/1.3).set_color(DARK_BLUE),
                run_time=0.5
            )
            self.wait(0.3)

        self.wait(1)

        # Sottotitolo finale
        subtitle = Text(
            "Valida per n costante",
            font_size=40,
            color=DARK_BLUE,
            slant=ITALIC
        )
        subtitle.to_edge(DOWN, buff=0.8)

        self.play(FadeIn(subtitle))
        self.wait(2)


class DerivazioneLeggeDeiGasPerfetti(Scene):
    """
    Derivazione della legge dei gas perfetti pV = nRT
    dalle tre leggi sperimentali (Boyle, Gay-Lussac, Charles)
    """
    def construct(self):
        # Sfondo bianco
        self.camera.background_color = WHITE

        # === TUTTO SU UNA SOLA SCHERMATA ===

        # Titolo (un po' più grande)
        title = Text("Come si ottiene pV = nRT?", font_size=36, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.15)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: Tre leggi sperimentali (un po' più grandi)
        step1_text = Text("Leggi sperimentali:", font_size=28, color=DARK_BLUE)
        step1_text.next_to(title, DOWN, buff=0.25)
        self.play(Write(step1_text))
        self.wait(0.3)

        boyle = MathTex("pV = k", color=RED_D, font_size=32)
        boyle_label = Text("(Boyle)", font_size=20, color=DARK_GRAY)
        boyle_group = VGroup(boyle, boyle_label).arrange(DOWN, buff=0.1)

        gay_lussac = MathTex("\\frac{p}{T} = k", color=RED_D, font_size=32)
        gay_lussac_label = Text("(Gay-Lussac)", font_size=20, color=DARK_GRAY)
        gay_lussac_group = VGroup(gay_lussac, gay_lussac_label).arrange(DOWN, buff=0.1)

        charles = MathTex("\\frac{V}{T} = k", color=RED_D, font_size=32)
        charles_label = Text("(Charles)", font_size=20, color=DARK_GRAY)
        charles_group = VGroup(charles, charles_label).arrange(DOWN, buff=0.1)

        laws = VGroup(boyle_group, gay_lussac_group, charles_group)
        laws.arrange(RIGHT, buff=0.6)
        laws.next_to(step1_text, DOWN, buff=0.2)

        self.play(Write(laws))
        self.wait(0.5)

        # Step 2: Mostra le deduzioni (frecce sotto ogni legge)
        arrow1 = MathTex("\\downarrow", color=DARK_GRAY, font_size=26)
        arrow1.next_to(boyle_group, DOWN, buff=0.1)
        arrow2 = MathTex("\\downarrow", color=DARK_GRAY, font_size=26)
        arrow2.next_to(gay_lussac_group, DOWN, buff=0.1)
        arrow3 = MathTex("\\downarrow", color=DARK_GRAY, font_size=26)
        arrow3.next_to(charles_group, DOWN, buff=0.1)

        # Riscritture delle leggi (più grandi)
        boyle_rewrite = MathTex("V = \\frac{k}{p}", color=RED_D, font_size=28)
        boyle_rewrite.next_to(arrow1, DOWN, buff=0.1)

        gay_lussac_rewrite = MathTex("p = kT", color=RED_D, font_size=28)
        gay_lussac_rewrite.next_to(arrow2, DOWN, buff=0.1)

        charles_rewrite = MathTex("V = kT", color=RED_D, font_size=28)
        charles_rewrite.next_to(arrow3, DOWN, buff=0.1)

        self.play(
            Write(arrow1), Write(boyle_rewrite),
            Write(arrow2), Write(gay_lussac_rewrite),
            Write(arrow3), Write(charles_rewrite)
        )
        self.wait(0.8)

        # Step 3: Proporzionalità derivate (centrate)
        step2_text = Text("Proporzionalità:", font_size=24, color=DARK_BLUE)
        step2_text.next_to(charles_rewrite, DOWN, buff=0.35)
        step2_text.shift(LEFT * step2_text.get_center()[0])  # Centra orizzontalmente
        self.play(Write(step2_text))
        self.wait(0.3)

        prop1 = MathTex("V \\propto \\frac{1}{p}", color=BLUE_D, font_size=30)
        prop2 = MathTex("p \\propto T", color=BLUE_D, font_size=30)
        prop3 = MathTex("V \\propto T", color=BLUE_D, font_size=30)

        props = VGroup(prop1, prop2, prop3)
        props.arrange(RIGHT, buff=0.5)
        props.next_to(step2_text, DOWN, buff=0.2)
        props.shift(LEFT * props.get_center()[0])  # Centra orizzontalmente

        self.play(
            TransformFromCopy(boyle_rewrite, prop1),
            TransformFromCopy(gay_lussac_rewrite, prop2),
            TransformFromCopy(charles_rewrite, prop3)
        )
        self.wait(0.8)

        # Step 4: Aggiungi V ∝ n (centrato)
        plus_n = Text("+ più moli → più volume:", font_size=22, color=DARK_BLUE)
        plus_n.next_to(props, DOWN, buff=0.25)
        plus_n.shift(LEFT * plus_n.get_center()[0])  # Centra orizzontalmente

        prop_n = MathTex("V \\propto n", color=BLUE_D, font_size=30)
        prop_n.next_to(plus_n, DOWN, buff=0.15)
        prop_n.shift(LEFT * prop_n.get_center()[0])  # Centra orizzontalmente

        self.play(Write(plus_n), Write(prop_n))
        self.wait(0.8)

        # Step 5: Combinazione (centrata)
        arrow = MathTex("\\Downarrow", color=GREEN_D, font_size=36)
        arrow.next_to(prop_n, DOWN, buff=0.25)
        arrow.shift(LEFT * arrow.get_center()[0])  # Centra orizzontalmente

        combined = MathTex("V \\propto \\frac{nT}{p}", color=GREEN_D, font_size=38)
        combined.next_to(arrow, DOWN, buff=0.2)
        combined.shift(LEFT * combined.get_center()[0])  # Centra orizzontalmente

        self.play(Write(arrow))
        self.wait(0.3)
        self.play(Write(combined))
        self.wait(0.8)

        # Step 6: Costante R (centrata)
        explanation = Text("La costante è R:", font_size=24, color=DARK_BLUE)
        explanation.next_to(combined, DOWN, buff=0.35)
        explanation.shift(LEFT * explanation.get_center()[0])  # Centra orizzontalmente
        self.play(Write(explanation))
        self.wait(0.3)

        equation_step1 = MathTex("V = R \\frac{nT}{p}", color=BLACK, font_size=36)
        equation_step1.next_to(explanation, DOWN, buff=0.2)
        equation_step1.shift(LEFT * equation_step1.get_center()[0])  # Centra orizzontalmente
        self.play(Write(equation_step1))
        self.wait(0.5)

        # Step 7: Moltiplica per p (centrato)
        multiply_text = Text("Moltiplichiamo per p:", font_size=24, color=RED_D)
        multiply_text.next_to(equation_step1, DOWN, buff=0.3)
        multiply_text.shift(LEFT * multiply_text.get_center()[0])  # Centra orizzontalmente
        self.play(Write(multiply_text))
        self.wait(0.3)

        # Step 8: Equazione finale (centrata)
        final_equation = MathTex("pV = nRT", color=RED_D, font_size=56)
        final_equation.next_to(multiply_text, DOWN, buff=0.3)
        final_equation.shift(LEFT * final_equation.get_center()[0])  # Centra orizzontalmente
        self.play(Write(final_equation))
        self.wait(0.5)

        box = SurroundingRectangle(final_equation, color=RED_D, buff=0.25, stroke_width=4)
        self.play(Create(box))
        self.wait(0.8)

        # Step 9: Conclusione (centrata)
        conclusion = Text(
            "Legge universale dei gas perfetti",
            font_size=30,
            color=DARK_BLUE,
            slant=ITALIC
        )
        conclusion.next_to(box, DOWN, buff=0.3)
        conclusion.shift(LEFT * conclusion.get_center()[0])  # Centra orizzontalmente

        r_definition = Text(
            "R = 8.314 J/(mol·K)",
            font_size=26,
            color=DARK_GRAY
        )
        r_definition.next_to(conclusion, DOWN, buff=0.2)
        r_definition.shift(LEFT * r_definition.get_center()[0])  # Centra orizzontalmente

        self.play(Write(conclusion))
        self.wait(0.3)
        self.play(Write(r_definition))
        self.wait(2)

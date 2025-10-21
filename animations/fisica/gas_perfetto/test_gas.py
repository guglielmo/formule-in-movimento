"""
Test animation for the Gas module
"""

from manim import *
import sys
sys.path.insert(0, '/home/gu/projects/formule-in-movimento')
from animations.gas_module import Gas


class TestGasAnimation(Scene):
    """
    Simple test animation showing the Gas module in action
    """
    def construct(self):
        # White background
        self.camera.background_color = WHITE

        # Title
        title = Text("Test Gas Module", font_size=48, color=BLACK, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create container
        container_width = 3
        container_height = 4
        container = Rectangle(
            width=container_width,
            height=container_height,
            color=DARK_BLUE,
            stroke_width=6
        )

        self.play(Create(container))
        self.wait(0.5)

        # Create gas at room temperature (300K) with 30 particles filling the ENTIRE volume
        gas = Gas(
            width=container_width,  # Match container exactly, no margin
            height=container_height,  # Match container exactly, no margin
            temperature=300,
            num_particles=30,
            particle_scale=2.0,  # Slightly larger for visibility
            center=ORIGIN
        )

        temp_label = MathTex("T = 300K", color=BLUE_D, font_size=36)
        temp_label.next_to(container, DOWN, buff=0.5)

        self.play(
            FadeIn(gas),
            Write(temp_label)
        )
        self.wait(2)

        # Heat the gas
        new_temp_label = MathTex("T = 600K", color=RED_D, font_size=36)
        new_temp_label.next_to(container, DOWN, buff=0.5)

        self.play(
            gas.animate_temperature(600, run_time=3),
            Transform(temp_label, new_temp_label),
            run_time=3
        )
        self.wait(2)

        # Cool down
        cool_temp_label = MathTex("T = 250K", color=BLUE_E, font_size=36)
        cool_temp_label.next_to(container, DOWN, buff=0.5)

        self.play(
            gas.animate_temperature(250, run_time=3),
            Transform(temp_label, cool_temp_label),
            run_time=3
        )
        self.wait(2)

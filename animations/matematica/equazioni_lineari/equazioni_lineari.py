from manim import *

class RiconoscereEquazioniLineari(Scene):
    """Scene showing how to recognize linear equations."""

    def construct(self):
        # Light background theme
        self.camera.background_color = WHITE

        # Title - positioned at the top with minimal margin
        title = Text("Riconoscere Equazioni Lineari", font_size=30, color=BLACK, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        self.play(Write(title))
        self.wait()

        # Show general form first - positioned below the title with less spacing
        form_intro = VGroup(
            Text("Forma generale di un'equazione lineare:", font_size=26, color=DARK_BLUE),
            MathTex("ax + b = c", color=BLACK, font_size=48),
            Text("dove a ≠ 0", font_size=24, color=DARK_GRAY, slant=ITALIC)
        ).arrange(DOWN, buff=0.4)
        form_intro.next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(form_intro, shift=UP*0.3))
        self.wait(3)  # Wait 3 seconds for info to sink in

        # Store the position where form_intro starts (for placing linear block)
        form_intro_top = form_intro.get_top()

        # Fade out the form
        self.play(FadeOut(form_intro))
        self.wait(0.5)

        # LINEAR BLOCK - should start at the same level as form_intro
        linear_header = Text("Lineari ✓", font_size=30, color=GREEN_D, weight=BOLD)

        # Linear equations - smaller font sizes
        linear_eqs = VGroup(
            MathTex("2x + 3 = 7", color=GREEN_D, font_size=48),
            MathTex("5x - 4 = 2x + 8", color=GREEN_D, font_size=48),
            MathTex("\\frac{x}{3} + 5 = 9", color=GREEN_D, font_size=48),
            MathTex("-3x = 12", color=GREEN_D, font_size=48)
        ).arrange(DOWN, buff=0.35)

        # Create linear block group and position it where form_intro was
        linear_block = VGroup(linear_header, linear_eqs).arrange(DOWN, buff=0.5)
        linear_block.move_to(form_intro_top - UP / 2, aligned_edge=UP)

        # Show linear header and equations
        self.play(FadeIn(linear_header, shift=DOWN*0.3))
        self.wait(0.3)

        # Animate linear equations appearing one by one
        for linear_eq in linear_eqs:
            self.play(FadeIn(linear_eq, shift=DOWN*0.3))
            self.wait(0.4)

        # Wait to let info sink in
        self.wait(1)

        # NON-LINEAR BLOCK - positioned below the linear block with spacing
        nonlinear_header = Text("NON Lineari ✗", font_size=30, color=RED_D, weight=BOLD)

        # Non-linear equations - smaller font sizes
        nonlinear_eqs = VGroup(
            MathTex("x^2 + 3 = 7", color=RED_D, font_size=48),
            MathTex("\\sqrt{x} = 4", color=RED_D, font_size=48),
            MathTex("\\frac{1}{x} = 2", color=RED_D, font_size=48),
            MathTex("x^3 - 2x = 5", color=RED_D, font_size=48)
        ).arrange(DOWN, buff=0.35)

        # Create non-linear block group and position below linear block
        nonlinear_block = VGroup(nonlinear_header, nonlinear_eqs).arrange(DOWN, buff=0.5)
        # Position it below the linear block with proper spacing (1.0 unit of space)
        nonlinear_block.next_to(linear_block, DOWN, buff=2.0)

        # Show non-linear header and equations
        self.play(FadeIn(nonlinear_header, shift=DOWN*0.3))
        self.wait(0.3)

        # Animate non-linear equations appearing one by one
        for nonlinear_eq in nonlinear_eqs:
            self.play(FadeIn(nonlinear_eq, shift=DOWN*0.3))
            self.wait(0.4)

        self.wait(1)

        # Add boxes around each block
        linear_box = SurroundingRectangle(
            linear_block,
            color=GREEN_D,
            buff=0.3,
            corner_radius=0.1,
            stroke_width=4
        )
        nonlinear_box = SurroundingRectangle(
            nonlinear_block,
            color=RED_D,
            buff=0.3,
            corner_radius=0.1,
            stroke_width=4
        )

        self.play(
            Create(linear_box),
            Create(nonlinear_box)
        )
        self.wait(2)

        # End with boxes visible
        self.wait(2)


class SemplificareEspressioni(Scene):
    """Scene showing simplification of linear expressions."""

    def construct(self):
        # Light background theme
        self.camera.background_color = WHITE

        # Title
        title = Text("Semplificare Espressioni", font_size=44, color=BLACK)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait()

        # Example 1: Combining like terms
        subtitle = Text("Raccogliere i termini simili", font_size=32, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Original expression
        expr = MathTex("3x", "+", "5", "+", "2x", "-", "3", color=BLACK, font_size=64)
        expr.move_to(ORIGIN)
        self.play(Write(expr))
        self.wait()

        # Highlight like terms one by one
        # First x term (3x)
        box_3x = SurroundingRectangle(expr[0], color=BLUE_D, buff=0.15)
        self.play(Create(box_3x))
        self.wait(0.5)

        # Second x term (2x)
        box_2x = SurroundingRectangle(expr[4], color=BLUE_D, buff=0.15)
        self.play(Create(box_2x))
        self.wait(0.5)

        # First constant term (5)
        box_5 = SurroundingRectangle(expr[2], color=RED_D, buff=0.15)
        self.play(Create(box_5))
        self.wait(0.5)

        # Second constant term (-3)
        box_3 = SurroundingRectangle(expr[6], color=RED_D, buff=0.15)
        self.play(Create(box_3))
        self.wait(1)

        # Transform: regroup terms (x terms together, constants together)
        # Keep boxes visible and move them with the terms
        expr_regroup = MathTex("3x", "+", "2x", "+", "5", "-", "3", color=BLACK, font_size=64)
        expr_regroup.move_to(ORIGIN)

        # Create merged rectangles for regrouped expression
        # One rectangle around both x terms (3x + 2x)
        box_x_merged = SurroundingRectangle(
            VGroup(expr_regroup[0], expr_regroup[1], expr_regroup[2]),
            color=BLUE_D,
            buff=0.15
        )
        # One rectangle around both constant terms (5 - 3)
        box_const_merged = SurroundingRectangle(
            VGroup(expr_regroup[4], expr_regroup[5], expr_regroup[6]),
            color=RED_D,
            buff=0.15
        )

        self.play(
            TransformMatchingTex(expr, expr_regroup),
            ReplacementTransform(VGroup(box_3x, box_2x), box_x_merged),
            ReplacementTransform(VGroup(box_5, box_3), box_const_merged)
        )
        self.wait(1)

        # Transform to simplified form
        expr_simp = MathTex("5x", "+", "2", color=BLACK, font_size=64)
        expr_simp.move_to(ORIGIN)

        # Create boxes for the simplified terms
        box_5x = SurroundingRectangle(expr_simp[0], color=BLUE_D, buff=0.15)
        box_2 = SurroundingRectangle(expr_simp[2], color=RED_D, buff=0.15)

        # Transform the rectangles to fit the simplified terms
        self.play(
            TransformMatchingTex(expr_regroup, expr_simp),
            Transform(box_x_merged, box_5x),
            Transform(box_const_merged, box_2)
        )
        self.wait(1.5)

        # Fade out boxes
        self.play(FadeOut(box_x_merged), FadeOut(box_const_merged))
        self.wait(0.5)

        # Example 2: Distributive property
        self.play(FadeOut(expr_simp))

        subtitle2 = Text("Proprietà distributiva", font_size=32, color=DARK_BLUE)
        subtitle2.next_to(title, DOWN, buff=0.5)
        self.play(Transform(subtitle, subtitle2))

        # Expression with parentheses
        expr2 = MathTex("3", "(", "2x", "-", "4", ")", "+", "5", color=BLACK, font_size=64)
        expr2.move_to(ORIGIN)
        self.play(Write(expr2))
        self.wait()

        # Highlight the multiplication
        highlight = SurroundingRectangle(
            VGroup(expr2[0], expr2[1], expr2[2], expr2[3], expr2[4], expr2[5]),
            color=BLUE_D,
            buff=0.15
        )
        self.play(Create(highlight))
        self.wait()

        # Transform to intermediate form showing the multiplication explicitly
        expr2_mult = MathTex("3", "\\cdot", "2x", "-", "3", "\\cdot", "4", "+", "5", color=BLACK, font_size=64)
        expr2_mult.move_to(ORIGIN)

        # Create rectangle around the intermediate multiplication terms (3·2x - 3·4)
        highlight_mult = SurroundingRectangle(
            VGroup(expr2_mult[0], expr2_mult[1], expr2_mult[2], expr2_mult[3], expr2_mult[4], expr2_mult[5], expr2_mult[6]),
            color=BLUE_D,
            buff=0.15
        )

        self.play(
            TransformMatchingTex(expr2, expr2_mult),
            Transform(highlight, highlight_mult)
        )
        self.wait(1.5)

        # Transform to distributed form with calculated products
        expr2_dist = MathTex("6x", "-", "12", "+", "5", color=BLACK, font_size=64)
        expr2_dist.move_to(ORIGIN)

        # Create rectangle around the distributed terms (6x - 12)
        highlight_dist = SurroundingRectangle(
            VGroup(expr2_dist[0], expr2_dist[1], expr2_dist[2]),
            color=BLUE_D,
            buff=0.15
        )

        self.play(
            TransformMatchingTex(expr2_mult, expr2_dist),
            Transform(highlight, highlight_dist)
        )
        self.wait(1.5)

        # Transform to final simplified form
        expr2_final = MathTex("6x", "-", "7", color=BLACK, font_size=64)
        expr2_final.move_to(ORIGIN)

        self.play(
            TransformMatchingTex(expr2_dist, expr2_final),
            FadeOut(highlight)
        )
        self.wait(2)


class RisolvereEquazione(Scene):
    """Scene showing step-by-step solution of a linear equation."""

    def construct(self):
        # Light background theme
        self.camera.background_color = WHITE

        # Title
        title = Text("Risolvere un'Equazione Lineare", font_size=44, color=BLACK)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait()

        # Step 1: Original equation
        eq1 = MathTex("3x", "+", "5", "=", "2x", "+", "11", color=BLACK, font_size=64)
        eq1.move_to(ORIGIN)
        self.play(Write(eq1))
        self.wait(1)

        # Step 2: Highlight 2x in blue
        step_text = Text("Sottrarre 2x da entrambi i lati", font_size=28, color=DARK_GRAY)
        step_text.next_to(eq1, DOWN, buff=0.8)
        self.play(FadeIn(step_text))

        box_2x = SurroundingRectangle(eq1[4], color=BLUE_D, buff=0.15)
        self.play(Create(box_2x))
        self.wait(1)

        # Step 3: Show subtraction on both sides
        eq2 = MathTex("3x", "-", "2x", "+", "5", "=", "2x", "-", "2x", "+", "11", color=BLACK, font_size=64)
        eq2.move_to(ORIGIN)

        box_left = SurroundingRectangle(eq2[2], color=BLUE_D, buff=0.15)
        box_right = SurroundingRectangle(VGroup(eq2[6], eq2[7], eq2[8]), color=BLUE_D, buff=0.15)

        self.play(
            TransformMatchingTex(eq1, eq2),
            ReplacementTransform(box_2x, VGroup(box_left, box_right))
        )
        self.wait(1)

        # Step 4: Simplify (2x - 2x cancels on right) - strikethrough effect
        step_text2 = Text("Semplificare", font_size=28, color=DARK_GRAY)
        step_text2.next_to(eq2, DOWN, buff=0.8)

        self.play(Transform(step_text, step_text2))
        self.wait(0.5)

        # Draw diagonal lines through the cancelling terms
        cancel_terms = VGroup(eq2[6], eq2[7], eq2[8])
        strikethrough = Line(
            cancel_terms.get_corner(DL) + LEFT * 0.1,
            cancel_terms.get_corner(UR) + RIGHT * 0.1,
            color=RED_D,
            stroke_width=4
        )

        self.play(Create(strikethrough))
        self.wait(0.8)

        # First: Fade out the strikethrough and cancelled terms
        self.play(
            FadeOut(strikethrough),
            FadeOut(cancel_terms)
        )
        self.wait(0.3)

        # Second: Fade out the boxes
        self.play(
            FadeOut(box_right),
            FadeOut(box_left)
        )
        self.wait(0.3)

        # Third: Fade out old equation and fade in simplified equation
        eq3 = MathTex("3x", "-", "2x", "+", "5", "=", "11", color=BLACK, font_size=64)
        eq3.move_to(ORIGIN)

        self.play(
            FadeOut(eq2),
            FadeIn(eq3)
        )
        self.wait(1)

        # Step 5: Combine like terms
        eq4 = MathTex("x", "+", "5", "=", "11", color=BLACK, font_size=64)
        eq4.move_to(ORIGIN)

        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1)

        # Step 6: Highlight 5 in blue
        step_text3 = Text("Sottrarre 5 da entrambi i lati", font_size=28, color=DARK_GRAY)
        step_text3.next_to(eq4, DOWN, buff=0.8)

        self.play(Transform(step_text, step_text3))

        box_5 = SurroundingRectangle(eq4[2], color=BLUE_D, buff=0.15)
        self.play(Create(box_5))
        self.wait(1)

        # Step 7: Show subtraction on both sides
        eq5 = MathTex("x", "+", "5", "-", "5", "=", "11", "-", "5", color=BLACK, font_size=64)
        eq5.move_to(ORIGIN)

        box_left2 = SurroundingRectangle(VGroup(eq5[2], eq5[3], eq5[4]), color=BLUE_D, buff=0.15)
        box_right2 = SurroundingRectangle(eq5[8], color=BLUE_D, buff=0.15)

        self.play(
            TransformMatchingTex(eq4, eq5),
            ReplacementTransform(box_5, VGroup(box_left2, box_right2))
        )
        self.wait(1)

        # Step 8: Simplify (5 - 5 cancels on left) - strikethrough effect
        step_text4 = Text("Calcolare", font_size=28, color=DARK_GRAY)
        step_text4.next_to(eq5, DOWN, buff=0.8)

        self.play(Transform(step_text, step_text4))
        self.wait(0.5)

        # Draw diagonal lines through the cancelling terms
        cancel_terms2 = VGroup(eq5[2], eq5[3], eq5[4])
        strikethrough2 = Line(
            cancel_terms2.get_corner(DL) + LEFT * 0.1,
            cancel_terms2.get_corner(UR) + RIGHT * 0.1,
            color=RED_D,
            stroke_width=4
        )

        self.play(Create(strikethrough2))
        self.wait(0.8)

        # First: Fade out the strikethrough and cancelled terms
        self.play(
            FadeOut(strikethrough2),
            FadeOut(cancel_terms2)
        )
        self.wait(0.3)

        # Second: Fade out the boxes
        self.play(
            FadeOut(box_left2),
            FadeOut(box_right2)
        )
        self.wait(0.3)

        # Third: Fade out old equation and fade in simplified equation
        eq6 = MathTex("x", "=", "11", "-", "5", color=BLACK, font_size=64)
        eq6.move_to(ORIGIN)

        self.play(
            FadeOut(eq5),
            FadeIn(eq6)
        )
        self.wait(1)

        # Step 9: Calculate final answer
        eq7 = MathTex("x", "=", "6", color=BLACK, font_size=64)
        eq7.move_to(ORIGIN)

        self.play(TransformMatchingTex(eq6, eq7))
        self.wait(0.5)

        # Step 10: Highlight solution in green
        eq8 = MathTex("x", "=", "6", color=GREEN_D, font_size=80)
        eq8.move_to(ORIGIN)

        self.play(
            TransformMatchingTex(eq7, eq8),
            FadeOut(step_text)
        )

        # Box around solution
        solution_box = SurroundingRectangle(eq8, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(solution_box))

        # Solution label
        solution_label = Text("Soluzione!", font_size=36, color=GREEN_D, weight=BOLD)
        solution_label.next_to(solution_box, DOWN, buff=0.8)
        self.play(FadeIn(solution_label, shift=UP*0.3))
        self.wait(2)


class VerificareSoluzione(Scene):
    """Scene showing how to verify a solution."""

    def construct(self):
        # Light background theme
        self.camera.background_color = WHITE

        # Title
        title = Text("Verificare la Soluzione", font_size=44, color=BLACK)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait()

        # Subtitle
        subtitle = Text("Sostituire x = 6", font_size=32, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Show solution
        solution_box = VGroup(
            Text("x = 6", font_size=36, color=GREEN_D, weight=BOLD)
        )
        solution_box.to_corner(UR, buff=0.8)
        box = SurroundingRectangle(solution_box, color=GREEN_D, buff=0.3)
        self.play(FadeIn(solution_box), Create(box))

        # Original equation
        eq = MathTex("3x", "+", "5", "=", "2x", "+", "11", color=BLACK, font_size=64)
        eq.move_to(ORIGIN)
        self.play(Write(eq))
        self.wait(1)

        # Substitute x = 6
        step_text = Text("Sostituire x con 6", font_size=24, color=DARK_GRAY)
        step_text.next_to(subtitle, DOWN, buff=0.3)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        eq_sub = MathTex("3", "\\cdot", "6", "+", "5", "=", "2", "\\cdot", "6", "+", "11",
                        color=BLACK, font_size=64)
        eq_sub.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq, eq_sub))
        self.wait(1)

        # Calculate left side
        step_text2 = Text("Calcolare entrambi i lati", font_size=24, color=DARK_GRAY)
        step_text2.move_to(step_text)
        self.play(Transform(step_text, step_text2))
        self.wait(0.5)

        eq_calc = MathTex("18", "+", "5", "=", "12", "+", "11",
                         color=BLACK, font_size=64)
        eq_calc.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq_sub, eq_calc))
        self.wait(1)

        # Final result
        step_text3 = Text("Semplificare", font_size=24, color=DARK_GRAY)
        step_text3.move_to(step_text)
        self.play(Transform(step_text, step_text3))
        self.wait(0.5)

        eq_result = MathTex("23", "=", "23", color=GREEN_D, font_size=80)
        eq_result.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq_calc, eq_result))
        self.play(FadeOut(step_text))

        # Checkmark
        check = Text("✓", font_size=120, color=GREEN_D)
        check.next_to(eq_result, RIGHT, buff=0.5)
        self.play(FadeIn(check, scale=0.5))

        # Verification message
        verify_msg = Text("La soluzione è corretta!", font_size=36, color=GREEN_D, weight=BOLD)
        verify_msg.next_to(eq_result, DOWN, buff=0.8)
        self.play(FadeIn(verify_msg, shift=UP*0.3))
        self.wait(2)


class EquazioniComplesse(Scene):
    """Scene showing a more complex linear equation."""

    def construct(self):
        # Light background theme
        self.camera.background_color = WHITE

        # Title
        title = Text("Equazione Più Complessa", font_size=44, color=BLACK)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait()

        # Subtitle
        subtitle = Text("Con parentesi e proprietà distributiva", font_size=28, color=DARK_BLUE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Original equation
        eq = MathTex("2", "(", "x", "+", "3", ")", "=", "4x", "-", "2",
                    color=BLACK, font_size=60)
        eq.move_to(ORIGIN)
        self.play(Write(eq))
        self.wait(1.5)

        # Step indicator
        step_text = Text("Applicare proprietà distributiva", font_size=24, color=DARK_GRAY)
        step_text.next_to(subtitle, DOWN, buff=0.3)
        self.play(FadeIn(step_text))
        self.wait(0.5)

        # Distribute
        eq2 = MathTex("2x", "+", "6", "=", "4x", "-", "2",
                     color=BLACK, font_size=60)
        eq2.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq, eq2))
        self.wait(1)

        # Subtract 4x
        step_text2 = Text("Sottrarre 4x da entrambi i lati", font_size=24, color=DARK_GRAY)
        step_text2.move_to(step_text)
        self.play(Transform(step_text, step_text2))
        self.wait(0.5)

        eq3 = MathTex("2x", "-", "4x", "+", "6", "=", "-2",
                     color=BLACK, font_size=60)
        eq3.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1)

        # Simplify
        step_text3 = Text("Semplificare", font_size=24, color=DARK_GRAY)
        step_text3.move_to(step_text)
        self.play(Transform(step_text, step_text3))
        self.wait(0.5)

        eq4 = MathTex("-2x", "+", "6", "=", "-2",
                     color=BLACK, font_size=60)
        eq4.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1)

        # Subtract 6
        step_text4 = Text("Sottrarre 6 da entrambi i lati", font_size=24, color=DARK_GRAY)
        step_text4.move_to(step_text)
        self.play(Transform(step_text, step_text4))
        self.wait(0.5)

        eq5 = MathTex("-2x", "=", "-2", "-", "6",
                     color=BLACK, font_size=60)
        eq5.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(1)

        # Simplify right side
        step_text5 = Text("Semplificare lato destro", font_size=24, color=DARK_GRAY)
        step_text5.move_to(step_text)
        self.play(Transform(step_text, step_text5))
        self.wait(0.5)

        eq6 = MathTex("-2x", "=", "-8",
                     color=BLACK, font_size=60)
        eq6.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq5, eq6))
        self.wait(1)

        # Divide by -2
        step_text6 = Text("Dividere entrambi i lati per -2", font_size=24, color=DARK_GRAY)
        step_text6.move_to(step_text)
        self.play(Transform(step_text, step_text6))
        self.wait(0.5)

        eq7 = MathTex("x", "=", "\\frac{-8}{-2}",
                     color=BLACK, font_size=60)
        eq7.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq6, eq7))
        self.wait(1)

        # Final answer
        step_text7 = Text("Semplificare", font_size=24, color=DARK_GRAY)
        step_text7.move_to(step_text)
        self.play(Transform(step_text, step_text7))
        self.wait(0.5)

        eq8 = MathTex("x", "=", "4", color=GREEN_D, font_size=80)
        eq8.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq7, eq8))
        self.play(FadeOut(step_text))

        # Box around solution
        solution_box = SurroundingRectangle(eq8, color=GREEN_D, buff=0.4, corner_radius=0.2, stroke_width=6)
        self.play(Create(solution_box))

        # Solution label
        solution_label = Text("Soluzione!", font_size=36, color=GREEN_D, weight=BOLD)
        solution_label.next_to(solution_box, DOWN, buff=0.8)
        self.play(FadeIn(solution_label, shift=UP*0.3))
        self.wait(2)

"""
Vertical Video Template for Formule in Movimento
=================================================

This template provides a standard layout for vertical (9:16) educational animations:
- Top 10%: Title and subtitle
- Content 85%: Split into two blocks (top and bottom)
- Bottom 5%: Empty margin

Layout coordinates (frame_height = 14.22):
- Top edge: +7.11
- Title area: +7.11 to +5.7
- Top separator: +5.7
- Top content block: +5.7 to -0.35 (center at +2.675)
- Middle separator: -0.35
- Bottom content block: -0.35 to -6.4 (center at -3.375)
- Bottom margin: -6.4 to -7.11
- Bottom edge: -7.11

Usage:
    from animations.vertical_template import VerticalTemplate

    class MyAnimation(VerticalTemplate):
        def construct(self):
            self.setup_vertical_layout("Title", "Subtitle")
            # Add your content here using:
            # - self.top_block_center (y = 2.675)
            # - self.bottom_block_center (y = -3.375)
"""

from manim import *


class VerticalTemplate(Scene):
    """
    Base template for vertical 9:16 animations with title and two content blocks.

    This template is configured in manim.cfg with:
        frame_width = 8.0
        frame_height = 14.22
    """

    # Layout constants
    FRAME_WIDTH = 8.0
    FRAME_HEIGHT = 14.22

    # Vertical positions
    TOP_SEPARATOR_Y = 5.7
    MIDDLE_SEPARATOR_Y = -0.35
    BOTTOM_MARGIN_Y = -6.4

    # Block centers
    TOP_BLOCK_CENTER = 2.675  # Midpoint between +5.7 and -0.35
    BOTTOM_BLOCK_CENTER = -3.375  # Midpoint between -0.35 and -6.4

    # Recommended content sizes
    RECOMMENDED_CONTAINER_HEIGHT = 3.5
    RECOMMENDED_CHART_WIDTH = 5.0
    RECOMMENDED_CHART_HEIGHT = 4.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_block_center = self.TOP_BLOCK_CENTER
        self.bottom_block_center = self.BOTTOM_BLOCK_CENTER

    def setup_vertical_layout(self, title_text, subtitle_text,
                            title_color=BLACK, subtitle_color=DARK_BLUE,
                            background_color=WHITE):
        """
        Set up the standard vertical layout with title and two content blocks.

        Args:
            title_text: Main title text
            subtitle_text: Subtitle text
            title_color: Color for the title (default: BLACK)
            subtitle_color: Color for the subtitle (default: DARK_BLUE)
            background_color: Background color (default: WHITE)
        """
        # Set background
        self.camera.background_color = background_color

        # === TOP 10%: TITLE AND SUBTITLE ===
        title = Text(title_text, font_size=38, color=title_color, weight=BOLD)
        title.to_edge(UP, buff=0.1)
        subtitle = Text(subtitle_text, font_size=28, color=subtitle_color)
        subtitle.next_to(title, DOWN, buff=0.15)

        # Separator lines
        separator_top = Line(
            LEFT * 4 + UP * self.TOP_SEPARATOR_Y,
            RIGHT * 4 + UP * self.TOP_SEPARATOR_Y,
            color=DARK_GRAY,
            stroke_width=2
        )
        separator_middle = Line(
            LEFT * 4 + UP * self.MIDDLE_SEPARATOR_Y,
            RIGHT * 4 + UP * self.MIDDLE_SEPARATOR_Y,
            color=DARK_GRAY,
            stroke_width=2
        )

        # Draw title, subtitle, and both separators together
        self.play(
            Write(title),
            Write(subtitle),
            Create(separator_top),
            Create(separator_middle)
        )
        self.wait(0.5)

        # Store references for later use
        self.title = title
        self.subtitle = subtitle
        self.separator_top = separator_top
        self.separator_middle = separator_middle

    def create_chart(self, x_label_text, y_label_text,
                    x_range=[0, 5, 1], y_range=[0, 5, 1],
                    chart_width=None, chart_height=None):
        """
        Create a chart/graph in the bottom block.

        Args:
            x_label_text: Label for x-axis
            y_label_text: Label for y-axis
            x_range: Range for x-axis [min, max, step]
            y_range: Range for y-axis [min, max, step]
            chart_width: Width of chart (default: RECOMMENDED_CHART_WIDTH)
            chart_height: Height of chart (default: RECOMMENDED_CHART_HEIGHT)

        Returns:
            Tuple of (axes, x_label, y_label)
        """
        if chart_width is None:
            chart_width = self.RECOMMENDED_CHART_WIDTH
        if chart_height is None:
            chart_height = self.RECOMMENDED_CHART_HEIGHT

        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=chart_width,
            y_length=chart_height,
            axis_config={"color": DARK_BLUE, "include_tip": True,
                        "tip_width": 0.15, "tip_height": 0.15},
        ).move_to(UP * self.bottom_block_center)

        x_label = Text(x_label_text, font_size=28, color=DARK_BLUE).next_to(
            axes.x_axis, RIGHT, buff=0.1
        )
        y_label = Text(y_label_text, font_size=28, color=DARK_BLUE).next_to(
            axes.y_axis, UP, buff=0.1
        )

        self.play(Create(axes), Write(x_label), Write(y_label))

        return axes, x_label, y_label


# Example usage demonstration
class ExampleVerticalAnimation(VerticalTemplate):
    """
    Example showing how to use the vertical template.
    """
    def construct(self):
        # Setup the standard layout
        self.setup_vertical_layout(
            title_text="Example Title",
            subtitle_text="This is a subtitle"
        )

        # TOP BLOCK: Add content centered at self.top_block_center
        example_text_top = Text(
            "Top Block Content",
            font_size=32,
            color=BLACK
        ).move_to(UP * self.top_block_center)
        self.play(Write(example_text_top))
        self.wait(1)

        # BOTTOM BLOCK: Create a chart
        axes, x_label, y_label = self.create_chart(
            x_label_text="x",
            y_label_text="y"
        )

        # Add a curve to the chart
        curve = axes.plot(
            lambda x: 3 * np.exp(-0.5 * x),
            x_range=[0, 4.5],
            color=RED_D,
            stroke_width=4
        )
        self.play(Create(curve))

        self.wait(2)

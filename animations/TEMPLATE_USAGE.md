# Vertical Animation Template Usage

This document explains how to use the vertical animation template for creating consistent 9:16 format educational videos.

## Template Location

`animations/vertical_template.py`

## Layout Structure

The template provides a standard vertical layout optimized for mobile viewing:

```
┌─────────────────────┐ +7.11 (top)
│                     │
│   Title (10%)       │ Title area
│   Subtitle          │
├─────────────────────┤ +5.7 (top separator)
│                     │
│                     │
│   Top Block (42%)   │ Physical animation
│   Center: +2.675    │ Recommended height: 3.5 units
│                     │
│                     │
├─────────────────────┤ -0.35 (middle separator)
│                     │
│                     │
│  Bottom Block (43%) │ Chart/graph
│   Center: -3.375    │ Recommended: 5.0×4.0 units
│                     │
│                     │
├─────────────────────┤ -6.4 (bottom margin)
│   Margin (5%)       │
└─────────────────────┘ -7.11 (bottom)
```

## Basic Usage

### 1. Import the Template

```python
from manim import *
from animations.vertical_template import VerticalTemplate
```

### 2. Create Your Animation Class

```python
class MyAnimation(VerticalTemplate):
    def construct(self):
        # Setup layout
        self.setup_vertical_layout(
            title_text="Your Title",
            subtitle_text="Your subtitle"
        )

        # Add top block content (centered at y = 2.675)
        my_object = Circle().move_to(UP * self.top_block_center)
        self.play(Create(my_object))

        # Add bottom block chart
        axes, x_label, y_label = self.create_chart("x", "y")
        curve = axes.plot(lambda x: x**2, x_range=[0, 2])
        self.play(Create(curve))
```

## Configuration

Make sure your animation directory has a `manim.cfg` file with:

```ini
[CLI]
media_dir = ../../../media/<discipline>
frame_width = 8.0
frame_height = 14.22
```

## Available Methods

### `setup_vertical_layout(title_text, subtitle_text, ...)`

Sets up the standard layout with title, subtitle, and separators.

**Parameters:**
- `title_text` (str): Main title
- `subtitle_text` (str): Subtitle text
- `title_color` (Color): Title color (default: BLACK)
- `subtitle_color` (Color): Subtitle color (default: DARK_BLUE)
- `background_color` (Color): Background (default: WHITE)

### `create_chart(x_label_text, y_label_text, ...)`

Creates a chart in the bottom block.

**Parameters:**
- `x_label_text` (str): X-axis label
- `y_label_text` (str): Y-axis label
- `x_range` (list): [min, max, step] for x-axis (default: [0, 5, 1])
- `y_range` (list): [min, max, step] for y-axis (default: [0, 5, 1])
- `chart_width` (float): Chart width (default: 5.5)
- `chart_height` (float): Chart height (default: 4.5)

**Returns:** `(axes, x_label, y_label)`

## Layout Constants

Available constants for positioning:

```python
self.top_block_center      # 2.675 (center of top block)
self.bottom_block_center   # -3.375 (center of bottom block)
self.TOP_SEPARATOR_Y       # 5.7
self.MIDDLE_SEPARATOR_Y    # -0.35
self.BOTTOM_MARGIN_Y       # -6.4
```

## Recommended Sizes

```python
RECOMMENDED_CONTAINER_HEIGHT = 3.5   # For cylinders, containers
RECOMMENDED_CHART_WIDTH = 5.0        # Chart width
RECOMMENDED_CHART_HEIGHT = 4.0       # Chart height
```

## Complete Example

See `animations/fisica/gas_perfetto/gas_perfetto.py` (TrasformazioneIsoterma) for a complete real-world example.

## Benefits

✅ **Consistent layout** across all animations
✅ **Mobile-optimized** 9:16 aspect ratio
✅ **Proper spacing** with title in top 10%, content in 85%, margin in bottom 5%
✅ **Reusable** for both matematica and fisica
✅ **Easy to maintain** - update template, all animations benefit

## Rendering

Use the Makefile as usual:

```bash
make my_animation QUALITY=ql    # Test with low quality
make my_animation QUALITY=qh    # Production quality
```

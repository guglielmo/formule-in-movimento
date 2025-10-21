# Logo System - Formule in Movimento

This document describes the logo system for **Formule in Movimento**, including all available logo variants, usage guidelines, and technical specifications.

## Logo Concept

The logo combines two symbolic elements:
1. **Infinity symbol (∞)** - Represents endless learning, continuous motion, and mathematical concepts
2. **Play button (▶)** - Represents video content, animation, and dynamic visualization

Together, they embody the project's name: "Formule in Movimento" (Formulas in Motion).

## Available Logo Files

### 1. Source Files (Root Directory)

Located in the project root for reference and editing:

- **`logo-concept.svg`** - Original concept sketch with infinity symbol and play button
- **`logo-full.svg`** - Full logo with "Formule in Movimento" text and tagline
- **`logo-variations.svg`** - Three variations of the symbol (clean, filled play, bold)

### 2. Production Assets (`media/logos/`)

Centralized location for all production-ready logo assets:

- **`logo-icon.svg`** (800x401) - High-resolution icon version (infinity + play)
- **`logo-icon-200.png`** (200x100) - PNG version for Apple touch icon and compatibility
- **`logo-full.svg`** - Full logo with text for print/high-res use
- **`logo-header.svg`** (180x60) - Compact horizontal logo for website navigation
- **`logo-social-og.svg`** (1200x630) - Social media sharing image (Open Graph format)

### 3. Frontend Assets (`frontend/public/`)

Optimized for web delivery and accessible via root path:

- **`/favicon.svg`** (512x512) - Browser favicon, supports all modern browsers
- **`/logo-header.svg`** (180x60) - Website navigation header
- **`/logo-social-og.svg`** (1200x630) - Social media preview image

Access via:
- `/favicon.svg`
- `/logo-header.svg`
- `/logo-social-og.svg`
- `/media/logos/logo-icon-200.png` (via symlink)

## Logo Specifications

### Color Palette

The logo uses a dark, professional color scheme for maximum contrast against light backgrounds:

- **Primary:** `#1a1a2e` (Dark navy, almost black)
- **Secondary:** `#4a4a4a` (Medium gray for subtitles)
- **Background:** `#ffffff` (White)

### Typography

When text is included in the logo:

- **"Formule"** - Georgia, Times New Roman (serif), bold, large
- **"in Movimento"** - Arial, Helvetica (sans-serif), italic, smaller
- **Tagline** - "Matematica e Fisica Animate" in small gray text

### Dimensions

| Asset | Dimensions | Format | Purpose |
|-------|-----------|---------|---------|
| Favicon | 512x512 | SVG | Browser favicon |
| Header Logo | 180x60 | SVG | Website navigation |
| Social/OG Image | 1200x630 | SVG | Social media sharing |
| Icon PNG | 200x100 | PNG | Apple touch icon, fallback |
| Icon SVG | 800x401 | SVG | High-res icon (2:1 ratio) |

## Usage Guidelines

### Website Header

Use `logo-header.svg` (180x60) in the website navigation:

```astro
<img src="/logo-header.svg" alt="Formule in Movimento" height="60" />
```

### Favicon

Already configured in `BaseLayout.astro`:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/media/logos/logo-icon-200.png">
```

### Social Media / Open Graph

Already configured in `BaseLayout.astro`:

```html
<meta property="og:image" content="https://formuleinmovimento.com/logo-social-og.svg">
<meta name="twitter:image" content="https://formuleinmovimento.com/logo-social-og.svg">
```

Override for specific pages:

```astro
<BaseLayout
  title="Page Title"
  description="Page description"
  ogImage="/custom-preview.png"
/>
```

### Print / High Resolution

Use `media/logos/logo-full.svg` for:
- Print materials
- Presentations
- High-resolution displays
- Branding guidelines

### Icon Only

Use `media/logos/logo-icon.svg` or `logo-icon-200.png` for:
- App icons
- Profile pictures
- Thumbnails
- Square format requirements

## File Organization

```
formule-in-movimento/
├── logo-concept.svg              # Source: Original concept
├── logo-full.svg                 # Source: Full logo with text
├── logo-variations.svg           # Source: Variations showcase
├── media/logos/                  # Production assets (committed to git)
│   ├── logo-icon.svg
│   ├── logo-icon-200.png
│   ├── logo-full.svg
│   ├── logo-header.svg
│   └── logo-social-og.svg
└── frontend/public/              # Web-optimized (deployed)
    ├── favicon.svg
    ├── logo-header.svg
    ├── logo-social-og.svg
    └── media -> ../../media      # Symlink for /media/logos/...
```

## Generating Additional Formats

If you need PNG files at different resolutions, use ImageMagick or Inkscape:

### With ImageMagick (CLI):

```bash
# Generate favicon PNG (multiple sizes)
convert media/logos/logo-icon.svg -resize 16x16 frontend/public/favicon-16.png
convert media/logos/logo-icon.svg -resize 32x32 frontend/public/favicon-32.png
convert media/logos/logo-icon.svg -resize 180x180 frontend/public/apple-touch-icon.png

# Generate social media image PNG
convert media/logos/logo-social-og.svg -resize 1200x630 frontend/public/og-image.png
```

### With Inkscape (CLI):

```bash
# High-quality PNG export
inkscape media/logos/logo-icon.svg --export-filename=logo-icon-512.png --export-width=512
inkscape media/logos/logo-full.svg --export-filename=logo-full-hires.png --export-width=2400
```

## SEO and Meta Tags

The logo system is integrated with Astro's `BaseLayout.astro` for optimal SEO:

- ✅ Favicon (SVG + PNG fallback)
- ✅ Apple touch icon
- ✅ Open Graph image
- ✅ Twitter Card image
- ✅ Canonical URLs
- ✅ Theme color matching

All meta tags automatically update based on the page theme (matematica/fisica/home).

## Design Philosophy

### Light Theme

All animations and web pages use a light background theme for better readability and accessibility. The logo is designed with dark colors (`#1a1a2e`) to ensure high contrast on light backgrounds.

### Mobile-First

The logo system is optimized for mobile devices:
- SVG format scales perfectly on all screen sizes
- Compact header logo (180x60) fits well on small screens
- Vertical video support (infinity symbol works in portrait orientation)

### Accessibility

- High contrast ratio (WCAG AAA compliant)
- Alt text always provided
- SVG with proper title/desc tags
- Fallback PNG for older browsers

## Customization

To modify the logo colors or design:

1. Edit the source SVG files in the root directory
2. Regenerate production assets in `media/logos/`
3. Copy updated files to `frontend/public/`
4. Test across different browsers and devices
5. Update documentation if specifications change

## Browser Compatibility

| Browser | Favicon | Touch Icon | OG Image |
|---------|---------|------------|----------|
| Chrome 4+ | ✅ SVG | ✅ PNG | ✅ SVG |
| Firefox 41+ | ✅ SVG | ✅ PNG | ✅ SVG |
| Safari 9+ | ✅ SVG | ✅ PNG | ✅ SVG |
| Edge 79+ | ✅ SVG | ✅ PNG | ✅ SVG |
| Mobile Safari | ✅ SVG | ✅ PNG | ✅ SVG |
| Mobile Chrome | ✅ SVG | ✅ PNG | ✅ SVG |

## Copyright & Usage

The "Formule in Movimento" logo and brand assets are part of this educational project. The logo design combines:
- Infinity symbol (mathematical symbol, public domain)
- Play button icon (common UI element)
- Custom composition and styling

---

**Last Updated:** October 2025
**Maintained by:** Formule in Movimento Team

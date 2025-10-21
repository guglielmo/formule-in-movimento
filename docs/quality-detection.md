# Quality Detection System

## Problem

The project had a mismatch between video quality paths:

- **Frontend pages** hardcoded video paths to specific quality folders (e.g., `854p15`)
- **Production builds** generate different quality folders (e.g., `1920p60` for `QUALITY=qh`)
- Result: High-quality videos were generated but never used by the frontend

## Solution: Smart Quality Detection

### How It Works

The `VideoPlayer` component now:

1. **Accepts quality-agnostic paths**: `/media/matematica/videos/equazioni_lineari/SceneName.mp4` (no quality folder)
2. **Tries multiple qualities in order**:
   - `1920p60` (production high quality, 60fps)
   - `1920p15` (development high quality, 15fps)
   - `1280p30` (medium quality)
   - `854p15` (low quality)
3. **Uses the first available quality**: Client-side script checks each path with `HEAD` requests
4. **Falls back gracefully**: Shows error message if no quality is found

### Implementation

**VideoPlayer.astro**:
```astro
<VideoPlayer src="/media/matematica/videos/equazioni_lineari/RiconoscereEquazioniLineari.mp4" />
```

The component:
- Parses the path to extract discipline, topic, and scene name
- Stores these in `data-*` attributes
- Client-side JavaScript tries each quality level
- Adds the first working `<source>` tag to the video

### Benefits

1. ✅ **Automatic quality selection** - Uses best available quality
2. ✅ **No manual updates needed** - Works with any quality build
3. ✅ **Backward compatible** - Still works with legacy quality-specific paths
4. ✅ **Developer friendly** - Simpler paths in Astro pages
5. ✅ **Production ready** - Automatically uses high-quality videos when available

### File Changes

1. **VideoPlayer.astro**: Added smart quality detection logic
2. **equazioni-lineari.astro**: Updated all video paths (removed quality folders)
3. **gas-perfetto.astro**: Updated all video paths (removed quality folders)
4. **Makefile**: Updated template to generate quality-agnostic paths

### Usage for New Animations

When creating new animations with `make new-animation`, the generated Astro page template now uses quality-agnostic paths:

```astro
<VideoPlayer src="/media/{discipline}/videos/{topic}/IntroScene.mp4" />
```

No need to specify quality - the component handles it automatically!

### Testing

To verify the solution works:

1. **Build low quality** (dev): `make equazioni_lineari QUALITY=ql`
   - Creates videos in `854p15/`
   - Frontend detects and uses these

2. **Build high quality** (prod): `make equazioni_lineari QUALITY=qh`
   - Creates videos in `1920p60/`
   - Frontend automatically switches to these (higher priority)

3. **Frontend**: `make frontend-dev`
   - Open `http://localhost:4321/matematica/equazioni-lineari`
   - Check browser console to see which quality was selected

### Quality Priority Order

The component tries qualities in this order (highest to lowest priority):

1. **1920p60** - `QUALITY=qh` (production, 1080x1920, 60fps)
2. **1920p15** - Custom high-res with low framerate
3. **1280p30** - `QUALITY=qm` (medium, 720x1280, 30fps)
4. **854p15** - `QUALITY=ql` (low, 480x854, 15fps)

This ensures the best available quality is always used.

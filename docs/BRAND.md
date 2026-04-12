# Brand Guide — metadev-protocol

## Color palette (Catppuccin Mocha, blue variant)

| Role | Hex | Name | Usage |
|------|-----|------|-------|
| Background | `#1e1e2e` | Base | Banner, demo, social preview |
| Title/accent | `#89b4fa` | Blue | Project name, highlights |
| Secondary | `#74c7ec` | Sapphire | Subtitles, links |
| Highlight | `#b4befe` | Lavender | Skills, special commands |
| Text | `#cdd6f4` | Text | Body content |
| Muted | `#6c7086` | Overlay | Labels, metadata |
| Surface | `#313244` | Surface 0 | Separators, borders |
| Deep surface | `#181825` | Mantle | Command bars, insets |

## Typography

| Role | Font | Fallback |
|------|------|----------|
| Title (pixel art) | Press Start 2P | Courier New, monospace |
| Body (terminal) | JetBrains Mono | Courier New, monospace |

## Style

- Dark terminal aesthetic — navy background (`#1e2a52`), not pure black
- Scanline effect (subtle, `rgba(0,0,0,0.13)`) + radial vignette
- 3D triple-shadow title (all-blue stack) + soft CRT glow filter
- Blinking cursor (1s cycle) as terminal signature
- Blue-cold tones, no green (except prompt `>` accent), no warm colors
- Hacker/technical feel, never corporate
- Rounded corners (`rx: 14` on the banner frame)

## Assets

| Asset | Path | Format |
|-------|------|--------|
| Banner | `docs/banner.svg` | SVG 900×230 — Press Start 2P embedded as base64 woff2 (GitHub blocks `@import`), ~8.4KB |
| Demo script | `scripts/demo.sh` | Bash |
| Demo tape | `scripts/demo.tape` | VHS (generates GIF) |

## Social preview

GitHub social preview (1280x640) should use the same palette.
Generate from banner.svg or create a dedicated version at `docs/social-preview.png`.

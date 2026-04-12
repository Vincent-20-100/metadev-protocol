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

- Dark terminal aesthetic
- Scanline effect (subtle, `rgba(0,0,0,0.08)`)
- Blue-cold tones, no green, no warm colors
- Hacker/technical feel, never corporate
- Rounded corners (`rx: 12` on containers)

## Assets

| Asset | Path | Format |
|-------|------|--------|
| Banner | `docs/banner.svg` | SVG (900x480) |
| Demo script | `scripts/demo.sh` | Bash |
| Demo tape | `scripts/demo.tape` | VHS (generates GIF) |

## Social preview

GitHub social preview (1280x640) should use the same palette.
Generate from banner.svg or create a dedicated version at `docs/social-preview.png`.

#!/usr/bin/env python3
import html
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path("/home/red/Projects/github-profile")
ASCII_PATH = Path("/home/red/Downloads/face-clean-52.txt")

with open(ASCII_PATH, "r", encoding="utf-8") as f:
    raw_lines = f.read().splitlines()

# Clean ASCII art lines
ascii_lines = []
started = False
for l in raw_lines:
    if l.strip():
        started = True
    if started:
        ascii_lines.append(l)
while ascii_lines and not ascii_lines[-1].strip():
    ascii_lines.pop()

assert len(ascii_lines) == 29, f"Expected 29 lines, got {len(ascii_lines)}"

TOTAL_WIDTH = 64

right_entries = [
    ("top", "red@cachyos", ""),
    ("field", "OS:", "CachyOS Linux, Android, Web"),
    ("field", "Uptime:", "2+ years building"),
    ("field", "Host:", "Negros Occidental, PH"),
    ("field", "Kernel:", "Full-Stack Dev & AI Engineer"),
    ("field", "Shell:", "zsh 5.9 (x86_64)"),
    ("field", "IDE:", "VS Code, Cursor"),
    ("dot", "", ""),
    ("field", "Languages.Programming:", "TypeScript, JavaScript, Python"),
    ("field", "Languages.Markup:", "HTML5, CSS3, Tailwind CSS"),
    ("field", "Frameworks.Web:", "React, Next.js, Node.js, Vite"),
    ("field", "Frameworks.Motion:", "Framer Motion, Three.js"),
    ("field", "Databases:", "PostgreSQL, MongoDB, Supabase"),
    ("field", "AI.Automation:", "n8n, Zapier, Ollama, Agents"),
    ("field", "Tools.DevOps:", "Docker, Git, Vercel, Cloudflare"),
    ("dot", "", ""),
    ("header", "Contact", ""),
    ("field", "Portfolio:", "https://reydian.tech"),
    ("field", "Email.Personal:", "reydian04@gmail.com"),
    ("field", "GitHub:", "bombocl4TTTT"),
    ("field", "LinkedIn:", "reydian-delagao"),
    ("dot", "", ""),
    ("header", "Status & Focus", ""),
    ("field", "Repos:", "27 Repositories on GitHub"),
    ("field", "Primary:", "Next.js, TypeScript, Python"),
    ("field", "Focus:", "Scalable Web & AI Automations"),
    ("field", "Location:", "Bacolod, Philippines (UTC+8)"),
    ("field", "Availability:", "Open for Opportunities"),
    ("dot", "", ""),
]

assert len(right_entries) == 29, f"Expected 29 right entries, got {len(right_entries)}"

# macOS Terminal palette
C_BODY_BG = "#151a20"
C_HEADER_BG = "#1c232c"
C_BORDER = "#283241"
C_DIVIDER = "#232b38"
C_ASCII = "#bfc7ce"
C_ORANGE = "#e2944e"
C_BLUE = "#9dcbf2"
C_DOTS = "#3c434f"
C_HEADER = "#bfc7ce"
C_TITLE_TXT = "#8694a6"

WIDTH = 1020
TITLE_BAR_H = 38
START_Y = TITLE_BAR_H + 34
LINE_HEIGHT = 18.6
FONT_SIZE = 13
HEIGHT = int(START_Y + 28 * LINE_HEIGHT + 34)

START_X_LEFT = 36
START_X_RIGHT = 456

svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="auto">',
    '  <defs>',
    f'    <clipPath id="windowClip">',
    f'      <rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="14" />',
    f'    </clipPath>',
    '  </defs>',
    '',
    '  <!-- Main Window Body -->',
    f'  <rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="14" fill="{C_BODY_BG}" stroke="{C_BORDER}" stroke-width="1.2" />',
    '',
    '  <!-- Window Header / Title Bar (clipped to rounded corners) -->',
    '  <g clip-path="url(#windowClip)">',
    f'    <rect x="1" y="1" width="{WIDTH-2}" height="{TITLE_BAR_H}" fill="{C_HEADER_BG}" />',
    f'    <line x1="1" y1="{TITLE_BAR_H}" x2="{WIDTH-1}" y2="{TITLE_BAR_H}" stroke="{C_DIVIDER}" stroke-width="1" />',
    '  </g>',
    '',
    '  <!-- Apple Window Control Buttons (Traffic Lights) -->',
    '  <!-- Close -->',
    '  <circle cx="22" cy="19" r="5.5" fill="#ff5f56" stroke="#e0443e" stroke-width="0.8" />',
    '  <!-- Minimize -->',
    '  <circle cx="40" cy="19" r="5.5" fill="#ffbd2e" stroke="#dea123" stroke-width="0.8" />',
    '  <!-- Zoom / Expand -->',
    '  <circle cx="58" cy="19" r="5.5" fill="#27c93f" stroke="#1aab29" stroke-width="0.8" />',
    '',
    '  <!-- Window Title (macOS style: red — -zsh — 100×29) -->',
    f'  <text x="{WIDTH/2}" y="23" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'SF Pro Text\', \'Segoe UI\', sans-serif" font-size="11.5" font-weight="500" fill="{C_TITLE_TXT}">red — -zsh — 102×29</text>',
    '',
    '  <!-- Terminal Content (Monospace) -->',
    f'  <g font-family="ui-monospace, \'Fira Code\', \'Cascadia Code\', \'JetBrains Mono\', \'DejaVu Sans Mono\', Menlo, Consolas, monospace" font-size="{FONT_SIZE}" xml:space="preserve">',
]

for i in range(29):
    y = START_Y + i * LINE_HEIGHT
    
    # Left column: ASCII line
    ascii_txt = html.escape(ascii_lines[i])
    svg_parts.append(f'    <text x="{START_X_LEFT}" y="{y:.1f}" fill="{C_ASCII}">{ascii_txt}</text>')
    
    # Right column
    kind, key, val = right_entries[i]
    if kind == "top":
        dashes = "-" * max(2, TOTAL_WIDTH - len(key) - 1)
        line_svg = (
            f'<text x="{START_X_RIGHT}" y="{y:.1f}">'
            f'<tspan fill="{C_BLUE}">{html.escape(key)}</tspan><tspan fill="{C_DOTS}"> {dashes}</tspan>'
            f'</text>'
        )
    elif kind == "header":
        prefix = "- "
        dashes = "-" * max(2, TOTAL_WIDTH - len(prefix) - len(key) - 1)
        line_svg = (
            f'<text x="{START_X_RIGHT}" y="{y:.1f}">'
            f'<tspan fill="{C_DOTS}">{prefix}</tspan><tspan fill="{C_HEADER}">{html.escape(key)}</tspan><tspan fill="{C_DOTS}"> {dashes}</tspan>'
            f'</text>'
        )
    elif kind == "dot":
        line_svg = f'<text x="{START_X_RIGHT}" y="{y:.1f}"><tspan fill="{C_DOTS}">.</tspan></text>'
    elif kind == "field":
        left = ". " + key + " "
        needed = TOTAL_WIDTH - len(left) - len(val) - 1
        dots = "." * max(2, needed)
        line_svg = (
            f'<text x="{START_X_RIGHT}" y="{y:.1f}">'
            f'<tspan fill="{C_ORANGE}">. {html.escape(key)} </tspan>'
            f'<tspan fill="{C_DOTS}">{dots} </tspan>'
            f'<tspan fill="{C_BLUE}">{html.escape(val)}</tspan>'
            f'</text>'
        )
    svg_parts.append(f'    {line_svg}')

svg_parts.append('  </g>')
svg_parts.append('</svg>')

svg_content = "\n".join(svg_parts)

out_svg = ROOT / "assets/header.svg"
out_png = ROOT / "assets/header.png"

with open(out_svg, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Wrote {out_svg}")

# Render to 2x Retina PNG via rsvg-convert
raw_png = "/tmp/raw_terminal.png"
cmd = ["rsvg-convert", "-w", str(WIDTH * 2), str(out_svg), "-o", raw_png]
subprocess.run(cmd, check=True)

# Quantize RGBA with Pillow to keep it fast & lightweight (~120KB)
im = Image.open(raw_png)
im_q = im.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
im_q.save(out_png, optimize=True)
print(f"Rendered and optimized {out_png} ({out_png.stat().st_size:,} bytes)")

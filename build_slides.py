from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Colours ──────────────────────────────────────────────────────────────────
BG       = RGBColor(0x0A, 0x0F, 0x1E)   # dark navy
BLUE     = RGBColor(0x00, 0x62, 0xFF)   # IBM blue
PURPLE   = RGBColor(0x7B, 0x2F, 0xFF)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY    = RGBColor(0xCB, 0xD5, 0xE1)
DGRAY    = RGBColor(0x1E, 0x29, 0x3D)
YELLOW   = RGBColor(0xF5, 0xA6, 0x23)
GREEN    = RGBColor(0x22, 0xC5, 0x5E)

W = Inches(13.33)   # widescreen width
H = Inches(7.5)     # widescreen height

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
blank = prs.slide_layouts[6]   # completely blank layout


def add_slide():
    sl = prs.slides.add_slide(blank)
    bg = sl.background.fill
    bg.solid()
    bg.fore_color.rgb = BG
    return sl


def txb(sl, text, x, y, w, h, size=18, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, italic=False, wrap=True):
    tb = sl.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return tb


def rect(sl, x, y, w, h, fill=DGRAY, line=None, line_width=Pt(1)):
    shape = sl.shapes.add_shape(1, x, y, w, h)   # MSO_SHAPE_TYPE.RECTANGLE = 1
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line:
        shape.line.color.rgb = line
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape


def placeholder_box(sl, label, x, y, w, h):
    """Dashed-border image placeholder with centred label."""
    r = rect(sl, x, y, w, h, fill=RGBColor(0x12, 0x1A, 0x2E), line=BLUE, line_width=Pt(1.5))
    txb(sl, f"[ {label} ]", x, y + h//2 - Inches(0.2), w, Inches(0.4),
        size=13, color=BLUE, align=PP_ALIGN.CENTER, italic=True)
    return r


def accent_bar(sl, x, y, w=Inches(0.06), h=Inches(0.8), color=BLUE):
    rect(sl, x, y, w, h, fill=color, line=None)


def bullet_lines(sl, lines, x, y, w, h, size=17, color=LGRAY, gap=Inches(0.38)):
    for i, line in enumerate(lines):
        txb(sl, f"• {line}", x, y + i * gap, w, Inches(0.35),
            size=size, color=color)


# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 1 — TITLE
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()

# Glow strip at top
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)

# Logo
txb(sl, "DevLift", Inches(1), Inches(1.1), Inches(5), Inches(1.4),
    size=72, bold=True, color=BLUE, align=PP_ALIGN.LEFT)

# Badge
badge = rect(sl, Inches(1), Inches(2.6), Inches(2.8), Inches(0.38), fill=RGBColor(0x00,0x3A,0x99))
txb(sl, "Powered by IBM watsonx.ai", Inches(1.05), Inches(2.63), Inches(2.7), Inches(0.33),
    size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

txb(sl, "AI-Powered Developer Onboarding Accelerator",
    Inches(1), Inches(3.1), Inches(7), Inches(0.5),
    size=22, color=LGRAY)

txb(sl, "IBM Bob Hackathon 2026",
    Inches(1), Inches(3.65), Inches(4), Inches(0.4),
    size=14, color=RGBColor(0x64,0x74,0x8B))

# Image placeholder — right half
placeholder_box(sl, "Screenshot: App Hero Page (slide1.png)",
                Inches(7.2), Inches(0.9), Inches(5.7), Inches(5.4))

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 2 — THE PROBLEM
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)
accent_bar(sl, Inches(0.5), Inches(0.85))
txb(sl, "The Problem", Inches(0.75), Inches(0.8), Inches(8), Inches(0.65),
    size=38, bold=True, color=WHITE)
txb(sl, "Onboarding a new developer is slow, expensive, and unstructured.",
    Inches(0.75), Inches(1.55), Inches(11), Inches(0.4), size=16, color=LGRAY)

# Stat card — right
stat = rect(sl, Inches(9.2), Inches(1.6), Inches(3.5), Inches(2.2), fill=RGBColor(0x00,0x1A,0x57), line=BLUE)
txb(sl, "23", Inches(9.2), Inches(1.75), Inches(3.5), Inches(1.2),
    size=80, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
txb(sl, "days average ramp-up\nper new developer", Inches(9.2), Inches(2.9), Inches(3.5), Inches(0.6),
    size=13, color=LGRAY, align=PP_ALIGN.CENTER)

stat2 = rect(sl, Inches(9.2), Inches(4.0), Inches(3.5), Inches(1.6), fill=RGBColor(0x1A,0x09,0x00), line=YELLOW)
txb(sl, "$15,000+", Inches(9.2), Inches(4.15), Inches(3.5), Inches(0.7),
    size=36, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
txb(sl, "lost productivity per hire", Inches(9.2), Inches(4.85), Inches(3.5), Inches(0.4),
    size=13, color=LGRAY, align=PP_ALIGN.CENTER)

# Bullets
problems = [
    "Engineers spend 3–4 weeks before their first meaningful contribution",
    "Codebases have no structured entry point — files read randomly",
    "Senior devs lose hours/week answering repetitive onboarding questions",
    "No standardised way to measure how contributor-friendly a repo is",
]
bullet_lines(sl, problems, Inches(0.75), Inches(2.05), Inches(8.1), Inches(4), size=17, gap=Inches(0.85))

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 3 — THE SOLUTION
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)
accent_bar(sl, Inches(0.5), Inches(0.85))
txb(sl, "The Solution", Inches(0.75), Inches(0.8), Inches(8), Inches(0.65),
    size=38, bold=True, color=WHITE)

# Mode cards
for i, (icon, title, desc, col) in enumerate([
    ("🔗", "Analyze a Repo", "Paste any GitHub URL → full AI Onboarding Kit in 60 seconds", BLUE),
    ("✦", "Discover Repos", "Describe your stack → get curated open-source repo matches", PURPLE),
]):
    cx = Inches(0.75) + i * Inches(4.5)
    r = rect(sl, cx, Inches(1.65), Inches(4.1), Inches(1.6),
             fill=RGBColor(0x0D,0x18,0x33), line=col)
    txb(sl, f"{icon}  {title}", cx + Inches(0.18), Inches(1.8), Inches(3.7), Inches(0.45),
        size=16, bold=True, color=col)
    txb(sl, desc, cx + Inches(0.18), Inches(2.25), Inches(3.7), Inches(0.7),
        size=13, color=LGRAY)

# Kit output section labels
txb(sl, "Kit includes:", Inches(0.75), Inches(3.5), Inches(4), Inches(0.35),
    size=14, bold=True, color=LGRAY)
kit_items = ["Architecture Overview", "Key Components", "Complexity Hotspots",
             "Suggested First Tasks", "Common Patterns", "Setup Guide"]
for i, item in enumerate(kit_items):
    col_i = i % 2
    row_i = i // 2
    ix = Inches(0.75) + col_i * Inches(3.2)
    iy = Inches(3.9)  + row_i * Inches(0.45)
    txb(sl, f"▸  {item}", ix, iy, Inches(3.0), Inches(0.38), size=14, color=WHITE)

# Readiness badge
rb = rect(sl, Inches(0.75), Inches(5.8), Inches(3.8), Inches(0.45),
          fill=RGBColor(0x00,0x3A,0x99), line=None)
txb(sl, "+ Contribution Readiness Score  (0 – 100)",
    Inches(0.85), Inches(5.83), Inches(3.6), Inches(0.38),
    size=13, bold=True, color=WHITE)

# Placeholder — right
placeholder_box(sl, "Screenshot: Kit Results + Readiness Score (slide3.png)",
                Inches(7.0), Inches(1.55), Inches(5.9), Inches(5.0))

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 4 — TECHNICAL ARCHITECTURE (SWIMLANE)
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)
accent_bar(sl, Inches(0.5), Inches(0.85))
txb(sl, "Technical Architecture", Inches(0.75), Inches(0.8), Inches(10), Inches(0.65),
    size=38, bold=True, color=WHITE)

lanes = [
    (BLUE,   "USER",         "Developer pastes GitHub URL or describes project requirement"),
    (RGBColor(0x06,0xB6,0xD4), "FRONTEND", "Next.js validates input → POST /analyze or /recommend → renders kit"),
    (PURPLE, "BACKEND",      "FastAPI fetches repo tree via GitHub API → builds prompt → calls watsonx.ai → parses JSON"),
    (YELLOW, "IBM watsonx.ai","Llama 3.1 70B receives prompt → returns structured JSON Onboarding Kit"),
]

lane_h = Inches(1.18)
for i, (col, label, desc) in enumerate(lanes):
    y = Inches(1.65) + i * lane_h
    # lane bg
    rect(sl, Inches(0.3), y, W - Inches(0.6), lane_h - Inches(0.06),
         fill=RGBColor(0x0D,0x18,0x33), line=col)
    # label pill
    rect(sl, Inches(0.3), y, Inches(1.9), lane_h - Inches(0.06), fill=col)
    txb(sl, label, Inches(0.35), y + Inches(0.38), Inches(1.8), Inches(0.45),
        size=13, bold=True, color=BG, align=PP_ALIGN.CENTER)
    # description
    txb(sl, desc, Inches(2.35), y + Inches(0.32), Inches(10.5), Inches(0.6),
        size=15, color=WHITE)
    # arrow down (except last)
    if i < len(lanes) - 1:
        txb(sl, "▼", Inches(1.1), y + lane_h - Inches(0.05), Inches(0.5), Inches(0.35),
            size=16, color=LGRAY, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 5 — WHAT YOU GET (Kit sections)
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)
accent_bar(sl, Inches(0.5), Inches(0.85))
txb(sl, "Onboarding Kit: What You Get", Inches(0.75), Inches(0.8), Inches(10), Inches(0.65),
    size=36, bold=True, color=WHITE)

sections = [
    ("🏗", "Architecture Overview", "How the system layers interact and data flows"),
    ("🔑", "Key Components",        "7 most critical files a new dev must read first"),
    ("⚠", "Complexity Hotspots",   "Risky areas flagged with concrete tips"),
    ("✅", "Suggested First Tasks", "Starter contributions ranked easy / medium / hard"),
    ("🔄", "Common Patterns",       "Conventions and idioms used throughout the codebase"),
    ("⚙", "Setup Guide",           "Exact commands to install, run and test locally"),
]

for i, (icon, title, desc) in enumerate(sections):
    col_i = i % 2
    row_i = i // 2
    sx = Inches(0.6)  + col_i * Inches(6.4)
    sy = Inches(1.65) + row_i * Inches(1.7)
    r = rect(sl, sx, sy, Inches(6.0), Inches(1.55), fill=DGRAY, line=BLUE)
    txb(sl, f"{icon}  {title}", sx + Inches(0.2), sy + Inches(0.18),
        Inches(5.6), Inches(0.45), size=16, bold=True, color=WHITE)
    txb(sl, desc, sx + Inches(0.2), sy + Inches(0.65),
        Inches(5.6), Inches(0.6), size=13, color=LGRAY)

# placeholder bottom right — show hotspots screenshot
placeholder_box(sl, "Screenshot: Kit Tabs — Hotspots view (slide5.png)",
                Inches(6.8), Inches(1.55), Inches(6.1), Inches(5.5))

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 6 — DISCOVER REPOS  (new slide for recommendation screenshot)
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=PURPLE)
accent_bar(sl, Inches(0.5), Inches(0.85), color=PURPLE)
txb(sl, "Discover Repos", Inches(0.75), Inches(0.8), Inches(8), Inches(0.65),
    size=38, bold=True, color=WHITE)
txb(sl, "Describe your project — AI finds the best open-source repos matched to your stack.",
    Inches(0.75), Inches(1.55), Inches(6.0), Inches(0.5), size=16, color=LGRAY)

steps = [
    "Describe your tech requirement or project goal in plain English",
    "IBM watsonx.ai extracts 3–5 targeted GitHub search queries",
    "GitHub API returns top-starred repositories for each query",
    "AI ranks and selects the best 3–5 matches with explanations",
    "Each result links directly to a DevLift Onboarding Kit",
]
bullet_lines(sl, steps, Inches(0.75), Inches(2.2), Inches(5.8), Inches(4.5),
             size=16, gap=Inches(0.75))

placeholder_box(sl, "Screenshot: Repo Recommendation Results",
                Inches(7.0), Inches(1.55), Inches(5.9), Inches(5.5))

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 7 — TECH STACK
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)
accent_bar(sl, Inches(0.5), Inches(0.85))
txb(sl, "Tech Stack", Inches(0.75), Inches(0.8), Inches(8), Inches(0.65),
    size=38, bold=True, color=WHITE)

stack = [
    ("Frontend",       "Next.js 14 · TypeScript · Tailwind CSS",  "Vercel",  BLUE),
    ("Backend",        "FastAPI (Python) · Uvicorn",               "Render",  RGBColor(0x06,0xB6,0xD4)),
    ("AI Model",       "IBM watsonx.ai · Meta Llama 3.1 70B",     "",        YELLOW),
    ("Repo Data",      "GitHub REST API",                          "",        GREEN),
    ("Font",           "Geist Mono",                               "",        LGRAY),
]

for i, (layer, tech, host, col) in enumerate(stack):
    y = Inches(1.65) + i * Inches(0.95)
    rect(sl, Inches(0.6), y, Inches(12.1), Inches(0.82), fill=DGRAY, line=None)
    # colour bar
    rect(sl, Inches(0.6), y, Inches(0.12), Inches(0.82), fill=col)
    txb(sl, layer, Inches(0.85), y + Inches(0.2), Inches(2.0), Inches(0.42),
        size=15, bold=True, color=col)
    txb(sl, tech, Inches(3.0), y + Inches(0.2), Inches(6.5), Inches(0.42),
        size=15, color=WHITE)
    if host:
        txb(sl, host, Inches(10.5), y + Inches(0.2), Inches(2.0), Inches(0.42),
            size=13, color=LGRAY, align=PP_ALIGN.RIGHT)

txb(sl, "Live: devlift-ten.vercel.app",
    Inches(0.75), Inches(6.7), Inches(8), Inches(0.45),
    size=15, color=BLUE, bold=True)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 8 — BUSINESS VALUE
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)
accent_bar(sl, Inches(0.5), Inches(0.85))
txb(sl, "Business Value", Inches(0.75), Inches(0.8), Inches(8), Inches(0.65),
    size=38, bold=True, color=WHITE)

cards = [
    ("23 days → 60 sec", "Onboarding time reduced",          BLUE),
    ("$15,000+",          "Saved per new developer hire",     GREEN),
    ("Every team",        "Universal market — all industries",PURPLE),
    ("3 revenue paths",   "SaaS · GitHub App · Enterprise API", YELLOW),
]
for i, (stat, label, col) in enumerate(cards):
    cx = Inches(0.6) + (i % 2) * Inches(6.4)
    cy = Inches(1.65) + (i // 2) * Inches(2.4)
    r = rect(sl, cx, cy, Inches(6.0), Inches(2.1), fill=DGRAY, line=col)
    txb(sl, stat,  cx + Inches(0.25), cy + Inches(0.25), Inches(5.5), Inches(0.9),
        size=30, bold=True, color=col)
    txb(sl, label, cx + Inches(0.25), cy + Inches(1.2),  Inches(5.5), Inches(0.55),
        size=15, color=LGRAY)

txb(sl, "DevLift pays for itself the first time a new developer joins your team.",
    Inches(0.75), Inches(6.85), Inches(11.5), Inches(0.45),
    size=14, color=LGRAY, italic=True, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 9 — WHAT'S NEXT
# ─────────────────────────────────────────────────────────────────────────────
sl = add_slide()
rect(sl, 0, 0, W, Inches(0.04), fill=BLUE)
accent_bar(sl, Inches(0.5), Inches(0.85))
txb(sl, "What's Next", Inches(0.75), Inches(0.8), Inches(8), Inches(0.65),
    size=38, bold=True, color=WHITE)

roadmap = [
    ("🔌", "VS Code Extension",  "Onboarding kit inside your IDE — no browser needed"),
    ("🤖", "Slack Bot",          "/devlift command in any engineering channel"),
    ("🏢", "Enterprise API",     "White-label kit generation for large engineering teams"),
]
for i, (icon, title, desc) in enumerate(roadmap):
    rx = Inches(0.6) + i * Inches(4.2)
    r = rect(sl, rx, Inches(1.65), Inches(3.9), Inches(2.4), fill=DGRAY, line=BLUE)
    txb(sl, icon,  rx + Inches(0.25), Inches(1.85), Inches(0.6), Inches(0.6), size=28)
    txb(sl, title, rx + Inches(0.25), Inches(2.5),  Inches(3.4), Inches(0.45),
        size=18, bold=True, color=WHITE)
    txb(sl, desc,  rx + Inches(0.25), Inches(3.0),  Inches(3.4), Inches(0.75),
        size=14, color=LGRAY)

# CTA box
cta = rect(sl, Inches(0.6), Inches(4.5), Inches(12.1), Inches(1.2),
           fill=RGBColor(0x00,0x1A,0x57), line=BLUE)
txb(sl, "Try it now:  devlift-ten.vercel.app",
    Inches(0.85), Inches(4.65), Inches(11.5), Inches(0.45),
    size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txb(sl, "Built with IBM Bob  ·  IBM Bob Hackathon 2026",
    Inches(0.85), Inches(5.15), Inches(11.5), Inches(0.35),
    size=13, color=LGRAY, align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────────────────
out = r"C:\Users\rohan\devlift\devlift_pitch.pptx"
prs.save(out)
print(f"Saved: {out}")

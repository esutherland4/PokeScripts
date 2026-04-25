#!/usr/bin/env python3
"""
Pokemon Puppet Template Generator
Generates printable SVG tracing sheets for paper stick puppets.

Print at 100% on US Letter paper.  Scale: 96 px = 1 inch.
Each sheet: one Pokemon, all shapes colour-coded and labelled.
"""

import os, math


def leaf_path(bx, by, tx, ty, hw, fill, stroke="#222", sw=2.5):
    """
    Proper organic leaf shape from base point (bx,by) to tip (tx,ty).
    hw = half-width at the widest point (around 30% from base).
    Narrows naturally from base, bulges wide in lower-third, tapers to tip.
    """
    dx, dy = tx - bx, ty - by
    L = math.sqrt(dx * dx + dy * dy)
    px, py = -dy / L, dx / L          # unit perpendicular (right-hand side)

    # Control points: right side of leaf
    cr1x = bx + dx * 0.22 + px * hw
    cr1y = by + dy * 0.22 + py * hw
    cr2x = bx + dx * 0.62 + px * hw * 0.55
    cr2y = by + dy * 0.62 + py * hw * 0.55

    # Control points: left side of leaf (mirror)
    cl1x = bx + dx * 0.62 - px * hw * 0.55
    cl1y = by + dy * 0.62 - py * hw * 0.55
    cl2x = bx + dx * 0.22 - px * hw
    cl2y = by + dy * 0.22 - py * hw

    d = (
        f"M {bx:.1f},{by:.1f} "
        f"C {cr1x:.1f},{cr1y:.1f} {cr2x:.1f},{cr2y:.1f} {tx:.1f},{ty:.1f} "
        f"C {cl1x:.1f},{cl1y:.1f} {cl2x:.1f},{cl2y:.1f} {bx:.1f},{by:.1f} Z"
    )
    return pth(d, fill, stroke, sw)

OUT = os.path.expanduser("~/Code/Projects/Pokemon/templates")
os.makedirs(OUT, exist_ok=True)

PW, PH = 816, 1056   # 8.5 × 11 in at 96 dpi


# ── SVG primitives ──────────────────────────────────────────────────────────

def el(cx, cy, rx, ry, fill, stroke="#222", sw=2.5, opacity=1):
    return f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>\n'

def circ(cx, cy, r, fill, stroke="#222", sw=2.5, opacity=1):
    return el(cx, cy, r, r, fill, stroke, sw, opacity)

def rr(x, y, w, h, r, fill, stroke="#222", sw=2.5):
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'

def poly(pts, fill, stroke="#222", sw=2.5):
    s = " ".join(f"{x},{y}" for x, y in pts)
    return f'  <polygon points="{s}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'

def pth(d, fill, stroke="#222", sw=2.5):
    return f'  <path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'

def tx(x, y, t, size=10, anchor="middle", weight="normal", fill="#444"):
    return f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial,Helvetica" font-size="{size}" font-weight="{weight}" fill="{fill}">{t}</text>\n'

def swatch(cx, y, label, color):
    """Pill-shaped colour badge below a shape."""
    w = len(label) * 6.4 + 18
    return (
        f'  <rect x="{cx - w/2:.0f}" y="{y}" width="{w:.0f}" height="16" rx="5" '
        f'fill="{color}" opacity="0.28" stroke="{color}" stroke-width="1.2"/>\n'
        f'  <text x="{cx}" y="{y+11.5:.1f}" text-anchor="middle" font-family="Arial" '
        f'font-size="9" font-weight="bold" fill="#111">{label}</text>\n'
    )

def divider(y):
    return f'  <line x1="28" y1="{y}" x2="{PW-28}" y2="{y}" stroke="#E8E8E8" stroke-width="1" stroke-dasharray="5,4"/>\n'

def row_label(y, t):
    return tx(PW // 2, y, t, size=8.5, fill="#AAAAAA")

PREV_CX = PW // 2   # 408  — horizontal centre of preview box
PREV_CY = 978       # vertical centre of preview box

def preview_box():
    """Returns the 'ASSEMBLED PREVIEW' section drawn at the bottom of each page."""
    return (
        divider(892) +
        row_label(902, "ASSEMBLED — how the pieces look when put together") +
        f'  <rect x="{PREV_CX - 108}" y="912" width="216" height="128" '
        f'rx="6" fill="#F8F8F8" stroke="#DDD" stroke-width="1.5"/>\n'
    )

def page(title, content):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}">
  <rect width="{PW}" height="{PH}" fill="white"/>
  <text x="{PW//2}" y="34" text-anchor="middle"
        font-family="Arial Black,Impact,Arial" font-size="22" font-weight="900" fill="#111">{title}</text>
  <text x="{PW//2}" y="52" text-anchor="middle"
        font-family="Arial" font-size="9.5" fill="#888">Trace each shape onto the matching colour paper · cut out · layer onto a craft stick</text>
  <line x1="24" y1="62" x2="{PW-24}" y2="62" stroke="#CCC" stroke-width="1.5"/>
{content}
  <text x="{PW//2}" y="{PH-12}" text-anchor="middle"
        font-family="Arial" font-size="7.5" fill="#CCC">Print at 100% · 96 px = 1 inch · Pokemon puppet craft</text>
</svg>'''


# ── Pointed-ear helper ──────────────────────────────────────────────────────

def pointed_oval(cx, cy, rx, ry, fill, taper=0.35, stroke="#222", sw=2.5):
    """Ellipse with a pointed top (for ears)."""
    # tip at (cx, cy-ry), bulge at sides
    bx = rx
    by = ry * taper           # how far down the side control-points sit
    d = (
        f"M {cx},{cy - ry} "                                    # top tip
        f"C {cx + bx},{cy - ry + by * 2} "
        f"  {cx + bx},{cy + ry * 0.6} "
        f"  {cx},{cy + ry} "                                    # bottom right curve
        f"C {cx - bx},{cy + ry * 0.6} "
        f"  {cx - bx},{cy - ry + by * 2} "
        f"  {cx},{cy - ry} Z"                                   # back to tip
    )
    return pth(d, fill, stroke, sw)


# ══════════════════════════════════════════════════════════════════════════════
# PIKACHU
# ══════════════════════════════════════════════════════════════════════════════

def pikachu():
    YEL = "#FFD84D"
    RED = "#D93030"
    BLK = "#1A1A1A"
    CRM = "#FFFACC"

    s = ""

    # ── ROW 1: large shapes ─────────────────────────────── y 70 – 455 ──
    s += row_label(77, "LARGE  (4\")  —  trace onto YELLOW paper")

    # Body: 4" × 3.5" oval
    bx, by = 210, 278
    s += el(bx, by, 192, 166, YEL)
    s += swatch(bx, by + 170, "YELLOW — Body  (4\")", YEL)

    # Head: 3" circle
    hx, hy = 590, 260
    s += el(hx, hy, 145, 142, YEL)
    s += swatch(hx, hy + 146, "YELLOW — Head  (3\")", YEL)

    s += divider(468)

    # ── ROW 2: medium shapes ────────────────────────────── y 480 – 730 ──
    s += row_label(486, "MEDIUM  (2-3\")  —  various colours")

    # Ears (tall pointed, ~0.75\" wide × 2\" tall)
    ex1, ey = 105, 610
    ex2 = 218
    s += pointed_oval(ex1, ey, 40, 95, YEL)
    s += pointed_oval(ex2, ey, 40, 95, YEL)
    s += swatch(161, ey + 98, "YELLOW — Ears  ×2  (0.75\"×2\")", YEL)

    # Ear tips: black cap drawn over ear top (~same width, shorter)
    s += pointed_oval(ex1, ey - 55, 38, 48, BLK)
    s += pointed_oval(ex2, ey - 55, 38, 48, BLK)
    s += swatch(161, ey - 55 - 50 + 4, "BLACK — Ear Tips  ×2", BLK)

    # Belly: ~2\"×1.5\" cream oval
    belly_cx, belly_cy = 440, 600
    s += el(belly_cx, belly_cy, 100, 72, CRM)
    s += swatch(belly_cx, belly_cy + 76, "CREAM — Belly  (2\"×1.5\")", CRM)

    # Cheeks: ~1\" red circles
    ck1x, ck1y = 615, 590
    ck2x, ck2y = 735, 590
    s += circ(ck1x, ck1y, 50, RED)
    s += circ(ck2x, ck2y, 50, RED)
    s += swatch((ck1x + ck2x) // 2, ck1y + 54, "RED — Cheeks  ×2  (1\")", RED)

    s += divider(744)

    # ── ROW 3: small shapes + tail ──────────────────────── y 755 – 1020 ──
    s += row_label(760, "SMALL  (≤1\")  +  Tail")

    # Eyes: ~0.55\"×0.7\" ovals
    s += el(92, 840, 28, 35, BLK)
    s += el(190, 840, 28, 35, BLK)
    s += swatch(141, 879, "BLACK — Eyes  ×2", BLK)

    # Nose: tiny
    s += el(308, 836, 14, 10, BLK)
    s += swatch(308, 850, "BLACK — Nose", BLK)

    # Tail — lightning-bolt polygon ~2\"×2.4\"
    tx0, ty0 = 430, 766
    tail = [
        (tx0 + 55, ty0),        # top-right
        (tx0 + 8,  ty0),        # top-left
        (tx0 + 30, ty0 + 108),  # mid-left (diagonal down)
        (tx0 - 8,  ty0 + 108),  # jog left
        (tx0 + 48, ty0 + 232),  # bottom tip
        (tx0 + 72, ty0 + 232),  # bottom-right
        (tx0 + 52, ty0 + 130),  # back up-right
        (tx0 + 82, ty0 + 130),  # jog right
    ]
    s += poly(tail, YEL)
    s += swatch(tx0 + 37, ty0 + 237, "YELLOW — Tail  (lightning bolt)", YEL)

    s += preview_box()
    s += el(408,990,42,37,YEL); s += el(408,993,23,16,CRM)          # body + belly
    s += circ(408,952,32,YEL)                                         # head
    s += pointed_oval(390,922,9,20,YEL); s += pointed_oval(426,922,9,20,YEL)  # ears
    s += el(390,913,8,8,BLK);  s += el(426,913,8,8,BLK)             # ear tips
    s += circ(390,958,11,RED); s += circ(426,958,11,RED)             # cheeks
    s += el(400,945,6,8,BLK);  s += el(416,945,6,8,BLK)             # eyes
    s += poly([(442,988),(450,988),(444,1001),(452,1001),(435,1021),(427,1021),(436,1004),(425,1004)],YEL)
    return page("⚡ PIKACHU — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# CHARMANDER
# ══════════════════════════════════════════════════════════════════════════════

def charmander():
    ORG = "#E8732A"
    CRM = "#FDECC8"
    BLU = "#4A8FD4"
    YEL = "#FFD84D"
    RED = "#D93030"
    BLK = "#1A1A1A"

    s = ""

    # ── ROW 1: large shapes ─────────────────────────────── y 70 – 470 ──
    s += row_label(77, "LARGE  (3-4\")  —  trace onto ORANGE paper")

    # Body: taller than wide, ~3\"×4\"
    bx, by = 200, 285
    s += el(bx, by, 145, 178, ORG)
    s += swatch(bx, by + 182, "ORANGE — Body  (3\"×4\")", ORG)

    # Head: ~3\" circle
    hx, hy = 585, 255
    s += el(hx, hy, 142, 138, ORG)
    s += swatch(hx, hy + 142, "ORANGE — Head  (3\")", ORG)

    s += divider(478)

    # ── ROW 2: medium shapes ────────────────────────────── y 488 – 730 ──
    s += row_label(494, "MEDIUM  (2-3\")  —  belly, tail, arms")

    # Belly: cream oval ~2\"×2.5\"
    belly_cx, belly_cy = 165, 620
    s += el(belly_cx, belly_cy, 100, 122, CRM)
    s += swatch(belly_cx, belly_cy + 126, "CREAM — Belly  (2\"×2.5\")", CRM)

    # Tail: tapered oval, angled ~1\"×2.5\"
    # Using a rotated ellipse approximated with a path
    tcx, tcy = 370, 600
    tail_d = (
        f"M {tcx},{tcy - 120} "
        f"C {tcx + 70},{tcy - 100} {tcx + 90},{tcy + 60} {tcx + 20},{tcy + 120} "
        f"C {tcx - 10},{tcy + 130} {tcx - 50},{tcy + 80} {tcx - 30},{tcy - 60} "
        f"C {tcx - 20},{tcy - 100} {tcx},{tcy - 120} Z"
    )
    s += pth(tail_d, ORG)
    s += swatch(tcx + 20, tcy + 135, "ORANGE — Tail  (1\"×2.5\")", ORG)

    # Flame: yellow teardrop blob
    fx, fy = 540, 530
    flame_d = (
        f"M {fx},{fy - 80} "
        f"C {fx + 55},{fy - 40} {fx + 55},{fy + 50} {fx},{fy + 75} "
        f"C {fx - 55},{fy + 50} {fx - 55},{fy - 40} {fx},{fy - 80} Z"
    )
    s += pth(flame_d, YEL)
    # Flame tip (red)
    flame_tip_d = (
        f"M {fx},{fy - 80} "
        f"C {fx + 30},{fy - 65} {fx + 30},{fy - 20} {fx},{fy - 10} "
        f"C {fx - 30},{fy - 20} {fx - 30},{fy - 65} {fx},{fy - 80} Z"
    )
    s += pth(flame_tip_d, RED)
    s += swatch(fx, fy + 80, "YELLOW + RED tip — Flame", YEL)

    # Arms: small ovals ~0.75\"×0.5\"  (two side by side)
    s += el(690, 580, 38, 28, ORG)
    s += el(780, 590, 35, 26, ORG)
    s += swatch(735, 622, "ORANGE — Arms  ×2  (0.75\"×0.5\")", ORG)

    s += divider(742)

    # ── ROW 3: small shapes ─────────────────────────────── y 752 – 1020 ──
    s += row_label(758, "SMALL  (≤1\")  —  eyes, nostrils")

    # Eyes: blue circles ~0.65\"
    s += circ(110, 840, 32, BLU)
    s += circ(210, 840, 32, BLU)
    s += swatch(160, 876, "BLUE — Eyes  ×2  (0.65\")", BLU)

    # Pupils: black dots
    s += circ(118, 836, 14, BLK)
    s += circ(218, 836, 14, BLK)
    s += swatch(168, 855, "BLACK — Pupils  ×2", BLK)

    # Nostrils: tiny
    s += circ(330, 832, 8, BLK)
    s += circ(356, 832, 8, BLK)
    s += swatch(343, 844, "BLACK — Nostrils  ×2", BLK)

    s += preview_box()
    s += el(408,990,32,38,ORG); s += el(408,988,22,26,CRM)          # body + belly
    s += el(408,951,31,30,ORG)                                        # head
    s += circ(399,944,7,BLU); s += circ(416,944,7,BLU)              # eyes
    s += circ(399,939,4,BLK); s += circ(416,939,4,BLK)              # pupils
    s += el(445,997,9,24,ORG)                                         # tail
    s += circ(445,970,9,YEL); s += circ(445,964,5,RED)              # flame
    return page("🔥 CHARMANDER — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# BULBASAUR
# ══════════════════════════════════════════════════════════════════════════════

def bulbasaur():
    TEAL  = "#5BBFAA"
    DTEAL = "#3A8070"
    DGRN  = "#2E7A2E"
    RED   = "#D93030"
    CRM   = "#E8F8F0"
    BLK   = "#1A1A1A"

    s = ""

    # ── ROW 1: large shapes ─────────────────────────────── y 70 – 460 ──
    s += row_label(77, "LARGE  (3-4\")  —  trace onto TEAL / BLUE-GREEN paper")

    bx, by = 205, 275
    s += el(bx, by, 188, 158, TEAL)
    s += swatch(bx, by + 162, "TEAL — Body  (4\"×3\")", TEAL)

    hx, hy = 585, 255
    s += el(hx, hy, 142, 138, TEAL)
    s += swatch(hx, hy + 142, "TEAL — Head  (3\")", TEAL)

    s += divider(470)

    # ── ROW 2: medium shapes ────────────────────────────── y 480 – 730 ──
    s += row_label(486, "MEDIUM  —  bulb assembly (dark green) · spots ×4 · eyes ×2 (red) · belly (cream)")

    # ── Bulb: garlic-bulb silhouette with clove ridge lines ──────────────
    # Wide round body, tapers inward to a narrow neck, small pointed tip.
    bcx, bcy = 168, 650

    bulb_d = (
        f"M {bcx},{bcy + 68} "
        # Right side — bottom round, swells out wide, then narrows toward neck
        f"C {bcx+64},{bcy+68} {bcx+102},{bcy+44} {bcx+102},{bcy+6} "
        f"C {bcx+102},{bcy-30} {bcx+86},{bcy-72} {bcx+56},{bcy-102} "
        # Neck taper to tip (right side)
        f"C {bcx+36},{bcy-122} {bcx+14},{bcy-136} {bcx},{bcy-144} "
        # Tip to left neck
        f"C {bcx-14},{bcy-136} {bcx-36},{bcy-122} {bcx-56},{bcy-102} "
        # Left side — mirror
        f"C {bcx-86},{bcy-72} {bcx-102},{bcy-30} {bcx-102},{bcy+6} "
        f"C {bcx-102},{bcy+44} {bcx-64},{bcy+68} {bcx},{bcy+68} Z"
    )
    s += pth(bulb_d, DGRN)

    # Vertical clove-ridge lines (follow the bulb contour, converge at tip)
    tip_y  = bcy - 140
    base_y = bcy + 66
    for xo in [-62, -30, 0, 30, 62]:
        tx_r  = bcx + xo * 0.20   # converge near tip
        bx_r  = bcx + xo * 0.38   # slight spread at base
        cp1x  = bcx + xo * 0.95;  cp1y = bcy - 68
        cp2x  = bcx + xo * 0.92;  cp2y = bcy + 22
        s += pth(
            f"M {tx_r:.0f},{tip_y} "
            f"C {cp1x:.0f},{cp1y} {cp2x:.0f},{cp2y} {bx_r:.0f},{base_y}",
            "none", "#174F17", 1.8
        )

    s += swatch(bcx, bcy + 72, "DARK GREEN — Bulb  (garlic shape, ~2\" wide × 2.2\" tall)", DGRN)

    # ── Spots: 2×2 grid ───────────────────────────────────────────────────
    for (sx, sy), (srx, sry) in [
        ((400, 528), (34, 24)), ((468, 528), (28, 20)),
        ((400, 595), (30, 22)), ((468, 595), (34, 25)),
    ]:
        s += el(sx, sy, srx, sry, DTEAL)
    s += swatch(434, 626, "DARK TEAL — Body Spots  ×4", DTEAL)

    # ── Eyes ──────────────────────────────────────────────────────────────
    s += el(578, 548, 28, 34, RED)
    s += el(652, 548, 28, 34, RED)
    s += swatch(615, 586, "RED — Eyes  ×2  (0.6\")", RED)

    # ── Belly patch ───────────────────────────────────────────────────────
    s += el(750, 595, 50, 72, CRM)
    s += swatch(750, 671, "CREAM — Belly  (1\"×1.5\")", CRM)

    s += divider(742)

    # ── ROW 3: small shapes ─────────────────────────────── y 752 – 1020 ──
    s += row_label(758, "SMALL  —  pupils, toe nubs")

    s += circ(115, 840, 14, BLK)
    s += circ(190, 840, 14, BLK)
    s += swatch(152, 858, "BLACK — Pupils  ×2", BLK)

    for i in range(6):
        s += circ(330 + i * 36, 840, 14, TEAL)
    s += swatch(510, 858, "TEAL — Toe Nubs  ×6  (3 per foot)", TEAL)

    s += preview_box()
    s += el(408,990,41,35,TEAL); s += circ(408,952,31,TEAL)         # body + head
    s += el(398,946,6,8,RED);    s += el(420,946,6,8,RED)           # eyes
    bx,by=383,977  # mini garlic bulb
    s += pth(f"M {bx},{by+12} C {bx+12},{by+12} {bx+20},{by+7} {bx+20},{by+1} C {bx+20},{by-7} {bx+15},{by-14} {bx+9},{by-20} C {bx+3},{by-26} {bx},{by-28} {bx},{by-28} C {bx},{by-28} {bx-3},{by-26} {bx-9},{by-20} C {bx-15},{by-14} {bx-20},{by-7} {bx-20},{by+1} C {bx-20},{by+7} {bx-12},{by+12} {bx},{by+12} Z",DGRN)
    return page("🌿 BULBASAUR — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# JIGGLYPUFF
# ══════════════════════════════════════════════════════════════════════════════

def jigglypuff():
    PINK  = "#F7B8CA"
    DPINK = "#D4607A"
    BLU   = "#5FA8E8"
    LTBLU = "#A8D4F5"
    BLK   = "#1A1A1A"
    CRM   = "#FFF8F8"

    s = ""

    # ── ROW 1: large shapes ─────────────────────────────── y 70 – 470 ──
    s += row_label(77, "LARGE  (4\")  —  trace onto PINK paper")

    # Body: large round circle ~4\"
    bx, by = 220, 275
    s += circ(bx, by, 192, PINK)
    s += swatch(bx, by + 196, "PINK — Body  (4\" circle)", PINK)

    # Head (same as body for Jigglypuff — it IS the body; show head circle for assembly reference)
    hx, hy = 588, 260
    s += circ(hx, hy, 145, PINK)
    s += swatch(hx, hy + 149, "PINK — Head  (3\" circle)\n[Same colour as body]", PINK)

    s += divider(478)

    # ── ROW 2: medium shapes ────────────────────────────── y 488 – 730 ──
    s += row_label(494, "MEDIUM  —  ears (pink), eyes (blue)")

    # Ears: small pointed ovals ~0.5\"×1\"
    s += pointed_oval(140, 620, 30, 62, PINK)
    s += pointed_oval(240, 620, 30, 62, PINK)
    s += swatch(190, 686, "PINK — Ears  ×2  (0.5\"×1\")", PINK)

    # Eyes: large circles ~1\" (distinctive big Jigglypuff eyes)
    s += circ(450, 590, 55, BLU)
    s += circ(580, 590, 55, BLU)
    s += swatch(515, 649, "BLUE — Eyes  ×2  (1\" circles)", BLU)

    # Eye highlights
    s += circ(462, 578, 16, LTBLU, stroke="none")
    s += circ(592, 578, 16, LTBLU, stroke="none")
    s += swatch(515, 595, "LIGHT BLUE — Eye Highlights  ×2", LTBLU)

    # Inner ear blush
    s += el(730, 610, 22, 40, DPINK, opacity=0.5)
    s += el(730, 610, 22, 40, "none", DPINK, 1.5)
    s += swatch(730, 654, "DARK PINK — Ear Blush  ×2", DPINK)

    s += divider(742)

    # ── ROW 3: small + forehead curl ────────────────────── y 752 – 1020 ──
    s += row_label(758, "SMALL  —  pupils, curl, mouth blush")

    # Pupils
    s += circ(105, 840, 15, BLK)
    s += circ(200, 840, 15, BLK)
    s += swatch(152, 859, "BLACK — Pupils  ×2", BLK)

    # Forehead curl: spiral-ish — approximated as a small curved teardrop
    ccx, ccy = 345, 820
    curl_d = (
        f"M {ccx},{ccy - 38} "
        f"C {ccx + 28},{ccy - 38} {ccx + 36},{ccy - 10} {ccx + 20},{ccy + 8} "
        f"C {ccx + 6},{ccy + 24} {ccx - 14},{ccy + 18} {ccx - 10},{ccy + 0} "
        f"C {ccx - 6},{ccy - 14} {ccx + 6},{ccy - 12} {ccx},{ccy - 38} Z"
    )
    s += pth(curl_d, DPINK)
    s += swatch(ccx, ccy + 40, "DARK PINK — Forehead Curl", DPINK)

    # Mouth blush dots: tiny pink circles on cheeks
    s += circ(530, 830, 10, DPINK, stroke="none")
    s += circ(590, 830, 10, DPINK, stroke="none")
    s += swatch(560, 844, "DARK PINK — Mouth dots  ×2", DPINK)

    s += preview_box()
    s += circ(408,978,42,PINK)                                        # big round body
    s += pointed_oval(388,944,8,16,PINK); s += pointed_oval(428,944,8,16,PINK)  # ears
    s += circ(394,970,13,BLU);  s += circ(422,970,13,BLU)           # eyes
    s += circ(394,966,7,BLK);   s += circ(422,966,7,BLK)            # pupils
    s += circ(408,956,6,DPINK)                                        # forehead curl
    return page("🎤 JIGGLYPUFF — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# EEVEE
# ══════════════════════════════════════════════════════════════════════════════

def eevee():
    BRN  = "#8B5828"
    LBRN = "#A87040"
    TAN  = "#DEB887"
    CRM  = "#F5EDCA"
    BLK  = "#1A1A1A"
    DBLU = "#3C2A10"   # dark eye colour

    s = ""

    # ── ROW 1: large shapes ─────────────────────────────── y 70 – 470 ──
    s += row_label(77, "LARGE  (3-4\")  —  trace onto BROWN paper")

    # Body: ~3\"×3.5\"
    bx, by = 205, 280
    s += el(bx, by, 148, 168, BRN)
    s += swatch(bx, by + 172, "BROWN — Body  (3\"×3.5\")", BRN)

    # Head: ~2.75\" circle
    hx, hy = 588, 258
    s += circ(hx, hy, 136, BRN)
    s += swatch(hx, hy + 140, "BROWN — Head  (2.75\")", BRN)

    s += divider(478)

    # ── ROW 2: medium shapes ────────────────────────────── y 488 – 730 ──
    s += row_label(494, "MEDIUM  —  ears (brown), collar (cream/tan), tail")

    # Ears: large pointed ~1\"×2\"
    s += pointed_oval(120, 618, 50, 96, BRN)
    s += pointed_oval(238, 618, 50, 96, BRN)
    s += swatch(179, 718, "BROWN — Ears  ×2  (1\"×2\")", BRN)

    # Inner ear: cream liner, slightly smaller
    s += pointed_oval(120, 626, 32, 75, CRM)
    s += pointed_oval(238, 626, 32, 75, CRM)
    s += swatch(179, 706, "CREAM — Inner Ear  ×2", CRM)

    # Collar: fluffy oval ~3\"×1.5\" cream
    ccx, ccy = 490, 590
    # Slightly irregular fluffy collar shape
    collar_d = (
        f"M {ccx},{ccy - 72} "
        f"C {ccx + 80},{ccy - 80} {ccx + 148},{ccy - 30} {ccx + 148},{ccy + 0} "
        f"C {ccx + 148},{ccy + 30} {ccx + 80},{ccy + 72} {ccx},{ccy + 72} "
        f"C {ccx - 80},{ccy + 72} {ccx - 148},{ccy + 30} {ccx - 148},{ccy + 0} "
        f"C {ccx - 148},{ccy - 30} {ccx - 80},{ccy - 80} {ccx},{ccy - 72} Z"
    )
    s += pth(collar_d, CRM)
    s += swatch(ccx, ccy + 76, "CREAM/TAN — Collar  (3\"×1.5\")", CRM)

    # Tail: fluffy oval + cream tip
    tx_tail, ty_tail = 730, 590
    s += el(tx_tail, ty_tail, 52, 75, BRN)
    s += el(tx_tail, ty_tail + 40, 44, 40, CRM)  # cream tip on bottom
    s += swatch(tx_tail, ty_tail + 119, "BROWN + CREAM tip — Tail", BRN)

    s += divider(742)

    # ── ROW 3: small shapes ─────────────────────────────── y 752 – 1020 ──
    s += row_label(758, "SMALL  —  eyes, nose")

    # Eyes: large oval, dark brown ~0.7\"
    s += el(115, 835, 34, 42, LBRN)
    s += el(225, 835, 34, 42, LBRN)
    s += swatch(170, 881, "BROWN — Eyes  ×2  (0.7\")", LBRN)

    # Pupils
    s += circ(122, 830, 16, BLK)
    s += circ(232, 830, 16, BLK)
    s += swatch(177, 850, "BLACK — Pupils  ×2", BLK)

    # Eye shine
    s += circ(130, 820, 7, "#FFFFFF", stroke="none")
    s += circ(240, 820, 7, "#FFFFFF", stroke="none")
    s += swatch(185, 833, "WHITE — Eye Shine  ×2", "#FFFFFF")

    # Nose: small brown oval
    s += el(350, 835, 16, 11, LBRN)
    s += swatch(350, 850, "BROWN — Nose", LBRN)

    s += preview_box()
    s += el(408,990,33,37,BRN);  s += circ(408,952,30,BRN)          # body + head
    s += el(408,980,32,15,CRM)                                        # collar
    s += pointed_oval(390,922,11,22,BRN); s += pointed_oval(426,922,11,22,BRN)  # ears
    s += pointed_oval(390,926,7,15,CRM);  s += pointed_oval(426,926,7,15,CRM)   # inner ears
    s += el(400,945,7,9,LBRN);   s += el(416,945,7,9,LBRN)          # eyes
    s += el(447,1005,11,16,BRN); s += el(447,1016,9,8,CRM)          # tail + tip
    return page("🍂 EEVEE — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# TOGEPI
# ══════════════════════════════════════════════════════════════════════════════

def togepi():
    CRM  = "#FFF8DC"
    YEL  = "#FFD84D"
    RED  = "#D93030"
    BLU  = "#4A8FD4"
    BLK  = "#1A1A1A"

    s = ""

    # ── ROW 1: large shapes ─────────────────────────────── y 70 – 470 ──
    s += row_label(77, "LARGE  (2.5-4\")  —  trace onto CREAM paper")

    # Egg body: egg shape ~2.5\"×4\"
    # Egg = upper half is a circle, lower half is wider
    ex, ey = 210, 290
    egg_d = (
        f"M {ex},{ey - 180} "                       # top
        f"C {ex + 120},{ey - 180} {ex + 140},{ey - 20} {ex + 140},{ey + 60} "   # right
        f"C {ex + 140},{ey + 160} {ex + 75},{ey + 200} {ex},{ey + 200} "        # bottom-right
        f"C {ex - 75},{ey + 200} {ex - 140},{ey + 160} {ex - 140},{ey + 60} "   # bottom-left
        f"C {ex - 140},{ey - 20} {ex - 120},{ey - 180} {ex},{ey - 180} Z"       # left
    )
    s += pth(egg_d, CRM)
    s += swatch(ex, ey + 204, "CREAM — Egg Body  (2.5\"×4\")", CRM)

    # Head: ~2.5\" circle
    hx, hy = 588, 262
    s += circ(hx, hy, 125, CRM)
    s += swatch(hx, hy + 129, "CREAM — Head  (2.5\" circle)", CRM)

    s += divider(478)

    # ── ROW 2: medium shapes ────────────────────────────── y 488 – 730 ──
    s += row_label(494, "MEDIUM  —  shell triangles (red × 3, blue × 3), head spikes (yellow × 3)")

    # Red triangles on egg: 3 triangles ~0.8\" tall
    red_tris = [
        [(80, 570), (120, 570), (100, 510)],
        [(175, 620), (215, 620), (195, 560)],
        [(80, 680), (120, 680), (100, 620)],
    ]
    for tri in red_tris:
        s += poly(tri, RED)
    s += swatch(145, 695, "RED — Shell Triangles  ×3", RED)

    # Blue triangles: 3 diamonds/triangles
    blue_tris = [
        [(140, 535), (180, 535), (160, 475)],
        [(225, 575), (265, 575), (245, 515)],
        [(140, 650), (180, 650), (160, 590)],
    ]
    for tri in blue_tris:
        s += poly(tri, BLU)
    s += swatch(270, 660, "BLUE — Shell Triangles  ×3", BLU)

    # Head spikes: 3 tiny yellow triangles
    for i, sx in enumerate([450, 510, 570]):
        s += poly([(sx - 14, 560), (sx + 14, 560), (sx, 510)], YEL)
    s += swatch(510, 575, "YELLOW — Head Spikes  ×3", YEL)

    # Eyes: black dots ~0.3\"
    s += circ(660, 560, 18, BLK)
    s += circ(720, 560, 18, BLK)
    s += swatch(690, 582, "BLACK — Eyes  ×2  (0.3\")", BLK)

    s += divider(742)

    # ── ROW 3: shell divider line + tiny shapes ──────────── y 752 – 1020 ──
    s += row_label(758, "SMALL  —  shell rim line, face details")

    # Shell rim: wavy line approximated as a long rounded rect strip
    # Just a thick arc to indicate the dividing line between head and shell
    s += rr(60, 800, 340, 22, 8, CRM)
    # Jagged edge suggestion — series of triangles along bottom of strip
    for i in range(8):
        xi = 68 + i * 42
        s += poly([(xi, 820), (xi + 20, 820), (xi + 10, 838)], CRM)
    s += swatch(230, 843, "CREAM — Shell Rim Strip  (trace & cut zigzag edge)", CRM)

    # Cheek blush circles
    s += circ(520, 820, 18, RED, opacity=0.5)
    s += circ(580, 820, 18, RED, opacity=0.5)
    s += el(520, 820, 18, 18, "none", RED, 1.5)
    s += el(580, 820, 18, 18, "none", RED, 1.5)
    s += swatch(550, 842, "RED (light) — Cheek Blush  ×2", RED)

    s += preview_box()
    s += el(408,998,28,42,CRM)                                        # egg body
    for i,(ex,ey) in enumerate([(397,1000),(408,978),(419,1000)]):
        s += poly([(ex-8,ey+10),(ex+8,ey+10),(ex,ey-10)], RED if i%2==0 else BLU)
    s += circ(408,944,24,CRM)                                         # head
    for sx in [400,408,416]: s += poly([(sx-5,940),(sx+5,940),(sx,927)],YEL)  # head spikes
    s += el(402,941,4,5,BLK); s += el(414,941,4,5,BLK)              # eyes
    return page("🥚 TOGEPI — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# SQUIRTLE  #007
# ══════════════════════════════════════════════════════════════════════════════

def squirtle():
    BLU  = "#4A8FD4"
    DBLU = "#2A5FA0"
    BRN  = "#9B7820"
    CRM  = "#FFF5DC"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-3.5\")  —  trace onto BLUE paper")

    bx, by = 205, 275
    s += circ(bx, by, 168, BLU)
    s += swatch(bx, by + 172, "BLUE — Body  (3.5\" circle)", BLU)

    hx, hy = 590, 258
    s += el(hx, hy, 145, 138, BLU)
    s += swatch(hx, hy + 142, "BLUE — Head  (3\")", BLU)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  shell (brown), plastron (cream), tail, cheek marks")

    s += el(185, 602, 138, 96, BRN)
    s += swatch(185, 702, "BROWN — Shell Dome  (2.5\"×2\")", BRN)

    s += el(385, 598, 78, 108, CRM)
    s += swatch(385, 710, "CREAM — Shell Front / Plastron  (1.5\"×2.2\")", CRM)

    # Curled tail
    tail = [(540, 575), (592, 548), (626, 586), (616, 642), (570, 666), (534, 640)]
    s += poly(tail, BLU)
    s += swatch(582, 672, "BLUE — Tail  (curled)", BLU)

    # Cheek lines: 3 short dark dashes per cheek
    for i in range(3):
        s += el(695 + i * 20, 600, 5, 18, DBLU)
        s += el(768 + i * 20, 600, 5, 18, DBLU)
    s += swatch(748, 624, "DARK BLUE — Cheek Lines  ×6  (3 per cheek)", DBLU)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes; note: draw curved lines on shell for hex pattern")

    s += el(105, 836, 28, 34, BLK)
    s += el(205, 836, 28, 34, BLK)
    s += swatch(155, 874, "BLACK — Eyes  ×2", BLK)

    s += preview_box()
    s += circ(408,990,37,BLU);  s += el(408,952,32,30,BLU)          # body + head
    s += el(408,990,26,20,BRN); s += el(408,990,13,22,CRM)          # shell dome + plastron
    s += el(400,945,6,8,BLK);   s += el(416,945,6,8,BLK)           # eyes
    s += poly([(434,979),(446,974),(451,991),(441,1004),(427,1001)],BLU)  # tail curl
    return page("💧 SQUIRTLE — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# CHIKORITA  #152
# ══════════════════════════════════════════════════════════════════════════════

def chikorita():
    LGN  = "#8FD46A"
    DGN  = "#3A7A2A"
    PINK = "#F4A0B0"
    CRM  = "#FFFACC"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-3.5\")  —  trace onto LIGHT GREEN paper")

    bx, by = 205, 278
    s += circ(bx, by, 168, LGN)
    s += swatch(bx, by + 172, "LIGHT GREEN — Body  (3.5\")", LGN)

    hx, hy = 590, 258
    s += el(hx, hy, 142, 138, LGN)
    s += swatch(hx, hy + 142, "LIGHT GREEN — Head  (3\")", LGN)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  big head leaf (dark green), collar leaves, belly")

    # Head leaf: large dark-green oval ~1.5\"×2.5\"
    s += el(185, 600, 74, 118, DGN)
    s += swatch(185, 722, "DARK GREEN — Head Leaf  (1.5\"×2.5\")", DGN)

    # Collar leaves: 3 smaller ovals
    for i, (cx, cy, rx, ry) in enumerate([(370, 570, 38, 58), (430, 600, 38, 58), (490, 570, 38, 58)]):
        s += el(cx, cy, rx, ry, DGN)
    s += swatch(430, 662, "DARK GREEN — Collar Leaves  ×3  (0.75\"×1.2\")", DGN)

    # Belly: cream oval
    s += el(650, 600, 88, 108, CRM)
    s += swatch(650, 712, "CREAM — Belly  (1.8\"×2.2\")", CRM)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes (pink/red)")

    s += el(105, 836, 26, 32, PINK)
    s += el(205, 836, 26, 32, PINK)
    s += swatch(155, 872, "PINK — Eyes  ×2", PINK)

    s += circ(105, 830, 12, BLK)
    s += circ(205, 830, 12, BLK)
    s += swatch(155, 847, "BLACK — Pupils  ×2", BLK)

    s += preview_box()
    s += el(408,990,38,34,LGN);  s += circ(408,953,30,LGN)          # body + head
    s += el(398,946,6,8,PINK);   s += el(420,946,6,8,PINK)          # eyes
    s += el(408,920,20,30,DGN)                                        # big head leaf
    for cx2 in [391,408,425]: s += el(cx2,958,8,14,DGN)             # collar leaves
    return page("🌿 CHIKORITA — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# CYNDAQUIL  #155
# ══════════════════════════════════════════════════════════════════════════════

def cyndaquil():
    NAVY = "#2A3870"
    CRM  = "#FDECC8"
    ORG  = "#E8732A"
    RED  = "#D93030"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-4\")  —  trace onto DARK BLUE / NAVY paper")

    # Body: hunched, wider at front
    bx, by = 205, 285
    s += el(bx, by, 178, 155, NAVY)
    s += swatch(bx, by + 159, "DARK NAVY — Body  (3.5\"×3\")", NAVY)

    hx, hy = 590, 265
    s += el(hx, hy, 130, 128, NAVY)
    s += swatch(hx, hy + 132, "DARK NAVY — Head  (2.7\")", NAVY)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  belly (cream), flames (orange), flame dots (red)")

    # Belly: large cream oval covering underside
    s += el(205, 610, 155, 108, CRM)
    s += swatch(205, 722, "CREAM — Belly  (3\"×2.2\")", CRM)

    # 4 flame teardrop shapes on back
    for i, (fx, fy) in enumerate([(430, 520), (490, 496), (550, 510), (610, 530)]):
        flame_d = (
            f"M {fx},{fy - 55} "
            f"C {fx + 30},{fy - 45} {fx + 32},{fy + 20} {fx},{fy + 30} "
            f"C {fx - 32},{fy + 20} {fx - 30},{fy - 45} {fx},{fy - 55} Z"
        )
        s += pth(flame_d, ORG)
    s += swatch(520, 562, "ORANGE — Flames  ×4  (teardrop shapes)", ORG)

    # 4 red dots (flame bases)
    for fx in [430, 490, 550, 610]:
        s += circ(fx, 580, 14, RED)
    s += swatch(520, 598, "RED — Flame Dots  ×4", RED)

    # Feet: small navy ovals
    s += el(660, 610, 38, 22, NAVY)
    s += el(740, 610, 38, 22, NAVY)
    s += swatch(700, 636, "DARK NAVY — Feet  ×2", NAVY)

    s += divider(742)
    s += row_label(758, "SMALL  —  closed eyes (black crescents), nose")

    # Eyes: closed crescent shapes
    cresc_d1 = f"M 80,830 C 82,810 128,810 130,830 C 128,820 82,820 80,830 Z"
    cresc_d2 = f"M 195,830 C 197,810 243,810 245,830 C 243,820 197,820 195,830 Z"
    s += pth(cresc_d1, BLK)
    s += pth(cresc_d2, BLK)
    s += swatch(162, 836, "BLACK — Closed Eyes  ×2  (crescent arcs)", BLK)

    s += circ(340, 828, 9, RED)
    s += swatch(340, 841, "RED — Nose", RED)

    s += preview_box()
    s += el(408,990,39,34,NAVY); s += el(408,990,27,23,CRM)         # body + belly
    s += el(408,953,28,27,NAVY)                                       # head
    for fx,fy in [(427,962),(437,957),(447,962),(457,970)]:
        s += el(fx,fy,6,11,ORG)                                       # back flames
    s += el(403,946,5,4,BLK);   s += el(413,946,5,4,BLK)           # closed eyes
    return page("🔥 CYNDAQUIL — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# TOTODILE  #158
# ══════════════════════════════════════════════════════════════════════════════

def totodile():
    BLU  = "#4A8FD4"
    YEL  = "#FFD84D"
    RED  = "#D93030"
    CRM  = "#F5F8E0"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-4\")  —  trace onto BLUE paper")

    bx, by = 205, 278
    s += el(bx, by, 158, 175, BLU)
    s += swatch(bx, by + 179, "BLUE — Body  (3\"×3.5\")", BLU)

    hx, hy = 590, 265
    # Head with wider jaw — taller ellipse
    s += el(hx, hy, 145, 155, BLU)
    s += swatch(hx, hy + 159, "BLUE — Head  (3\")", BLU)

    s += divider(478)
    s += row_label(494, "MEDIUM  —  belly stripe (yellow), back spines (red), teeth (cream)")

    # Belly: yellow oval with irregular edge to suggest zigzag/scale pattern
    s += el(205, 610, 112, 138, YEL)
    s += swatch(205, 752, "YELLOW — Belly  (2.3\"×2.8\")  [draw zigzag lines on it]", YEL)

    # Back spines: 3 red triangles
    spine_y = 500
    for i, sx in enumerate([440, 510, 580]):
        s += poly([(sx, spine_y - 55), (sx - 22, spine_y + 10), (sx + 22, spine_y + 10)], RED)
    s += swatch(510, 525, "RED — Back Spines  ×3", RED)

    # Teeth: small cream triangles in jaw area
    for i in range(5):
        tx2 = 630 + i * 28
        s += poly([(tx2, 630), (tx2 + 12, 630), (tx2 + 6, 650)], CRM)
    s += swatch(742, 656, "CREAM — Teeth  ×5", CRM)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes, claws")

    s += el(105, 836, 26, 30, BLK)
    s += el(195, 836, 26, 30, BLK)
    s += swatch(150, 870, "BLACK — Eyes  ×2", BLK)

    # Claw dots: 3 tiny cream ovals per hand
    for i in range(6):
        s += el(340 + i * 22, 838, 7, 12, CRM)
    s += swatch(450, 854, "CREAM — Claws  ×6  (3 per hand)", CRM)

    s += preview_box()
    s += el(408,990,35,38,BLU);  s += el(408,990,24,30,YEL)         # body + belly stripe
    s += el(408,951,32,34,BLU)                                        # head
    for sx2 in [397,408,419]: s += poly([(sx2-6,972),(sx2+6,972),(sx2,960)],RED)  # back spines
    s += el(400,944,6,7,BLK);   s += el(416,944,6,7,BLK)           # eyes
    return page("💦 TOTODILE — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# TREECKO  #252
# ══════════════════════════════════════════════════════════════════════════════

def treecko():
    DGN  = "#2E6E3A"
    LGN  = "#7BC96F"
    RED  = "#D93030"
    YEL  = "#FFD84D"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-4\")  —  trace onto DARK GREEN paper")

    bx, by = 205, 278
    s += el(bx, by, 145, 175, DGN)
    s += swatch(bx, by + 179, "DARK GREEN — Body  (3\"×3.5\")", DGN)

    hx, hy = 590, 255
    s += el(hx, hy, 142, 135, DGN)
    s += swatch(hx, hy + 139, "DARK GREEN — Head  (3\")", DGN)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  belly (light green), tail (dark green), eyes (red)")

    # Belly: lt-green oval
    s += el(205, 610, 100, 130, LGN)
    s += swatch(205, 744, "LIGHT GREEN — Belly  (2\"×2.7\")", LGN)

    # Tail: long thin oval
    s += el(430, 600, 55, 128, DGN)
    s += swatch(430, 732, "DARK GREEN — Tail  (1.1\"×2.6\")", DGN)

    # Eyes: red ovals
    s += el(620, 570, 30, 38, RED)
    s += el(710, 570, 30, 38, RED)
    s += swatch(665, 612, "RED — Eyes  ×2", RED)

    s += divider(742)
    s += row_label(758, "SMALL  —  pupils, toe pads (yellow)")

    s += circ(105, 836, 14, BLK)
    s += circ(195, 836, 14, BLK)
    s += swatch(150, 854, "BLACK — Pupils  ×2", BLK)

    # Toe pads: 3 per foot
    for i in range(6):
        s += circ(330 + i * 28, 836, 10, YEL)
    s += swatch(490, 850, "YELLOW — Toe Pads  ×6  (3 per foot)", YEL)

    s += preview_box()
    s += el(408,990,32,38,DGN);  s += el(408,988,22,26,LGN)         # body + belly
    s += el(408,952,31,29,DGN)                                        # head
    s += el(398,945,7,9,RED);    s += el(418,945,7,9,RED)            # eyes
    s += el(447,993,12,28,DGN)                                        # tail
    return page("🌲 TREECKO — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# TORCHIC  #255
# ══════════════════════════════════════════════════════════════════════════════

def torchic():
    ORG  = "#E8732A"
    YEL  = "#FFD84D"
    RED  = "#D93030"
    CRM  = "#FFF5DC"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-4\")  —  trace onto ORANGE paper")

    bx, by = 205, 278
    s += circ(bx, by, 182, ORG)
    s += swatch(bx, by + 186, "ORANGE — Body  (3.5\" round, fluffy)", ORG)

    hx, hy = 590, 258
    s += circ(hx, hy, 145, ORG)
    s += swatch(hx, hy + 149, "ORANGE — Head  (3\")", ORG)

    s += divider(478)
    s += row_label(494, "MEDIUM  —  head crest (red), belly (cream), beak (yellow), feet")

    # Head crest: red pointed feather
    s += pointed_oval(185, 562, 30, 72, RED)
    s += swatch(185, 638, "RED — Head Crest Feather  (0.6\"×1.5\")", RED)

    # Belly highlight: cream oval
    s += el(385, 600, 95, 118, CRM)
    s += swatch(385, 722, "CREAM — Belly  (2\"×2.4\")", CRM)

    # Beak: two yellow triangles (upper + lower)
    s += poly([(560, 570), (620, 570), (590, 612)], YEL)    # upper
    s += poly([(568, 614), (612, 614), (590, 638)], YEL)    # lower
    s += swatch(590, 644, "YELLOW — Beak  ×2  (upper & lower triangle)", YEL)

    # Feet: yellow rounded shapes
    s += el(700, 610, 42, 24, YEL)
    s += el(775, 618, 38, 22, YEL)
    s += swatch(738, 638, "YELLOW — Feet  ×2", YEL)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes")

    s += el(105, 836, 26, 32, BLK)
    s += el(205, 836, 26, 32, BLK)
    s += swatch(155, 872, "BLACK — Eyes  ×2", BLK)

    s += preview_box()
    s += circ(408,990,40,ORG);   s += el(408,988,28,20,CRM)         # body + belly
    s += circ(408,950,32,ORG)                                         # head
    s += el(408,926,7,15,RED)                                         # head crest
    s += poly([(404,957),(412,957),(408,966)],YEL)                   # beak
    s += el(400,946,5,7,BLK);   s += el(416,946,5,7,BLK)           # eyes
    return page("🔥 TORCHIC — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# MUDKIP  #258
# ══════════════════════════════════════════════════════════════════════════════

def mudkip():
    BLU  = "#7AB8E0"
    DBLU = "#3A6A9E"
    ORG  = "#E8732A"
    PINK = "#F4A0B0"
    CRM  = "#F5F0E0"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-4\")  —  trace onto BLUE paper")

    bx, by = 205, 278
    s += circ(bx, by, 175, BLU)
    s += swatch(bx, by + 179, "BLUE — Body  (3.5\")", BLU)

    hx, hy = 590, 262
    s += el(hx, hy, 148, 140, BLU)
    s += swatch(hx, hy + 144, "BLUE — Head  (3\")", BLU)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  head fin (ORANGE — very distinctive!), belly, cheek gills")

    # Head fin: LARGE orange crest — most distinctive feature
    fin_d = (
        f"M 185,556 "
        f"C 155,490 165,440 205,430 "
        f"C 240,420 260,460 255,510 "
        f"C 245,545 220,560 185,556 Z"
    )
    s += pth(fin_d, ORG)
    s += swatch(210, 568, "ORANGE — Head Fin  (1.5\"×1.3\")  KEY FEATURE", ORG)

    # Belly: cream oval
    s += el(415, 598, 88, 112, CRM)
    s += swatch(415, 714, "CREAM — Belly  (1.8\"×2.3\")", CRM)

    # Cheek gills: 3 pink dots each side
    for i in range(3):
        s += circ(580 + i * 24, 580, 14, PINK)
        s += circ(700 + i * 24, 580, 14, PINK)
    s += swatch(672, 598, "PINK — Cheek Gills  ×6  (3 per side)", PINK)

    # Tail fin: wide blue fan
    tail_pts = [(570, 640), (625, 610), (665, 640), (655, 690), (575, 690)]
    s += poly(tail_pts, BLU)
    s += swatch(618, 696, "BLUE — Tail Fan", BLU)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes")

    s += el(105, 836, 28, 32, BLK)
    s += el(205, 836, 28, 32, BLK)
    s += swatch(155, 872, "BLACK — Eyes  ×2", BLK)

    s += preview_box()
    s += circ(408,990,38,BLU);   s += el(408,988,26,18,CRM)         # body + belly
    s += el(408,952,33,31,BLU)                                        # head
    s += el(392,928,14,28,ORG)                                        # orange head fin (key feature)
    for gx in [388,396,404]: s += circ(gx,953,5,PINK)               # cheek gills
    s += el(400,946,6,7,BLK);   s += el(416,946,6,7,BLK)           # eyes
    return page("💦 MUDKIP — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# TURTWIG  #387
# ══════════════════════════════════════════════════════════════════════════════

def turtwig():
    GRN  = "#6DB846"
    LGN  = "#A8D870"
    BRN  = "#8B5828"
    DBRN = "#5A3818"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3\")  —  trace onto GREEN paper")

    bx, by = 205, 278
    s += el(bx, by, 158, 148, GRN)
    s += swatch(bx, by + 152, "GREEN — Body  (3\")", GRN)

    hx, hy = 590, 262
    s += el(hx, hy, 130, 125, GRN)
    s += swatch(hx, hy + 129, "GREEN — Head  (2.7\")", GRN)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  shell (brown), belly (light green), head twig + sprout")

    # Shell: brown dome oval
    s += el(205, 598, 142, 102, BRN)
    s += swatch(205, 704, "BROWN — Shell  (3\"×2\")", BRN)

    # Belly underside: light green
    s += el(205, 648, 115, 58, LGN)
    s += swatch(205, 710, "LIGHT GREEN — Belly strip", LGN)

    # Head twig: brown stick + small green sprout leaf
    s += rr(572, 490, 14, 60, 4, DBRN)    # brown stick
    s += swatch(579, 554, "DARK BROWN — Head Twig stick", DBRN)

    s += el(579, 476, 28, 40, GRN)         # green sprout
    s += swatch(579, 520, "GREEN — Sprout leaf", GRN)

    # Shell segments: draw hint lines on shell
    s += swatch(430, 598, "BROWN — draw dividing lines on shell for segments", BRN)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes")

    s += el(105, 836, 24, 28, BLK)
    s += el(195, 836, 24, 28, BLK)
    s += swatch(150, 868, "BLACK — Eyes  ×2", BLK)

    s += preview_box()
    s += el(408,990,35,32,GRN);  s += el(408,990,30,20,BRN)         # body + shell
    s += el(408,952,29,27,GRN)                                        # head
    s += rr(406,922,4,14,2,DBRN)                                     # twig stick
    s += el(408,919,7,9,GRN)                                          # sprout leaf
    s += el(400,946,5,7,BLK);   s += el(416,946,5,7,BLK)           # eyes
    return page("🌿 TURTWIG — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# CHIMCHAR  #390
# ══════════════════════════════════════════════════════════════════════════════

def chimchar():
    ORG  = "#E8732A"
    CRM  = "#FDECC8"
    BRN  = "#5A3818"
    DBLU = "#3A4A8F"
    RED  = "#D93030"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3\")  —  trace onto ORANGE paper")

    bx, by = 205, 278
    s += circ(bx, by, 152, ORG)
    s += swatch(bx, by + 156, "ORANGE — Body  (3\")", ORG)

    hx, hy = 590, 258
    s += circ(hx, hy, 138, ORG)
    s += swatch(hx, hy + 142, "ORANGE — Head  (2.8\")", ORG)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  face (cream), hair tufts (brown), flame (blue base + orange/red)")

    # Face: cream oval
    s += el(205, 598, 110, 128, CRM)
    s += swatch(205, 730, "CREAM — Face  (2.3\"×2.7\")", CRM)

    # Hair tufts: 3 dark brown pointed ovals
    s += pointed_oval(430, 545, 22, 52, BRN)
    s += pointed_oval(480, 528, 22, 52, BRN)
    s += pointed_oval(530, 545, 22, 52, BRN)
    s += swatch(480, 602, "DARK BROWN — Hair Tufts  ×3", BRN)

    # Flame base: blue oval on butt area
    s += el(660, 605, 50, 38, DBLU)
    s += swatch(660, 647, "DARK BLUE — Flame Base", DBLU)

    # Flame: orange teardrop
    flame_d = (
        f"M 660,560 "
        f"C 690,548 712,578 700,610 "
        f"C 688,638 640,638 628,610 "
        f"C 616,578 638,548 660,560 Z"
    )
    s += pth(flame_d, ORG)
    # Flame tip: red
    tip_d = (
        f"M 660,560 "
        f"C 675,555 688,570 682,585 "
        f"C 672,600 648,600 638,585 "
        f"C 632,570 645,555 660,560 Z"
    )
    s += pth(tip_d, RED)
    s += swatch(660, 570, "ORANGE + RED tip — Tail Flame", ORG)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes")

    s += el(105, 836, 24, 28, BLK)
    s += el(195, 836, 24, 28, BLK)
    s += swatch(150, 868, "BLACK — Eyes  ×2", BLK)

    s += preview_box()
    s += circ(408,990,33,ORG);   s += el(408,988,23,27,CRM)         # body + face
    s += circ(408,952,30,ORG)                                         # head
    for hx in [400,408,416]: s += el(hx,926,5,11,BRN)               # hair tufts
    s += circ(447,1003,9,DBLU);  s += circ(447,994,8,ORG); s += circ(447,989,5,RED)  # tail flame
    s += el(400,946,5,7,BLK);   s += el(416,946,5,7,BLK)           # eyes
    return page("🔥 CHIMCHAR — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# PIPLUP  #393
# ══════════════════════════════════════════════════════════════════════════════

def piplup():
    DBLU = "#3A5A9F"
    LBLU = "#7AAAD4"
    YEL  = "#FFD84D"
    WHT  = "#F8FBFF"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3\")  —  trace onto DARK BLUE paper")

    bx, by = 205, 278
    s += el(bx, by, 148, 162, DBLU)
    s += swatch(bx, by + 166, "DARK BLUE — Body  (3\")", DBLU)

    hx, hy = 590, 258
    s += circ(hx, hy, 138, DBLU)
    s += swatch(hx, hy + 142, "DARK BLUE — Head  (2.8\")", DBLU)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  face (light blue), belly (white), beak (yellow), feet, head dots")

    # Face: large light-blue oval
    s += el(205, 600, 110, 138, LBLU)
    s += swatch(205, 742, "LIGHT BLUE — Face  (2.3\"×2.8\")", LBLU)

    # Belly: white oval
    s += el(205, 645, 75, 95, WHT)
    s += swatch(205, 744, "WHITE — Belly", WHT)

    # Beak: short yellow triangle
    s += poly([(550, 580), (610, 580), (580, 618)], YEL)
    s += swatch(580, 624, "YELLOW — Beak  (short triangle)", YEL)

    # Head dots: 2 small lt-blue circles
    s += circ(685, 548, 18, LBLU)
    s += circ(735, 548, 18, LBLU)
    s += swatch(710, 570, "LIGHT BLUE — Head Dots  ×2", LBLU)

    # Feet: yellow rounded shapes
    s += el(680, 632, 38, 20, YEL)
    s += el(755, 632, 38, 20, YEL)
    s += swatch(718, 656, "YELLOW — Feet  ×2", YEL)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes")

    s += el(105, 836, 26, 30, BLK)
    s += el(205, 836, 26, 30, BLK)
    s += swatch(155, 870, "BLACK — Eyes  ×2", BLK)

    s += preview_box()
    s += el(408,990,33,36,DBLU); s += el(408,980,22,28,LBLU)        # body + face panel
    s += el(408,990,14,20,WHT)                                        # belly
    s += circ(408,952,30,DBLU);  s += el(408,948,20,24,LBLU)        # head + face
    s += poly([(404,956),(412,956),(408,964)],YEL)                   # beak
    s += el(400,946,5,7,BLK);   s += el(416,946,5,7,BLK)           # eyes
    return page("🐧 PIPLUP — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# SNIVY  #495
# ══════════════════════════════════════════════════════════════════════════════

def snivy():
    DGN  = "#2E6E3A"
    LGN  = "#88C870"
    YEL  = "#E8D870"
    RED  = "#D93030"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (2.5-3\")  —  trace onto DARK GREEN paper")

    bx, by = 205, 278
    s += el(bx, by, 130, 155, DGN)
    s += swatch(bx, by + 159, "DARK GREEN — Body  (2.7\"×3.2\")", DGN)

    hx, hy = 590, 258
    s += el(hx, hy, 132, 125, DGN)
    s += swatch(hx, hy + 129, "DARK GREEN — Head  (2.7\")", DGN)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  belly stripe (cream/yellow), tail + leaf fan, collar leaves")

    # Belly stripe: cream-yellow long oval
    s += el(205, 605, 78, 132, YEL)
    s += swatch(205, 741, "CREAM-YELLOW — Belly Stripe  (1.6\"×2.7\")", YEL)

    # Tail: long thin dark-green
    s += el(415, 598, 38, 135, DGN)
    s += swatch(415, 737, "DARK GREEN — Tail  (0.8\"×2.8\")", DGN)

    # Leaf fan at tail tip: 3 small leaf ovals
    for i, (lx, ly) in enumerate([(470, 500), (510, 480), (550, 500)]):
        s += el(lx, ly, 28, 48, LGN)
    s += swatch(510, 552, "LIGHT GREEN — Tail Leaf Fan  ×3", LGN)

    # Collar leaves: 2 small ovals
    s += el(670, 560, 24, 42, LGN)
    s += el(720, 560, 24, 42, LGN)
    s += swatch(695, 606, "LIGHT GREEN — Collar Leaves  ×2", LGN)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes (red), pupils")

    s += el(105, 836, 26, 30, RED)
    s += el(200, 836, 26, 30, RED)
    s += swatch(152, 870, "RED — Eyes  ×2", RED)

    s += circ(105, 832, 12, BLK)
    s += circ(200, 832, 12, BLK)
    s += swatch(152, 848, "BLACK — Pupils  ×2", BLK)

    s += preview_box()
    s += el(408,990,29,34,DGN);  s += el(408,987,18,24,YEL)         # body + belly stripe
    s += el(408,953,29,27,DGN)                                        # head
    s += el(398,946,6,8,RED);    s += el(418,946,6,8,RED)            # eyes
    s += el(447,1002,10,20,DGN); s += el(447,980,12,14,LGN)         # tail + leaf fan
    return page("🍃 SNIVY — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# TEPIG  #498
# ══════════════════════════════════════════════════════════════════════════════

def tepig():
    ORG  = "#E06030"
    CRM  = "#FDECC8"
    RED  = "#D93030"
    YEL  = "#FFD84D"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3-3.5\")  —  trace onto ORANGE-RED paper")

    bx, by = 205, 278
    s += circ(bx, by, 172, ORG)
    s += swatch(bx, by + 176, "ORANGE-RED — Body  (3.5\")", ORG)

    hx, hy = 590, 258
    s += circ(hx, hy, 145, ORG)
    s += swatch(hx, hy + 149, "ORANGE-RED — Head  (3\")", ORG)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  snout (cream, BIG round), belly (cream), ears, tail")

    # Snout: cream large round circle
    s += circ(205, 598, 115, CRM)
    s += swatch(205, 717, "CREAM — Snout  (2.4\" round circle)  KEY FEATURE", CRM)

    # Belly: cream oval
    s += el(420, 600, 88, 112, CRM)
    s += swatch(420, 716, "CREAM — Belly  (1.8\"×2.3\")", CRM)

    # Ears: orange with yellow inside
    s += pointed_oval(600, 545, 38, 65, ORG)
    s += pointed_oval(680, 545, 38, 65, ORG)
    s += pointed_oval(600, 550, 22, 46, YEL)
    s += pointed_oval(680, 550, 22, 46, YEL)
    s += swatch(640, 614, "ORANGE + YELLOW inner — Ears  ×2", ORG)

    # Tail: curled orange strip with black tip
    tail_d = (
        f"M 760,560 C 800,540 820,590 800,620 "
        f"C 785,642 760,638 755,618 "
        f"C 750,598 768,590 776,604 "
    )
    s += pth(tail_d, ORG)
    s += circ(775, 607, 12, BLK)
    s += swatch(790, 645, "ORANGE + BLACK tip — Tail", ORG)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes, nostrils (red dots on snout)")

    s += el(105, 836, 25, 28, BLK)
    s += el(200, 836, 25, 28, BLK)
    s += swatch(152, 868, "BLACK — Eyes  ×2", BLK)

    s += circ(340, 836, 10, RED)
    s += circ(375, 836, 10, RED)
    s += swatch(358, 850, "RED — Nostrils  ×2  (place on snout)", RED)

    s += preview_box()
    s += circ(408,990,38,ORG);   s += circ(408,952,32,ORG)          # body + head
    s += el(408,958,18,14,CRM);  s += el(408,990,25,16,CRM)         # snout + belly
    s += circ(404,957,4,RED);    s += circ(412,957,4,RED)            # nostrils
    s += poly([(439,976),(449,970),(454,981),(446,990),(438,987)],ORG)  # tail
    s += circ(439,988,5,BLK)                                          # tail tip
    s += el(400,946,5,7,BLK);   s += el(416,946,5,7,BLK)           # eyes
    return page("🐷 TEPIG — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# OSHAWOTT  #501
# ══════════════════════════════════════════════════════════════════════════════

def oshawott():
    LBLU = "#7ACCE8"
    DBLU = "#2A4A7E"
    CRM  = "#FFF5DC"
    BRN  = "#8B6028"
    PINK = "#F4B0B0"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3\")  —  trace onto LIGHT BLUE paper")

    bx, by = 205, 278
    s += circ(bx, by, 152, LBLU)
    s += swatch(bx, by + 156, "LIGHT BLUE — Body  (3\")", LBLU)

    hx, hy = 590, 258
    s += circ(hx, hy, 138, LBLU)
    s += swatch(hx, hy + 142, "LIGHT BLUE — Head  (2.8\")", LBLU)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  face (cream), belly (cream), scalchop (brown), ears (dark blue)")

    # Face: large cream oval
    s += el(205, 600, 112, 132, CRM)
    s += swatch(205, 736, "CREAM — Face  (2.3\"×2.7\")", CRM)

    # Belly: cream oval
    s += el(420, 600, 88, 110, CRM)
    s += swatch(420, 714, "CREAM — Belly  (1.8\"×2.3\")", CRM)

    # Scalchop: brown scallop shell on belly
    scalchop_d = (
        f"M 420,548 "
        f"C 456,548 480,572 480,600 "
        f"C 480,626 456,648 420,648 "
        f"C 384,648 360,626 360,600 "
        f"C 360,572 384,548 420,548 Z"
    )
    s += pth(scalchop_d, BRN)
    # Scallop ridges
    for i in range(3):
        angle = -30 + i * 30
        import math
        rx2 = 56 + i * 0
        s += el(420, 598, 55 - i*12, 50 - i*14, "none", BRN, 1.5)
    s += swatch(420, 652, "BROWN — Scalchop  (scallop on belly)", BRN)

    # Ears: dark navy pointed ovals
    s += pointed_oval(600, 548, 28, 55, DBLU)
    s += pointed_oval(680, 548, 28, 55, DBLU)
    s += swatch(640, 607, "DARK BLUE — Ears  ×2", DBLU)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes, nose")

    s += el(105, 836, 25, 30, BLK)
    s += el(198, 836, 25, 30, BLK)
    s += swatch(152, 870, "BLACK — Eyes  ×2", BLK)

    s += circ(330, 834, 10, PINK)
    s += swatch(330, 848, "PINK — Nose", PINK)

    s += preview_box()
    s += circ(408,990,33,LBLU);  s += el(408,988,22,28,CRM)         # body + face
    s += circ(408,952,30,LBLU);  s += el(408,948,20,25,CRM)         # head + face
    s += circ(408,990,12,BRN)                                         # scalchop
    s += pointed_oval(390,931,6,13,DBLU); s += pointed_oval(426,931,6,13,DBLU)  # ears
    s += el(400,946,5,7,BLK);   s += el(416,946,5,7,BLK)           # eyes
    return page("🌊 OSHAWOTT — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# CHESPIN
# ══════════════════════════════════════════════════════════════════════════════

def chespin():
    BRN  = "#8B6028"
    DGN  = "#2E6E2E"
    GRN  = "#5A9040"
    CRM  = "#FFF5DC"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3\")  —  lower body BROWN, head/helmet DARK GREEN")

    # Lower body: brown round
    bx, by = 205, 300
    s += el(bx, by, 148, 148, BRN)
    s += swatch(bx, by + 152, "BROWN — Lower Body  (3\")", BRN)

    # Head dome/helmet: dark green
    hx, hy = 590, 258
    s += circ(hx, hy, 138, DGN)
    s += swatch(hx, hy + 142, "DARK GREEN — Head / Helmet  (2.8\")", DGN)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  face (cream), spikes (green), belly (cream)")

    # Face: cream oval inside green helmet
    s += el(205, 598, 105, 128, CRM)
    s += swatch(205, 730, "CREAM — Face / Belly  (2.2\"×2.7\")", CRM)

    # Spikes on head: 5 green triangular points
    spike_bases_y = 505
    for i, sx in enumerate([520, 558, 596, 634, 672]):
        tip_y = spike_bases_y - 55 - (15 if i == 2 else 5 if i in [1, 3] else 0)
        s += poly([(sx - 18, spike_bases_y), (sx + 18, spike_bases_y), (sx, tip_y)], GRN)
    s += swatch(596, 520, "GREEN — Head Spikes  ×5", GRN)

    # Arms/paws: brown ovals
    s += el(700, 598, 38, 26, BRN)
    s += el(775, 604, 35, 24, BRN)
    s += swatch(738, 634, "BROWN — Paws  ×2", BRN)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes, nose")

    s += el(105, 836, 24, 28, BLK)
    s += el(198, 836, 24, 28, BLK)
    s += swatch(152, 868, "BLACK — Eyes  ×2", BLK)

    s += circ(335, 834, 10, BLK)
    s += swatch(335, 848, "BLACK — Nose", BLK)

    s += preview_box()
    s += el(408,995,33,32,BRN)                                        # brown lower body
    s += circ(408,952,30,DGN);   s += el(408,960,22,25,CRM)         # green head + cream face
    for sx2 in [394,401,408,415,422]: s += poly([(sx2-5,940),(sx2+5,940),(sx2,927)],GRN)
    s += el(400,957,5,7,BLK);   s += el(416,957,5,7,BLK)           # eyes
    return page("🌰 CHESPIN — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# FENNEKIN
# ══════════════════════════════════════════════════════════════════════════════

def fennekin():
    YEL  = "#FFD84D"
    ORG  = "#E87040"
    CRM  = "#FFF5DC"
    BRN  = "#7A4018"
    REYE = "#8B3020"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3\")  —  trace onto YELLOW paper")

    bx, by = 205, 278
    s += el(bx, by, 142, 155, YEL)
    s += swatch(bx, by + 159, "YELLOW — Body  (3\"×3.2\")", YEL)

    hx, hy = 590, 258
    s += circ(hx, hy, 138, YEL)
    s += swatch(hx, hy + 142, "YELLOW — Head  (2.8\")", YEL)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  tall ears (yellow + orange inside), chest fluff (cream), tail")

    # Ears: tall pointed yellow ovals
    s += pointed_oval(465, 548, 38, 90, YEL)
    s += pointed_oval(555, 548, 38, 90, YEL)
    # Ear interiors: orange
    s += pointed_oval(465, 554, 24, 68, ORG)
    s += pointed_oval(555, 554, 24, 68, ORG)
    s += swatch(510, 642, "YELLOW outer + ORANGE inner — Ears  ×2  (1.5\"×1.8\")", YEL)

    # Chest fluff: cream oval
    s += el(185, 600, 105, 128, CRM)
    s += swatch(185, 732, "CREAM — Chest Fluff  (2.2\"×2.7\")", CRM)

    # Tail: yellow wide oval with orange tip
    s += el(720, 598, 65, 105, YEL)
    s += el(720, 672, 58, 40, ORG)
    s += swatch(720, 715, "YELLOW + ORANGE tip — Tail", YEL)

    s += divider(742)
    s += row_label(758, "SMALL  —  eyes (dark red-brown), nose")

    s += el(105, 836, 26, 30, REYE)
    s += el(200, 836, 26, 30, REYE)
    s += swatch(152, 870, "DARK RED — Eyes  ×2", REYE)

    s += circ(105, 830, 12, BLK)
    s += circ(200, 830, 12, BLK)
    s += swatch(152, 848, "BLACK — Pupils  ×2", BLK)

    s += circ(340, 835, 9, BRN)
    s += swatch(340, 848, "BROWN — Nose", BRN)

    s += preview_box()
    s += el(408,990,31,34,YEL);  s += el(408,986,20,24,CRM)         # body + chest fluff
    s += circ(408,952,30,YEL)                                         # head
    s += pointed_oval(390,918,8,20,YEL); s += pointed_oval(426,918,8,20,YEL)  # ears
    s += pointed_oval(390,921,5,14,ORG); s += pointed_oval(426,921,5,14,ORG)  # ear interior
    s += el(447,1002,14,24,YEL); s += el(447,1020,12,9,ORG)         # tail + tip
    s += el(400,946,6,8,REYE);   s += el(416,946,6,8,REYE)          # eyes
    return page("🦊 FENNEKIN — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# FROAKIE
# ══════════════════════════════════════════════════════════════════════════════

def froakie():
    BLU  = "#5A90C8"
    DBLU = "#2A4A7E"
    WHT  = "#F0F8FF"
    CRM  = "#FFF5DC"
    PINK = "#F4A0A0"
    BLK  = "#1A1A1A"

    s = ""
    s += row_label(77, "LARGE  (3\")  —  trace onto BLUE paper")

    bx, by = 205, 278
    s += circ(bx, by, 152, BLU)
    s += swatch(bx, by + 156, "BLUE — Body  (3\")", BLU)

    # Head: slightly larger, rounder
    hx, hy = 590, 255
    s += circ(hx, hy, 145, BLU)
    s += swatch(hx, hy + 149, "BLUE — Head  (3\")", BLU)

    s += divider(468)
    s += row_label(486, "MEDIUM  —  frubbles/foam (white), belly (cream), back stripe (dark blue)")

    # Frubble foam on chest: white fluffy oval
    s += el(205, 590, 118, 105, WHT)
    s += swatch(205, 699, "WHITE — Chest Frubbles / Foam  (2.5\"×2.2\")", WHT)

    # Back frubble: white oval (on back of puppet, smaller)
    s += el(430, 580, 80, 70, WHT)
    s += swatch(430, 654, "WHITE — Back Frubbles  (1.6\"×1.4\")", WHT)

    # Belly: cream
    s += el(205, 620, 80, 72, CRM)
    s += swatch(205, 696, "CREAM — Belly  (under frubbles)", CRM)

    # Back dark stripe
    s += el(620, 580, 50, 108, DBLU)
    s += swatch(620, 692, "DARK BLUE — Back  (1\"×2.2\")", DBLU)

    # Eyes: large bulging (cream whites with big black pupils)
    s += circ(720, 558, 38, WHT)
    s += circ(785, 558, 38, WHT)
    s += circ(725, 555, 24, BLK)
    s += circ(790, 555, 24, BLK)
    s += swatch(752, 600, "WHITE outer + BLACK pupil — Eyes  ×2  (large/bulging)", WHT)

    s += divider(742)
    s += row_label(758, "SMALL  —  nose bump")

    s += circ(155, 835, 14, PINK)
    s += swatch(155, 853, "PINK — Nose bump", PINK)

    s += preview_box()
    s += circ(408,990,33,BLU);   s += circ(408,952,32,BLU)          # body + head
    s += el(408,982,26,18,WHT);  s += el(408,952,18,16,WHT)         # chest + back frubbles
    s += el(408,988,18,12,CRM)                                        # belly
    s += circ(393,944,11,WHT);   s += circ(421,944,11,WHT)          # eye whites
    s += circ(395,943,7,BLK);    s += circ(423,943,7,BLK)           # pupils
    return page("🐸 FROAKIE — Puppet Template", s)


# ══════════════════════════════════════════════════════════════════════════════
# Write all files
# ══════════════════════════════════════════════════════════════════════════════

files = {
    # Gen I
    "pikachu.svg":    pikachu(),
    "bulbasaur.svg":  bulbasaur(),
    "charmander.svg": charmander(),
    "squirtle.svg":   squirtle(),
    # Gen I puppet-set originals
    "jigglypuff.svg": jigglypuff(),
    "eevee.svg":      eevee(),
    "togepi.svg":     togepi(),
    # Gen II
    "chikorita.svg":  chikorita(),
    "cyndaquil.svg":  cyndaquil(),
    "totodile.svg":   totodile(),
    # Gen III
    "treecko.svg":    treecko(),
    "torchic.svg":    torchic(),
    "mudkip.svg":     mudkip(),
    # Gen IV
    "turtwig.svg":    turtwig(),
    "chimchar.svg":   chimchar(),
    "piplup.svg":     piplup(),
    # Gen V
    "snivy.svg":      snivy(),
    "tepig.svg":      tepig(),
    "oshawott.svg":   oshawott(),
    # Gen VI
    "chespin.svg":    chespin(),
    "fennekin.svg":   fennekin(),
    "froakie.svg":    froakie(),
}

for fname, content in files.items():
    path = os.path.join(OUT, fname)
    with open(path, "w") as f:
        f.write(content)
    print(f"✓  {path}")

print(f"\nAll templates written to:  {OUT}")
print("Open in a browser or any SVG viewer, then print at 100%.")

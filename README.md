# Pokemon Paper Puppet Templates

> **Work in progress!** The templates are functional but not perfect — some shapes are still being refined to better match the official Pokemon designs. Contributions are very welcome: if you improve a shape, add a new Pokemon, or have ideas for making the craft more kid-friendly, please open a PR or issue!

A Python script that generates printable SVG tracing sheets for Pokemon paper stick puppets. Print the sheets, cut out the shapes, trace them onto colored cardstock, cut again, and layer everything onto a craft stick.

---

## How it works

`generate_templates.py` builds one SVG file per Pokemon and writes them all to the `templates/` folder.

Each template is a US Letter page (8.5" × 11") laid out in three rows:

| Row | Content |
|-----|---------|
| **Large** | Body and head shapes (3–4") |
| **Medium** | Details — belly, ears, tails, special features |
| **Small** | Eyes, pupils, tiny accents |

At the bottom of every page is a small assembled preview showing roughly how the pieces look when stacked together.

Every shape is color-coded and labeled with the paper color to use. The scale is **96 px = 1 inch** — print at 100% (no scaling) and the sizes will be right.

---

## Craft instructions

### What you need
- Printed templates
- Colored cardstock or construction paper (one sheet per color per Pokemon)
- Scissors
- Craft sticks (popsicle sticks)
- Glue or double-sided tape
- Optional: googly eyes, markers for details

### Steps
1. **Print** the template page at 100% on regular paper.
2. **Cut out** each shape from the printed page to use as a cardboard stencil — or trace the outlines directly onto cardboard first for a sturdier stencil.
3. **Trace** each shape onto the matching color paper indicated on the label.
4. **Cut** out all the colored paper pieces.
5. **Layer** the pieces in order (large shapes first, details on top) and glue them together.
6. **Attach** the assembled puppet to a craft stick at the bottom.

---

## Generating the templates

Requires Python 3 — no external libraries needed.

```bash
python3 generate_templates.py
```

SVGs are written to `templates/`. Open any file in a browser to preview before printing.

---

## Pokemon included

### Gen I
`pikachu` · `bulbasaur` · `charmander` · `squirtle` · `jigglypuff` · `eevee` · `togepi`

### Gen II
`chikorita` · `cyndaquil` · `totodile`

### Gen III
`treecko` · `torchic` · `mudkip`

### Gen IV
`turtwig` · `chimchar` · `piplup`

### Gen V
`snivy` · `tepig` · `oshawott`

### Gen VI
`chespin` · `fennekin` · `froakie`

---

## Contributing

The shapes are built with SVG path primitives (ellipses, polygons, and cubic bezier curves) inside one Python function per Pokemon. If you want to improve a template:

1. Open `generate_templates.py` and find the function for the Pokemon you want to fix (e.g. `def charmander():`).
2. Edit the shapes — each one is a call to a helper like `el()` (ellipse), `circ()` (circle), `poly()` (polygon), `pth()` (path), or `leaf_path()` (organic leaf bezier).
3. Run `python3 generate_templates.py` to regenerate the SVGs.
4. Open the SVG in a browser to check the result.
5. Open a PR with your changes.

### Helper reference

| Function | Description |
|----------|-------------|
| `el(cx, cy, rx, ry, fill)` | Ellipse |
| `circ(cx, cy, r, fill)` | Circle |
| `poly([(x,y),...], fill)` | Polygon |
| `pth(d, fill)` | Arbitrary SVG path |
| `leaf_path(bx, by, tx, ty, hw, fill)` | Organic leaf shape via bezier (base → tip, hw = half-width) |
| `pointed_oval(cx, cy, rx, ry, fill)` | Ellipse with a pointed tip, used for ears |
| `swatch(cx, y, label, color)` | Color label badge placed below a shape |
| `preview_box()` | The assembled preview section at the bottom of the page |

### Scale
96 px = 1 inch. The page is 816 × 1056 px (8.5" × 11").

#!/usr/bin/env python3
"""Genera assets/favicon.svg desde un mapa de pixeles.

Candado en pixel-art: el tema del deck (auth) dibujado en la retícula PETSCII
del C64. Rejilla de 16x16 para que caiga en pixeles enteros a 16px de tab.
  #  = trazo (blanco roto)
  .  = fondo (negro cálido)
"""

import pathlib

VOID = "#1a1a17"
BRIGHT = "#e9e7de"

# 16x16. Arco de 2px, cuerpo macizo y ojo de cerradura calado.
ART = """
................
................
.....######.....
.....##..##.....
.....##..##.....
.....##..##.....
.....##..##.....
..############..
..############..
..####....####..
..####....####..
..#####..#####..
..#####..#####..
..############..
................
................
"""


def build() -> str:
    rows = [r for r in ART.strip("\n").split("\n")]
    assert len(rows) == 16, len(rows)
    assert all(len(r) == 16 for r in rows), [len(r) for r in rows]

    # Une pixeles contiguos de cada fila en un solo <rect>: menos nodos y
    # sin costuras entre rectangulos adyacentes al escalar.
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < 16:
            if row[x] == "#":
                run = 0
                while x + run < 16 and row[x + run] == "#":
                    run += 1
                rects.append(f'<rect x="{x}" y="{y}" width="{run}" height="1"/>')
                x += run
            else:
                x += 1

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" '
        'shape-rendering="crispEdges">'
        f'<rect width="16" height="16" fill="{VOID}"/>'
        f'<g fill="{BRIGHT}">' + "".join(rects) + "</g>"
        "</svg>"
    )


out = pathlib.Path(__file__).parent.parent / "assets" / "favicon.svg"
svg = build()
out.write_text(svg, encoding="utf-8")
print(f"favicon.svg -> {len(svg)} bytes")

# Vista previa en ASCII: nada de bloques Unicode, que revientan en consolas
# que no son UTF-8 (la de Windows, sin ir mas lejos).
for row in ART.strip("\n").split("\n"):
    print("  " + row.replace("#", "[]").replace(".", "  "))

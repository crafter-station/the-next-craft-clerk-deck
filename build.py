#!/usr/bin/env python3
"""Inlina los SVG oficiales en la plantilla y escribe deck.html.

Los logos viven como archivos sueltos en assets/ para poder actualizarlos
desde la fuente original. Este script los normaliza a currentColor (el deck
es B&N estricto) y los pega en la plantilla, para que deck.html quede
autocontenido: un solo archivo que se abre o se publica sin dependencias.

Uso:  python build.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

# Fills de marca → currentColor. El amarillo de Crafter (#F8BB2D) también:
# DESIGN.md manda B&N estricto, los logos van en escala de grises.
BRAND_FILLS = ("white", "#fff", "#FFF", "#ffffff", "#000", "#F8BB2D")


def load_svg(name: str, keep: range | None = None) -> str:
    """Devuelve el <svg> listo para inlinear.

    keep: índices de <path> a conservar (para recortar un logo compuesto).
    """
    svg = (ASSETS / name).read_text(encoding="utf-8").strip()

    if keep is not None:
        head = svg[: svg.index(">") + 1]
        paths = re.findall(r"<path\b[^>]*?/>", svg)
        svg = head + "".join(paths[i] for i in keep) + "</svg>"

    # Que herede el color del contenedor en vez de imponer el de marca.
    for fill in BRAND_FILLS:
        svg = svg.replace(f'fill="{fill}"', 'fill="currentColor"')

    # Escala con el contenedor: el tamaño lo fija el CSS, no el atributo.
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    svg = svg.replace("<svg", '<svg aria-hidden="true" focusable="false"', 1)

    return svg


def load_icon(slug: str) -> str:
    """Marca de 24x24 de assets/icons/ (simple-icons), lista para inlinear.

    Vienen sin atributo fill (o sea, negro): hay que forzar currentColor para
    que hereden el color del deck. El <title> se quita porque la etiqueta
    accesible la pone el contenedor, y si no el navegador lo muestra
    como tooltip.
    """
    svg = (ASSETS / "icons" / f"{slug}.svg").read_text(encoding="utf-8").strip()

    svg = re.sub(r"<title>.*?</title>", "", svg, flags=re.DOTALL)
    svg = svg.replace("<svg", '<svg fill="currentColor" aria-hidden="true"', 1)
    svg = svg.replace('role="img"', "", 1)

    return svg


def build() -> None:
    template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

    # %%ICON:react%% -> el SVG de assets/icons/react.svg
    template = re.sub(
        r"%%ICON:([a-z0-9]+)%%",
        lambda m: load_icon(m.group(1)),
        template,
    )

    # clerk.svg trae marca (paths 5-7) y wordmark (paths 0-4) en un mismo
    # viewBox de 441×128. El lockup de portada usa el logo completo.
    parts = {
        "%%CLERK_WORDMARK%%": load_svg("clerk-logo.svg"),
        "%%CLERK_MARK%%": load_svg("clerk-logo.svg", keep=range(5, 8)),
        "%%CRAFTER%%": load_svg("crafter-logo.svg"),
        "%%NEXT%%": load_svg("next-logo.svg"),
    }

    for token, svg in parts.items():
        if token in template:
            template = template.replace(token, svg)

    missing = re.findall(r"%%[A-Z_]+%%", template)
    if missing:
        raise SystemExit(f"Placeholders sin resolver: {sorted(set(missing))}")

    # index.html y no deck.html: GitHub Pages sirve la raiz por ese nombre
    out = ROOT / "index.html"
    out.write_text(template, encoding="utf-8")
    print(f"index.html -> {out.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()

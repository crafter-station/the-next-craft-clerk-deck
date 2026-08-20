#!/usr/bin/env python3
"""Genera og.png: la portada del deck, para la tarjeta de previsualizacion.

Es una captura real de la diapositiva 1, no una imagen aparte: si cambia la
portada, se vuelve a correr esto y la tarjeta queda al dia.

1200x630 es la proporcion que piden las redes (1.91:1). El escenario del deck
es 16:9, asi que queda una franja arriba y abajo del mismo negro calido del
fondo, sin costura visible.

Uso:  python tools/make-og.py
"""

import asyncio
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
DECK = (ROOT / "index.html").resolve().as_uri()
OUT = ROOT / "og.png"

# Sin la barra superior ni el contador: es una portada, no una captura de
# pantalla de la herramienta.
HIDE_CHROME = """
  .chrome, .index { display: none !important; }
"""


async def shoot() -> None:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 1200, "height": 630},
            device_scale_factor=1,
        )
        # ?slide=1 salta el boot y garantiza que sea la portada
        await page.goto(DECK + "?slide=1")
        await page.add_style_tag(content=HIDE_CHROME)

        # El deck encoge el escenario para que quepa ENTERO en la ventana; a
        # 1.91:1 eso deja la portada flotando pequena. Se fuerza la escala al
        # ancho y se recortan las franjas de arriba y abajo, que en la portada
        # estan vacias.
        await page.evaluate(
            "() => document.getElementById('stage')"
            ".style.setProperty('--scale', 1200 / 1280)"
        )

        # Las fuentes tienen que estar listas o la portada sale en fallback
        await page.evaluate("async () => { await document.fonts.ready; }")
        await page.wait_for_timeout(1200)

        active = await page.evaluate(
            "() => document.querySelector('.slide[data-active=\"true\"]')"
            "?.dataset.title"
        )
        if active != "Portada":
            raise SystemExit(f"esperaba la portada, salio: {active!r}")

        await page.screenshot(path=str(OUT))
        await browser.close()

    print(f"og.png -> {OUT.stat().st_size / 1024:.0f} KB (1200x630)")


asyncio.run(shoot())

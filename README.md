# Agrega Auth a tu APP en menos de 10 min

Deck para **[Clerk](https://clerk.com) × [The Next Craft](https://thenextcraft.crafter.run)**, por Ignacio Rueda ([jibaru.dev](https://jibaru.dev)).

13 diapositivas en 16:9, en español, con el sistema de diseño **"Commodore 64 mono"**
de [crafter-station/the-next-craft](https://github.com/crafter-station/the-next-craft)
(su `DESIGN.md` es la fuente de verdad): blanco y negro estricto, negro cálido
vintage, tipografía pixel PETSCII y `READY.█`.

## Presentar

Abre `deck.html` en el navegador. No necesita servidor ni build: es un solo
archivo con todo dentro (las únicas peticiones externas son las fuentes de
Google).

| Tecla | Acción |
|---|---|
| `→` `↓` `Espacio` `PageDown` | Siguiente |
| `←` `↑` `PageUp` | Anterior |
| `G` | Abrir el índice |
| `Esc` | Cerrar el índice |
| `Home` / `End` | Primera / última |

También responde a rueda del mouse, trackpad y swipe en móvil. Pon el navegador
en pantalla completa (`F11`) antes de proyectar.

El arranque muestra un boot de C64 la primera vez de cada sesión. Se salta con
cualquier tecla o clic, y no aparece si el sistema pide movimiento reducido.

## Exportar a PDF

`Ctrl/Cmd + P` → *Guardar como PDF*, horizontal, sin márgenes, con gráficos de
fondo activados. Cada diapositiva sale como una página de 1280×720.

## Editar

El contenido vive en `src/template.html`. `deck.html` es **generado**: no lo
edites a mano, se sobrescribe.

```bash
python build.py    # src/template.html + assets/*.svg -> deck.html
```

`build.py` inlinea los logos oficiales de `assets/` y los normaliza a
`currentColor`, porque el deck es blanco y negro estricto.

### Agregar una diapositiva

Copia un `<section class="slide" data-title="...">` dentro de `#stage`. El
índice, el contador y la barra de progreso se arman solos a partir del DOM.

Convenciones que conviene respetar:

- **Silkscreen no tiene glifos acentuados.** Los titulares `.pixel-heading` van
  sin tildes (el acento cae a otra fuente y se nota). El texto en mono sí puede
  llevarlas.
- **Máximo ~40 palabras de prosa por diapositiva**, según el
  [`deck-best-practices.md`](https://github.com/crafter-station/the-next-craft/blob/main/docs/deck-best-practices.md)
  del proyecto original. Si necesita más, son dos diapositivas.
- Poné `class="fill"` al bloque principal para que estire y ocupe el alto que
  sobra; el encabezado se queda anclado arriba y no salta entre diapositivas.
- Los números de línea BASIC (`10`, `20`, …) marcan el orden de la charla.
- **Legibilidad proyectada:** nada de texto por debajo de **15px** en el
  escenario de 1280×720 (≈2% del alto), y ningún par color/fondo por debajo de
  **4.5:1**. Hoy el mínimo real es 15px y 5.24:1. No uses `opacity` para
  atenuar texto — baja el contraste sin que se note en pantalla; usa
  `var(--text-dim)`, que está medido en 8.91:1.

## Estructura

```
deck.html            # el entregable: un solo archivo, autocontenido
build.py             # inlinea los SVG en la plantilla
src/template.html    # el contenido y los estilos (acá se edita)
assets/
  clerk-logo.svg     # logo oficial de Clerk
  crafter-logo.svg   # logotipo de Crafter Station
  next-logo.svg      # wordmark de Next.js
```

## Datos verificados

Los comandos salen de `clerk --help` (CLI v1.5.0) y de la
[documentación de Clerk](https://clerk.com/docs). El plan gratuito son
**50.000 MRU** (usuarios retenidos al mes), según
[clerk.com/pricing](https://clerk.com/pricing) — no los 10.000 MAU de la
tarifa antigua.

## Créditos

- **Sistema de diseño** — "Commodore 64 mono" de
  [crafter-station/the-next-craft](https://github.com/crafter-station/the-next-craft)
  (MIT). Su `DESIGN.md` y `docs/deck-best-practices.md` son la fuente de verdad.
- **Iconos de frameworks** — [simple-icons](https://github.com/simple-icons/simple-icons)
  (CC0 1.0), en `assets/icons/`.
- **Logos de marca** — Clerk, Crafter Station y Next.js son marcas de sus
  respectivos dueños; se usan aquí solo con fines de identificación.

# Generador de la presentación para el curso de IA aplicada

Reconstruye `../Tesina_MTI_IA_Aplicada.pptx` y su PDF desde cero.

## Requisitos

    npm install pptxgenjs
    # LibreOffice para la exportación a PDF, y poppler-utils para el render de control

## Uso

    ./render.sh

El script genera el `.pptx`, lo valida, lo exporta a PDF y arma hojas de contacto
(`qa-NN.jpg`) con las treinta láminas, para la revisión visual.

## Archivos

| Archivo | Qué contiene |
|:---|:---|
| `gen.js` | Las treinta láminas: cuatro diseños maestros, las tablas nativas y el plan de tiempos del orador |
| `visuals.js` | Los ocho gráficos nativos que reemplazan a las cajas con erratas |
| `recortes.py` | El recorte aplicado a la caja A3 y su motivo |
| `cajas/` | Las cuatro cajas reutilizadas como imagen, más el original de A3 |
| `render.sh` | Construcción, validación, exportación y hojas de contacto |
| `REVISION.md` | Las diez pasadas de revisión y los hallazgos que corrigió cada una |

## Criterios de contenido

- Fuente de verdad: `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md`.
- Sin emojis ni marcas de agua, según `CLAUDE.md`.
- Predominio de texto y gráficos nativos; las imágenes solo donde su texto es correcto.
- Toda cifra del mazo aparece en el informe con el mismo valor.
- Las veintitrés combinaciones de color cumplen el nivel AA de contraste.

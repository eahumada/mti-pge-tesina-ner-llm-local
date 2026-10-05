/* Gráficos nativos que reemplazan a los paneles con erratas o con cifras no respaldadas.
   Todos dibujan dentro de la columna derecha: x 6.75 → 12.75, y 1.30 → 5.76. */

module.exports = function (pres, THEME) {
  const C = pres.SchemeColor;
  const X = 6.75, W = 6.0, Y = 1.3, H = 4.46;
  const MONO = "+mn-lt";

  // marco con titulillo, para que los ocho visuales se lean como una familia
  function marco(s, titulo, name) {
    s.addShape(pres.ShapeType.roundRect, {
      x: X, y: Y, w: W, h: H, rectRadius: 0.05,
      fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 },
      objectName: "marco-" + name,
    });
    s.addText(titulo, { x: X + 0.3, y: Y + 0.22, w: W - 0.6, h: 0.3, margin: 0,
      fontSize: 11.5, bold: true, charSpacing: 1, color: THEME.colors.accent1, isTextBox: true });
  }

  function nota(s, texto) {
    s.addText(texto, { x: X + 0.3, y: Y + H - 0.66, w: W - 0.6, h: 0.5, margin: 0,
      fontSize: 10.5, italic: true, color: THEME.colors.accent5, isTextBox: true });
  }

  // tarjeta con cifra grande, etiqueta y pie
  function cifra(s, x, y, w, h, valor, etiqueta, pie, color, n) {
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.05,
      fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 1 }, objectName: "cifra-" + n });
    s.addText(valor, { x: x + 0.18, y: y + 0.14, w: w - 0.36, h: 0.62, margin: 0,
      fontSize: 27, bold: true, color, isTextBox: true });
    s.addText(etiqueta, { x: x + 0.18, y: y + 0.76, w: w - 0.36, h: 0.3, margin: 0,
      fontSize: 11.5, bold: true, color: C.text1, isTextBox: true });
    if (pie) s.addText(pie, { x: x + 0.18, y: y + 1.04, w: w - 0.36, h: 0.62, margin: 0,
      fontSize: 10, color: THEME.colors.accent5, isTextBox: true });
  }

  // fila: etiqueta a la izquierda, texto a la derecha
  function fila(s, x, y, w, etiqueta, texto, color, n) {
    s.addShape(pres.ShapeType.roundRect, { x, y, w: 1.55, h: 0.4, rectRadius: 0.05,
      fill: { color }, line: { color, width: 1 }, objectName: "fila-" + n });
    const lum = (h) => {
      const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      return 0.2126 * f(parseInt(h.slice(0, 2), 16)) + 0.7152 * f(parseInt(h.slice(2, 4), 16)) + 0.0722 * f(parseInt(h.slice(4, 6), 16));
    };
    s.addText(etiqueta, { x, y, w: 1.55, h: 0.4, margin: 0, align: "center", valign: "middle",
      fontSize: 10, bold: true, color: lum(color) > 0.3 ? THEME.colors.dk2 : "FFFFFF", isTextBox: true });
    s.addText(texto, { x: x + 1.7, y: y + 0.01, w: w - 1.7, h: 0.4, margin: 0, valign: "middle",
      fontSize: 10.5, color: C.text1, isTextBox: true });
  }

  const ejes = (titulo) => ({
    x: X + 0.25, y: Y + 0.62, w: W - 0.5, h: H - 1.35,
    showTitle: true, title: titulo, titleFontSize: 11, titleColor: THEME.colors.accent2,
    titleFontFace: MONO,
    showLegend: false, showValue: false,
    catAxisLabelColor: THEME.colors.accent2, catAxisLabelFontSize: 9.5, catAxisLabelFontFace: MONO,
    valAxisLabelColor: THEME.colors.accent5, valAxisLabelFontSize: 9, valAxisLabelFontFace: MONO,
    valGridLine: { color: "D9E2EC", size: 1 }, catGridLine: { style: "none" },
    chartColors: [THEME.colors.accent1],
  });

  return {
    /* §1.1 — el costo del proceso manual frente al estimado del sistema local */
    costo(s) {
      marco(s, "COSTO ESTIMADO POR ARTÍCULO", "costo");
      cifra(s, X + 0.3, Y + 0.65, 2.6, 1.75, "USD 8,75", "Revisión manual",
        "Analista a USD 35/hora, quince minutos por noticia", THEME.colors.accent3, "manual");
      cifra(s, X + 3.1, Y + 0.65, 2.6, 1.75, "USD 0,052", "Sistema local",
        "Infraestructura amortizada, igual para todos los modelos", THEME.colors.accent1, "local");
      s.addShape(pres.ShapeType.roundRect, { x: X + 0.3, y: Y + 2.6, w: W - 0.6, h: 0.72, rectRadius: 0.05,
        fill: { color: THEME.colors.accent2 }, line: { color: THEME.colors.accent2, width: 1 }, objectName: "delta-costo" });
      s.addText([
        { text: "−99,4 %  ", options: { fontSize: 18, bold: true, color: THEME.colors.accent6 } },
        { text: "en el costo unitario directo, equivalente al 60–80 % del costo operativo total", options: { fontSize: 11, color: "FFFFFF" } },
      ], { x: X + 0.5, y: Y + 2.68, w: W - 1.0, h: 0.56, margin: 0, valign: "middle", isTextBox: true });
      nota(s, "Ambas cifras son estimaciones declaradas como tales, no mediciones: dependen del precio del equipo, su vida útil, la tarifa eléctrica y el volumen realmente procesado.");
    },

    /* §1.2 — a dónde va el texto en cada opción */
    riesgo(s) {
      marco(s, "A DÓNDE VA EL TEXTO DEL CLIENTE", "riesgo");
      const cw = 2.6, cy = Y + 0.68, ch = 2.55;
      [["API en la nube", THEME.colors.accent3, X + 0.3,
        ["El artículo y el contexto de la investigación salen hacia un tercero",
         "Costo por llamada, que escala con el volumen",
         "Sujeto a las políticas del proveedor"]],
       ["Inferencia local", THEME.colors.accent1, X + 3.1,
        ["El texto no abandona la organización en ningún momento",
         "Sin costo por llamada ni dependencia de un proveedor",
         "Operación posible incluso desconectada"]],
      ].forEach(([tit, col, cx, pts], i) => {
        s.addShape(pres.ShapeType.roundRect, { x: cx, y: cy, w: cw, h: ch, rectRadius: 0.05,
          fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 1 }, objectName: "col-" + i });
        s.addShape(pres.ShapeType.roundRect, { x: cx + 0.18, y: cy + 0.18, w: cw - 0.36, h: 0.36, rectRadius: 0.05,
          fill: { color: col }, line: { color: col, width: 1 }, objectName: "tit-" + i });
        s.addText(tit, { x: cx + 0.18, y: cy + 0.18, w: cw - 0.36, h: 0.36, margin: 0,
          align: "center", valign: "middle", fontSize: 11, bold: true, color: "FFFFFF", isTextBox: true });
        s.addText(pts.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < pts.length - 1, paraSpaceAfter: 7 } })),
          { x: cx + 0.2, y: cy + 0.66, w: cw - 0.4, h: ch - 0.85, margin: 0, fontSize: 10, color: C.text1, isTextBox: true });
      });
      nota(s, "El estudio mide cuánto cuesta esa decisión en desempeño: menos de un punto de F1 sobre el corpus de mayor potencia.");
    },

    /* §3.2 — las cinco capas */
    capas(s) {
      marco(s, "LAS CINCO CAPAS DEL SISTEMA", "capas");
      const caps = [
        ["Ingesta", "Carga y valida el corpus contra su esquema"],
        ["Pub/Sub", "Desacopla la lectura del consumo por los modelos"],
        ["AIMD", "Ajusta los hilos activos ante errores y límites de tasa"],
        ["Proveedor", "Factory/Facade: Ollama local tras una interfaz común"],
        ["Evaluación", "F1, alucinaciones, ANOVA, Tukey y Friedman"],
      ];
      caps.forEach((c, i) => fila(s, X + 0.3, Y + 0.72 + i * 0.62, W - 0.6, c[0], c[1],
        i === 2 ? THEME.colors.accent6 : THEME.colors.accent1, i));
      nota(s, "El controlador reacciona a los errores del proveedor y a las rachas de fallo; no recibe telemetría de memoria, y así se declara en el informe.");
    },

    /* §4 — los tres corpus y las pruebas */
    corpus(s) {
      marco(s, "TRES CORPUS Y CÓMO SE CONTRASTAN", "corpus");
      const cs = [
        ["N=15", "Kleptotrace, inglés", "Exploratorio y variantes de prompt"],
        ["N=30", "Dominio AML/KYC, inglés", "Solo los dos modelos de mayor capacidad"],
        ["N=120", "Periodístico, 105 en español", "Estudio principal, 113 por grupo"],
      ];
      cs.forEach((c, i) => {
        const y = Y + 0.72 + i * 0.86;
        s.addShape(pres.ShapeType.roundRect, { x: X + 0.3, y, w: W - 0.6, h: 0.72, rectRadius: 0.05,
          fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 1 }, objectName: "corpus-" + i });
        s.addText(c[0], { x: X + 0.45, y: y + 0.08, w: 1.1, h: 0.56, margin: 0, valign: "middle",
          fontSize: 17, bold: true, color: i === 2 ? THEME.colors.accent1 : THEME.colors.accent5, isTextBox: true });
        s.addText(c[1], { x: X + 1.6, y: y + 0.08, w: W - 1.9, h: 0.28, margin: 0,
          fontSize: 11, bold: true, color: C.text1, isTextBox: true });
        s.addText(c[2], { x: X + 1.6, y: y + 0.36, w: W - 1.9, h: 0.28, margin: 0,
          fontSize: 10, color: THEME.colors.accent5, isTextBox: true });
      });
      s.addText("ANOVA de una vía · Tukey HSD · Friedman como contraste no paramétrico",
        { x: X + 0.3, y: Y + 3.35, w: W - 0.6, h: 0.3, margin: 0, fontSize: 10.5, bold: true,
          color: THEME.colors.accent2, isTextBox: true });
      nota(s, "Los veintiséis grupos del estudio principal evalúan los mismos 113 artículos, de modo que las observaciones no son independientes; por eso se repite con Friedman.");
    },

    /* §5.1 — los mejores modelos sobre el corpus principal */
    ranking(s) {
      marco(s, "F1 SOBRE EL CORPUS PRINCIPAL (N=120)", "ranking");
      s.addChart(pres.ChartType.bar, [{
        name: "F1 baseline",
        labels: ["llama3.2:latest   63,25 %", "gemma4:latest   75,33 %", "gpt-oss:20b   75,41 %",
                 "gemma4:12b-mlx   77,67 %", "gemma4:31b-mlx   81,47 %", "gemma4:31b-cloud   82,13 %"],
        values: [63.25, 75.33, 75.41, 77.67, 81.47, 82.13],
      }], Object.assign(ejes("Porcentaje de F1, extracción directa"), {
        barDir: "bar", valAxisMaxVal: 100, valAxisMinVal: 0,
        chartColors: [THEME.colors.accent1],
      }));
      nota(s, "La variante alojada encabeza por 0,66 puntos. Todas las demás filas son modelos abiertos ejecutados en local.");
    },

    /* §5.3 — local frente a nube, con el matiz de los dos corpus */
    soberania(s) {
      marco(s, "LOCAL FRENTE A NUBE, EN LOS DOS CORPUS", "soberania");
      s.addChart(pres.ChartType.bar, [
        { name: "En local", labels: ["N=120 principal\nlocal 81,47 % · nube 82,13 %", "N=15 exploratorio\nlocal 69,12 % · nube 66,99 %"], values: [81.47, 69.12] },
        { name: "En la nube", labels: ["N=120 principal\nlocal 81,47 % · nube 82,13 %", "N=15 exploratorio\nlocal 69,12 % · nube 66,99 %"], values: [82.13, 66.99] },
      ], Object.assign(ejes("Porcentaje de F1 del mismo modelo"), {
        barDir: "bar", barGrouping: "clustered", valAxisMaxVal: 100, valAxisMinVal: 0,
        showLegend: true, legendPos: "b", legendFontSize: 9.5, legendFontFace: MONO,
        legendColor: THEME.colors.accent2,
        chartColors: [THEME.colors.accent1, THEME.colors.accent3],
        h: H - 1.5,
      }));
      nota(s, "Los dos corpus no dicen lo mismo: sobre el de quince gana el local, pero es el de menor potencia. La conclusión sostenible es la del corpus mayor.");
    },

    /* §5.2 y §6 — el efecto del RAG por capacidad del modelo */
    rag(s) {
      marco(s, "EFECTO DEL RAG CONTEXTUAL, POR MODELO", "rag");
      s.addChart(pres.ChartType.bar, [{
        name: "Δ F1 con RAG contextual",
        labels: ["mistral-nemo   −4,29", "gemma4:31b-cloud   +0,81", "gemma4:31b-mlx   +0,97",
                 "gemma4:12b-mlx   +2,29", "gemma4:latest   +2,53", "llama3.2:latest   +6,73", "nemotron-mini:4b   +12,26"],
        values: [-4.29, 0.81, 0.97, 2.29, 2.53, 6.73, 12.26],
      }], Object.assign(ejes("Puntos porcentuales de F1 ganados o perdidos"), {
        barDir: "bar", valAxisMaxVal: 14, valAxisMinVal: -8, catAxisLabelPos: "low",
        chartColors: [THEME.colors.accent6], invertedColors: [THEME.colors.accent3],

      }));
      nota(s, "Solo el primero alcanza significancia estadística (p < 0,001) entre los trece modelos. El efecto decrece conforme sube la capacidad.");
    },

    /* §6-7 — viabilidad: costo y alucinaciones, con su alcance real */
    viabilidad(s) {
      marco(s, "LO QUE SE SOSTIENE, CON SU ALCANCE", "viabilidad");
      const items = [
        ["Fuga de datos", "Eliminada por construcción: el texto nunca sale", THEME.colors.accent1],
        ["Costo unitario", "−99,4 % estimado frente a la revisión manual", THEME.colors.accent1],
        ["Alucinación", "Cero en las variantes alojadas de gemma4:31b", THEME.colors.accent6],
        ["Alcance", "28 de 61 grupos medidos quedan por debajo del 1 %", THEME.colors.accent5],
        ["Límite", "Hasta 21,59 % en deepseek-r1:1.5b con diccionario", THEME.colors.accent3],
      ];
      items.forEach((c, i) => fila(s, X + 0.3, Y + 0.72 + i * 0.62, W - 0.6, c[0], c[1], c[2], "v" + i));
      nota(s, "El problema se concentra en los dos modelos más pequeños: en los de mayor capacidad la instrucción de ceñirse al artículo funciona.");
    },
  };
};

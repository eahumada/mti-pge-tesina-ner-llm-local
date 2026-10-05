const pptxgen = require("pptxgenjs");
const path = require("path");
const DIR = __dirname;
const IMG = (n) => path.join(DIR, "cajas", n + ".png");

const THEME = {
  name: "Soberania MTI",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "16213E", lt1: "FFFFFF",
    dk2: "0F1C3F", lt2: "EEF3F9",
    accent1: "0C6E6D", accent2: "1E2761", accent3: "C1292E",
    accent4: "E09F3E", accent5: "51708D", accent6: "2A9D8F",
    secOsc: "8FA9C4", accent6cl: "35B3A3",
    hlink: "0C6E6D", folHlink: "51708D",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13.3 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Eduardo Mauricio Ahumada Gallardo";
pres.company = "UTFSM - Magister en Tecnologias de la Informacion";
pres.subject = "NER soberano para cumplimiento AML/KYC";
pres.title = "Extraccion de entidades con soberania de datos";

const C = pres.SchemeColor;
const V = require("./visuals.js")(pres, THEME);
const FOOT = "MTI · Aplicaciones de inteligencia artificial · E. Ahumada G. · 3 de octubre de 2026";

/* ============================ layouts ============================ */

pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: THEME.colors.dk2 },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: 0.9, y: 1.55, w: 11.5, h: 0.45,
        fontSize: 14, color: THEME.colors.accent6, charSpacing: 2, bold: true, align: "left" }, text: " " } },
    { placeholder: { options: { name: "title", type: "title", x: 0.9, y: 2.05, w: 11.5, h: 2.0,
        fontSize: 40, bold: true, color: C.background1, align: "left", valign: "top" }, text: " " } },
    { placeholder: { options: { name: "sub", type: "body", x: 0.9, y: 4.2, w: 11.5, h: 1.0,
        fontSize: 17, color: THEME.colors.lt2, align: "left" }, text: " " } },
    { placeholder: { options: { name: "meta", type: "body", x: 0.9, y: 5.7, w: 11.5, h: 1.1,
        fontSize: 13, color: THEME.colors.secOsc, align: "left" }, text: " " } },
  ],
});

pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "chip", type: "body", x: 0.6, y: 0.42, w: 1.3, h: 0.42,
        fontSize: 12, bold: true, color: C.background1, align: "center", valign: "middle" }, text: " " } },
    { placeholder: { options: { name: "title", type: "title", x: 2.05, y: 0.34, w: 10.65, h: 0.72,
        fontSize: 26, bold: true, color: C.text1, align: "left", valign: "middle" }, text: " " } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 1.4, w: 5.75, h: 3.9,
        fontSize: 14, color: C.text1, align: "left" }, text: " " } },
    { placeholder: { options: { name: "pic", type: "pic", x: 6.75, y: 1.3, w: 6.0, h: 4.46,
        color: C.text1 }, text: " " } },
    { text: { text: FOOT, options: { x: 0.6, y: 6.95, w: 9.6, h: 0.3, fontSize: 9,
        color: THEME.colors.accent5, isTextBox: true, margin: 0 } } },
  ],
  slideNumber: { x: 12.4, y: 6.95, w: 0.5, h: 0.3, fontSize: 9, color: THEME.colors.accent5, align: "right" },
});

pres.defineSlideMaster({
  title: "ANCHO",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "chip", type: "body", x: 0.6, y: 0.42, w: 1.3, h: 0.42,
        fontSize: 12, bold: true, color: C.background1, align: "center", valign: "middle" }, text: " " } },
    { placeholder: { options: { name: "title", type: "title", x: 2.05, y: 0.34, w: 10.65, h: 0.72,
        fontSize: 26, bold: true, color: C.text1, align: "left", valign: "middle" }, text: " " } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 1.3, w: 12.1, h: 5.4,
        fontSize: 14, color: C.text1, align: "left" }, text: " " } },
    { text: { text: FOOT, options: { x: 0.6, y: 6.95, w: 9.6, h: 0.3, fontSize: 9,
        color: THEME.colors.accent5, isTextBox: true, margin: 0 } } },
  ],
  slideNumber: { x: 12.4, y: 6.95, w: 0.5, h: 0.3, fontSize: 9, color: THEME.colors.accent5, align: "right" },
});

pres.defineSlideMaster({
  title: "OSCURA",
  background: { color: THEME.colors.dk2 },
  objects: [
    { placeholder: { options: { name: "chip", type: "body", x: 0.6, y: 0.42, w: 1.3, h: 0.42,
        fontSize: 12, bold: true, color: THEME.colors.dk2, align: "center", valign: "middle" }, text: " " } },
    { placeholder: { options: { name: "title", type: "title", x: 2.05, y: 0.34, w: 10.65, h: 0.72,
        fontSize: 26, bold: true, color: C.background1, align: "left", valign: "middle" }, text: " " } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 1.4, w: 12.1, h: 1.9,
        fontSize: 14, color: THEME.colors.lt2, align: "left" }, text: " " } },
    { text: { text: FOOT, options: { x: 0.6, y: 6.95, w: 9.6, h: 0.3, fontSize: 9,
        color: "8FA9C4", isTextBox: true, margin: 0 } } },
  ],
  slideNumber: { x: 12.4, y: 6.95, w: 0.5, h: 0.3, fontSize: 9, color: "8FA9C4", align: "right" },
});

/* ============================ helpers ============================ */

// Lee el tamaño real del PNG (cabecera IHDR) para no deformar las infografías:
// el marco es 6,00 x 4,46 y cada caja tiene su propia proporción.
function pngSize(file) {
  const b = require("fs").readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

function encajar(nombre, bx, by, bw, bh) {
  const p = pngSize(IMG(nombre));
  const k = Math.min(bw / p.w, bh / p.h);
  const w = p.w * k, h = p.h * k;
  return { x: bx + (bw - w) / 2, y: by + (bh - h) / 2, w, h };
}

function chip(s, label, dark) {
  s.addShape(pres.ShapeType.roundRect, {
    x: 0.6, y: 0.42, w: 1.3, h: 0.42, rectRadius: 0.08,
    fill: { color: dark ? THEME.colors.accent6 : THEME.colors.accent1 },
    line: { color: dark ? THEME.colors.accent6 : THEME.colors.accent1, width: 0 },
    objectName: "chip-" + label,
  });
  s.addText(label, { placeholder: "chip" });
}

function bullets(s, items, ph) {
  const runs = items.map((t, i) => ({
    text: t,
    options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 9 },
  }));
  s.addText(runs, { placeholder: ph || "body" });
}

function stat(s, x, y, w, big, label, color) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h: 1.15, rectRadius: 0.06,
    fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 },
    objectName: "dato-" + big,
  });
  s.addText(big, { x: x + 0.16, y: y + 0.09, w: w - 0.32, h: 0.5, margin: 0,
    fontSize: 24, bold: true, color: color || THEME.colors.accent1, isTextBox: true });
  s.addText(label, { x: x + 0.16, y: y + 0.58, w: w - 0.32, h: 0.5, margin: 0,
    fontSize: 10.5, color: THEME.colors.accent5, isTextBox: true });
}

function stats(s, list, y, x0, wTotal) {
  const n = list.length, gap = 0.22;
  const W0 = wTotal || 5.75, X0 = x0 === undefined ? 0.6 : x0;
  const w = (W0 - gap * (n - 1)) / n;
  list.forEach((st, i) => stat(s, X0 + i * (w + gap), y === undefined ? 5.45 : y, w, st[0], st[1], st[2]));
}

function content(s, chapLabel, title, items, visual, kpis) {
  chip(s, chapLabel, false);
  s.addText(title, { placeholder: "title" });
  bullets(s, items);
  if (typeof visual === "function") visual(s);
  else if (visual) {
    // mismo marco que los gráficos nativos, para que las cuatro cajas reutilizadas
    // no floten sobre el blanco mientras el resto del mazo va enmarcado
    s.addShape(pres.ShapeType.roundRect, { x: 6.75, y: 1.3, w: 6.0, h: 4.46, rectRadius: 0.05,
      fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 },
      objectName: "marco-" + visual });
    const c = encajar(visual, 6.93, 1.48, 5.64, 4.1);
    s.addImage({ path: IMG(visual), x: c.x, y: c.y, w: c.w, h: c.h, objectName: "infografia-" + visual });
  }
  if (kpis) stats(s, kpis);
}

// tabla nativa: encabezado en color de acento, cuerpo alternado
function tabla(s, head, rows, opts) {
  const o = opts || {};
  const hdr = head.map((h) => ({
    text: h,
    options: { bold: true, color: "FFFFFF", fill: { color: THEME.colors.accent2 }, fontSize: o.fsHead || 11.5,
      align: "center", valign: "middle" },
  }));
  const body = rows.map((r, i) =>
    r.map((cell, j) => {
      const isObj = cell && typeof cell === "object";
      const txt = isObj ? cell.t : cell;
      const op = isObj ? cell : {};
      return {
        text: String(txt),
        options: Object.assign({
          fontSize: o.fsBody || 11,
          color: op.color || C.text1,
          bold: !!op.bold,
          align: j === 0 ? "left" : "center",
          valign: "middle",
          fill: { color: op.fill || (i % 2 ? "FFFFFF" : THEME.colors.lt2) },
        }, op.opts || {}),
      };
    })
  );
  s.addTable([hdr].concat(body), Object.assign({
    x: 0.6, y: 1.45, w: 12.1,
    colW: o.colW,
    border: { type: "solid", color: "D6DFE9", pt: 0.5 },
    rowH: o.rowH || 0.27,
    margin: [2, 5, 2, 5],
    autoPage: false,
    objectName: o.name || "tabla",
  }, o.table || {}));
}

// vinetas en un marco propio, para laminas anchas con dos columnas
function bullets2(s, x, y, w, h, items, fs) {
  const runs = items.map((t, i) => ({
    text: t,
    options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 10 },
  }));
  s.addText(runs, { x, y, w, h, fontSize: fs || 13, color: C.text1, isTextBox: true, margin: 0, valign: "top" });
}

function nota(s, texto, y) {
  s.addText(texto, { x: 0.6, y: y === undefined ? 6.35 : y, w: 12.1, h: 0.5,
    fontSize: 10.5, italic: true, color: THEME.colors.accent5, isTextBox: true, margin: 0 });
}


/* ---- plan de tiempos: 14 minutos de recorrido y 8 láminas de respaldo ---- */

const PLAN = [
  "[0:00–0:30 · recorrido]", "[0:30–1:15 · recorrido]", "[1:15–1:45 · recorrido]",
  "[1:45–2:35 · recorrido]", "[2:35–3:15 · recorrido]", "[3:15–4:00 · recorrido]",
  "[4:00–4:45 · recorrido]", "[4:45–5:20 · recorrido]",
  "[RESPALDO · solo si preguntan por los objetivos formales]",
  "[5:20–6:00 · recorrido]",
  "[RESPALDO · solo si preguntan por qué no BERT]",
  "[6:00–6:40 · recorrido]", "[6:40–7:30 · recorrido]", "[7:30–8:20 · recorrido]",
  "[8:20–9:00 · recorrido]", "[9:00–9:45 · recorrido]",
  "[RESPALDO · solo si preguntan por la implementación]",
  "[9:45–10:25 · recorrido]",
  "[RESPALDO · solo si preguntan por el catálogo de modelos]",
  "[RESPALDO · solo si preguntan por las métricas o las convenciones]",
  "[10:25–11:15 · recorrido]", "[11:15–12:00 · recorrido]", "[12:00–12:40 · recorrido]",
  "[12:40–13:20 · recorrido]",
  "[RESPALDO · usarla si sobra tiempo; sostiene la honestidad del trabajo]",
  "[RESPALDO · solo si preguntan por costos o por el hardware]",
  "[13:20–14:00 · recorrido]",
  "[RESPALDO · usarla si sobra tiempo o en la ronda de preguntas]",
  "[14:00–14:40 · recorrido]", "[14:40–15:00 · recorrido]",
];
let iPlan = 0;
function notas(s, texto) { s.addNotes(PLAN[iPlan++] + " " + texto); }

/* ---------------- 1. portada ---------------- */

/* ========================= 0. APERTURA ========================= */

pres.addSection({ title: "Apertura" });

/* --- 1. portada --- */
let s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Apertura" });
s.addText("BORRADOR DE PROYECTO FINAL · MVP FUNCIONAL · UN CASO DE IA APLICADA", { placeholder: "kicker" });
s.addText("Extracción de entidades con soberanía de datos", { placeholder: "title" });
s.addText([
  { text: "Modelos de lenguaje abiertos, ejecutados 100 % en local, para cumplimiento AML/KYC", options: { breakLine: true } },
  { text: "Clasificación y extracción de entidades nombradas (NER) en noticias de cumplimiento normativo corporativo", options: { fontSize: 13, color: THEME.colors.secOsc } },
], { placeholder: "sub" });
s.addText([
  { text: "Eduardo Mauricio Ahumada Gallardo", options: { bold: true, color: "FFFFFF", breakLine: true } },
  { text: "Universidad Técnica Federico Santa María · Departamento de Informática · Magíster en Tecnologías de la Información", options: { breakLine: true } },
  { text: "Aplicaciones de inteligencia artificial · Sesión del sábado 3 de octubre de 2026, 09:00 h" },
], { placeholder: "meta" });
notas(s, "Apertura en treinta segundos. Presentarse, decir que esto es el borrador del proyecto final y que el MVP ya corre. Anunciar el recorrido: problema, solución, evidencia, conclusiones. Reservar los últimos cinco minutos para preguntas.\n\n" +
  "PLAN DE TIEMPOS. Veintidós láminas de recorrido suman unos catorce minutos, con un minuto de holgura antes de los cinco de preguntas. Las ocho restantes son de respaldo y cada una lleva en su nota la pregunta que la justifica; se saltan en la pasada normal.\n" +
  "Recorrido: 1 a 8, 10, 12 a 16, 18, 21 a 24, 27, 29 y 30.\n" +
  "Respaldo: 9 objetivos, 11 familias de técnicas, 17 pila tecnológica, 19 catálogo de modelos, 20 métricas y convenciones, 25 alucinaciones, 26 eficiencia y costo, 28 limitaciones.\n" +
  "Si el tiempo se acorta a diez minutos, recortar por este orden: 5 aplicabilidad, 16 capas, 13 factorial del prompt y 23 soberanía, que queda cubierta por la lámina 21.\n" +
  "Si sobra tiempo, añadir 25 alucinaciones y 28 limitaciones: son las que más credibilidad aportan ante un tribunal.");

/* --- 2. presentación inicial --- */
s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "Apertura" });
chip(s, "INICIO", false);
s.addText("Quién presenta, qué se presenta y cómo", { placeholder: "title" });

const pres0 = [
  ["Expositor", "Eduardo M. Ahumada G.", "Estudiante del Magíster en Tecnologías de la Información de la UTFSM. El trabajo se desarrolla sobre un proceso real de cumplimiento normativo."],
  ["Qué se presenta", "Borrador del proyecto final", "Un MVP construido y medido: código funcionando, tres corpus anotados y resultados estadísticamente contrastados, aún en revisión."],
  ["Formato", "10 a 15 min + 5 de preguntas", "Treinta láminas: el recorrido principal y, al final de cada capítulo, las de detalle reservadas para la ronda de preguntas."],
];
pres0.forEach((b, i) => {
  const w = 3.9, gap = 0.2, x = 0.6 + i * (w + gap);
  s.addShape(pres.ShapeType.roundRect, { x, y: 1.4, w, h: 2.25, rectRadius: 0.07,
    fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 }, objectName: "pres-" + i });
  s.addText(b[0].toUpperCase(), { x: x + 0.22, y: 1.58, w: w - 0.44, h: 0.26, margin: 0,
    fontSize: 10, bold: true, charSpacing: 1.2, color: THEME.colors.accent1, isTextBox: true });
  s.addText(b[1], { x: x + 0.22, y: 1.86, w: w - 0.44, h: 0.42, margin: 0,
    fontSize: 15.5, bold: true, color: C.text1, isTextBox: true });
  s.addText(b[2], { x: x + 0.22, y: 2.32, w: w - 0.44, h: 1.2, margin: 0,
    fontSize: 11.5, color: THEME.colors.accent5, isTextBox: true });
});

s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 3.85, w: 12.1, h: 1.35, rectRadius: 0.07,
  fill: { color: THEME.colors.accent2 }, line: { width: 0 }, objectName: "tema" });
s.addText("EL TEMA, Y POR QUÉ ES DE INTERÉS GENERAL", { x: 0.9, y: 4.03, w: 11.5, h: 0.28, margin: 0,
  fontSize: 10, bold: true, charSpacing: 1.2, color: THEME.colors.accent6cl, isTextBox: true });
s.addText("Cualquier organización que deba revisar texto no estructurado —noticias, contratos, correos, expedientes— enfrenta el mismo dilema: automatizar con una API en la nube es rápido, pero entrega datos de clientes a un tercero. Este trabajo prueba que hoy se puede automatizar sin ceder el dato, con modelos abiertos sobre un equipo que la empresa ya tiene.",
  { x: 0.9, y: 4.33, w: 11.5, h: 0.78, margin: 0, fontSize: 13, color: "FFFFFF", isTextBox: true });

stats(s, [
  ["13", "modelos abiertos evaluados"],
  ["120", "artículos reales anotados"],
  ["81,47 %", "F1 del mejor modelo local"],
  ["0", "salidas a Internet en operación local"],
], 5.4, 0.6, 12.1);
notas(s, "Encuadre para el curso: tema de interés general, aplicable a cualquier empresa que procese texto sensible. El MVP está construido, no es una propuesta en papel. Si el grupo presenta en conjunto, añadir aquí a los coexpositores.");

/* --- 3. ruta --- */
s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "Apertura" });
chip(s, "RUTA", false);
s.addText("El recorrido de los próximos quince minutos", { placeholder: "title" });
s.addText([
  { text: "La pregunta que ordena todo el trabajo:", options: { breakLine: true, fontSize: 12, color: THEME.colors.accent5, paraSpaceAfter: 6 } },
  { text: "¿Puede un modelo de lenguaje abierto, corriendo en un equipo de la propia empresa, igualar a una API comercial sin entregarle los datos del cliente?",
    options: { breakLine: true, fontSize: 17, bold: true, color: THEME.colors.accent1, paraSpaceAfter: 16 } },
  { text: "La respuesta corta es que sí, y que la diferencia es menor a un punto porcentual de F1. El resto de la presentación es cómo se midió eso y qué supuestos hay detrás.",
    options: { fontSize: 13.5, color: C.text1 } },
], { placeholder: "body" });

const ruta = [
  ["1", "Problema y trilema", "El costo de vigilar noticias y por qué ninguna vía lo resuelve sola"],
  ["2", "Marco teórico", "Familias de NER, aprendizaje en contexto y RAG contextual"],
  ["3", "Arquitectura y MVP", "Ejecución local, concurrencia adaptativa y aislamiento de proveedores"],
  ["4", "Diseño experimental", "Tres corpus, trece configuraciones y validación estadística"],
  ["5", "Resultados", "Desempeño, soberanía frente a la nube, alucinaciones y eficiencia"],
  ["6", "Conclusiones", "Viabilidad, costos, limitaciones y hoja de ruta"],
];
ruta.forEach((r, i) => {
  const y = 1.45 + i * 0.78;
  s.addShape(pres.ShapeType.ellipse, { x: 6.9, y: y + 0.06, w: 0.42, h: 0.42,
    fill: { color: THEME.colors.accent1 }, line: { width: 0 }, objectName: "num-" + r[0] });
  s.addText(r[0], { x: 6.9, y: y + 0.06, w: 0.42, h: 0.42, margin: 0, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: "FFFFFF", isTextBox: true });
  s.addText(r[1], { x: 7.5, y: y, w: 5.2, h: 0.3, margin: 0, fontSize: 14, bold: true, color: C.text1, isTextBox: true });
  s.addText(r[2], { x: 7.5, y: y + 0.3, w: 5.2, h: 0.36, margin: 0, fontSize: 11, color: THEME.colors.accent5, isTextBox: true });
});
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.6, w: 5.75, h: 1.7, rectRadius: 0.06,
  fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 }, objectName: "caso" });
s.addText("El caso, en una línea", { x: 0.85, y: 4.78, w: 5.25, h: 0.3, margin: 0,
  fontSize: 11, bold: true, charSpacing: 1, color: THEME.colors.accent1, isTextBox: true });
s.addText("Trece modelos abiertos, de 1,5B a 31B parámetros, evaluados sobre 120 artículos reales para extraer personas y organizaciones sujetas a vigilancia de cumplimiento, con todo el procesamiento dentro de la organización.",
  { x: 0.85, y: 5.08, w: 5.25, h: 1.1, margin: 0, fontSize: 12.5, color: C.text1, isTextBox: true });
notas(s, "Mostrar la pregunta y anunciar la respuesta de entrada: así la audiencia escucha la evidencia sabiendo adónde va.");

/* --- 4. el MVP --- */
s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "Apertura" });
chip(s, "MVP", false);
s.addText("Qué está construido y funcionando hoy", { placeholder: "title" });
const mvp = [
  ["Pipeline de extracción", "Ingesta de artículos, inferencia local con Ollama, salida JSON validada contra esquema y almacenamiento de resultados por corrida."],
  ["Orquestador concurrente", "Arquitectura pub/sub multihilo con controlador AIMD de concurrencia, cortacircuitos ante rachas de error y punto de control reanudable."],
  ["Módulo RAG contextual", "Base de conocimientos con guías tipológicas por dominio y ejemplares anotados, con cuatro modos seleccionables por línea de órdenes."],
  ["Evaluador y estadística", "Cotejo difuso por distancia de Indel, precisión, exhaustividad, F1, tasa de alucinación, ANOVA, Tukey HSD y Friedman."],
  ["Tablero de resultados", "Interfaz en Streamlit para explorar corridas, comparar modelos y revisar el detalle de cada artículo extraído."],
  ["Reproducibilidad", "Cada corrida queda definida por un fichero de configuración, de modo que cualquier cifra del informe puede rehacerse."],
];
mvp.forEach((m, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const w = 5.95, x = 0.6 + col * (w + 0.2), y = 1.4 + row * 1.42;
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 1.26, rectRadius: 0.06,
    fill: { color: "FFFFFF" }, line: { color: "D6DFE9", width: 1 }, objectName: "mvp-" + i });
  s.addShape(pres.ShapeType.rect, { x, y, w: 0.07, h: 1.26, fill: { color: THEME.colors.accent1 },
    line: { width: 0 }, objectName: "mvpbar-" + i });
  s.addText(m[0], { x: x + 0.26, y: y + 0.14, w: w - 0.5, h: 0.3, margin: 0,
    fontSize: 14, bold: true, color: C.text1, isTextBox: true });
  s.addText(m[1], { x: x + 0.26, y: y + 0.45, w: w - 0.5, h: 0.72, margin: 0,
    fontSize: 11.5, color: THEME.colors.accent5, isTextBox: true });
});
nota(s, "Alcance del MVP: procesa artículos en lote sobre hardware local, no está integrado todavía a un feed de noticias en tiempo real ni expuesto como servicio. Esa integración es la fase 4 de la hoja de ruta.", 6.1);
notas(s, "Esta es la lámina que responde al requisito de MVP del curso: lo construido, con su alcance y sus límites dichos en voz alta.");

/* --- 5. aplicabilidad --- */
s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "Apertura" });
chip(s, "IMPACTO", false);
s.addText("Dónde se aplica esto dentro de una empresa", { placeholder: "title" });
s.addText([
  { text: "El caso estudiado es la vigilancia de medios para prevención de lavado de activos, pero el patrón —leer texto no estructurado, extraer entidades y clasificarlas, sin que el texto salga de la organización— se repite en funciones muy distintas.",
    options: { fontSize: 13.5, paraSpaceAfter: 12 } },
], { placeholder: "body" });
const usos = [
  ["Cumplimiento y riesgo", "Vigilancia continua de noticias y listas de sanciones; detección temprana de exposición reputacional de clientes y contrapartes."],
  ["Legal y contratos", "Extracción de partes, plazos y obligaciones desde contratos y anexos, sin subir documentos confidenciales a un servicio externo."],
  ["Operaciones y siniestros", "Lectura de informes, peritajes y denuncias para prellenar expedientes y detectar inconsistencias antes de la revisión humana."],
  ["Atención de clientes", "Clasificación y enrutamiento de correos y reclamos con datos personales, manteniendo la información dentro del perímetro de la empresa."],
];
usos.forEach((u, i) => {
  const w = 2.92, gap = 0.21, x = 0.6 + i * (w + gap);
  s.addShape(pres.ShapeType.roundRect, { x, y: 2.5, w, h: 2.25, rectRadius: 0.07,
    fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 }, objectName: "uso-" + i });
  s.addText(u[0], { x: x + 0.2, y: 2.68, w: w - 0.4, h: 0.5, margin: 0,
    fontSize: 13.5, bold: true, color: THEME.colors.accent1, isTextBox: true });
  s.addText(u[1], { x: x + 0.2, y: 3.2, w: w - 0.4, h: 1.4, margin: 0,
    fontSize: 11.5, color: C.text1, isTextBox: true });
});
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 5.1, w: 12.1, h: 1.1, rectRadius: 0.06,
  fill: { color: THEME.colors.accent2 }, line: { width: 0 }, objectName: "condicion" });
s.addText([
  { text: "La condición que lo habilita:  ", options: { fontSize: 13, bold: true, color: THEME.colors.accent6cl } },
  { text: "los modelos abiertos de tamaño medio ya caben en un equipo de escritorio con memoria unificada, así que la inferencia deja de requerir un centro de datos y el dato deja de tener que viajar.",
    options: { fontSize: 13, color: "FFFFFF" } },
], { x: 0.9, y: 5.28, w: 11.5, h: 0.78, margin: 0, isTextBox: true });
notas(s, "Conectar con la audiencia: cada asistente trabaja en una empresa distinta. El patrón es el mismo, cambia el documento.");

/* ========================= 1. PROBLEMA ========================= */

pres.addSection({ title: "1. Problema" });

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "1. Problema" });
content(s, "CAP. 1",
  "El desafío operativo: vigilar el flujo noticioso",
  [
    "Las instituciones sujetas a AML y KYC están obligadas a monitorear de forma continua grandes volúmenes de noticias no estructuradas, buscando personas y organizaciones ligadas a sanciones, corrupción o lavado de activos.",
    "El volumen exige automatizar, pero el texto periodístico en español trae ambigüedad referencial: «Santander» puede ser una persona, un banco o una ciudad.",
    "Hacerlo a mano da la máxima precisión y un costo que crece linealmente con el flujo. Es insostenible.",
    "Automatizar no es prescindir del analista: el sistema le entrega una preselección que él valida, de modo que el ahorro depende de cuánto baje el volumen que llega a revisión humana.",
  ],
  V.costo,
  [["15 min", "de analista por noticia, estimado"], ["Cientos", "de artículos al día sin analista dedicado"]]);
notas(s, "Punto de partida: una obligación regulatoria que no se puede desatender y un costo que escala con el volumen.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "1. Problema" });
content(s, "CAP. 1",
  "El trilema: ninguna vía resuelve el problema sola",
  [
    "Revisión manual: máxima precisión, pero el costo escala con el volumen y no soporta un flujo continuo.",
    "APIs comerciales en la nube: aportan la capacidad técnica, pero transfieren datos de clientes y contexto confidencial a un tercero, con un costo que crece con el uso.",
    "Modelos supervisados tipo BERT-NER: exigen miles de ejemplos etiquetados del dominio, y no existe corpus público anotado en español para AML/KYC.",
    "De ahí la cuarta vía que este trabajo evalúa: un modelo generativo abierto, instruido por prompt y ejecutado dentro de la organización.",
  ],
  "A1",
  [["3 vías clásicas", "y las tres fallan en algo distinto"], ["0", "corpus público AML/KYC en español"]]);
notas(s, "El trilema es el argumento central del capítulo 1: cada alternativa resuelve una arista y rompe otra.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "1. Problema" });
content(s, "CAP. 1",
  "Riesgo y soberanía del dato",
  [
    "Procesar la noticia en una API externa significa entregar a un proveedor el texto y el contexto de la investigación, no una consulta anónima.",
    "En una entidad regulada eso choca con las políticas de privacidad y con la soberanía del dato, antes incluso que con el presupuesto.",
    "Evitarlo elimina además la necesidad de suscribir acuerdos de tratamiento de datos con un proveedor externo y reduce la superficie de exposición.",
    "La alternativa evaluada mantiene el texto dentro de la organización: inferencia local sobre hardware propio, sin salida a Internet.",
  ],
  V.riesgo,
  [["100 %", "del proceso, puertas adentro"], ["< 1 pp", "cuesta esa soberanía en F1"]]);
notas(s, "La soberanía no es un extra: en entidades reguladas condiciona si la solución es siquiera adoptable.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "1. Problema" });
chip(s, "CAP. 1", false);
s.addText("Objetivos del trabajo", { placeholder: "title" });
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 1.35, w: 12.1, h: 0.95, rectRadius: 0.06,
  fill: { color: THEME.colors.accent2 }, line: { width: 0 }, objectName: "og" });
s.addText("OBJETIVO GENERAL", { x: 0.9, y: 1.5, w: 11.5, h: 0.26, margin: 0,
  fontSize: 10, bold: true, charSpacing: 1.2, color: THEME.colors.accent6cl, isTextBox: true });
s.addText("Diseñar, implementar y validar un sistema soberano de extracción de entidades nombradas para cumplimiento normativo (AML/KYC) basado en modelos de lenguaje de código abierto ejecutados localmente.",
  { x: 0.9, y: 1.78, w: 11.5, h: 0.45, margin: 0, fontSize: 13.5, color: "FFFFFF", isTextBox: true });

const objs = [
  ["OE1", "Arquitectura", "Diseñar e implementar una arquitectura pub/sub multihilo con control adaptativo de concurrencia para ejecutar modelos de gran escala en hardware Apple Silicon."],
  ["OE2", "Comparación de modelos", "Evaluar modelos abiertos de las familias Gemma, Llama, DeepSeek, Qwen, Mistral, GPT-OSS y Nemotron: doce en el benchmark exploratorio y trece en el estudio principal."],
  ["OE3", "Diseño de prompts", "Comparar cuatro configuraciones de prompt en un diseño factorial dos por dos, cruzando idioma e inclusión de ejemplos, para cuantificar la localización lingüística."],
  ["OE4", "Validación estadística", "Contrastar los resultados mediante ANOVA de una vía y pruebas post-hoc de Tukey HSD con alfa de 0,05 sobre un corpus de treinta observaciones o más."],
  ["OE5", "Costo y alucinación", "Demostrar una reducción del costo operativo entre 60 % y 80 % frente a la revisión manual, manteniendo la tasa de alucinaciones por debajo del 5 %."],
];
objs.forEach((o, i) => {
  const y = 2.55 + i * 0.82;
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 0.9, h: 0.62, rectRadius: 0.06,
    fill: { color: THEME.colors.accent1 }, line: { width: 0 }, objectName: "oe-" + i });
  s.addText(o[0], { x: 0.6, y, w: 0.9, h: 0.62, margin: 0, align: "center", valign: "middle",
    fontSize: 12, bold: true, color: "FFFFFF", isTextBox: true });
  s.addText(o[1], { x: 1.68, y: y + 0.02, w: 2.5, h: 0.3, margin: 0, fontSize: 13, bold: true, color: C.text1, isTextBox: true });
  s.addText(o[2], { x: 4.25, y: y + 0.02, w: 8.45, h: 0.58, margin: 0, fontSize: 11.5, color: THEME.colors.accent5, isTextBox: true });
});
notas(s, "Los cinco objetivos específicos se cumplen; el quinto, con la salvedad de que las cifras de costo son estimaciones y de que el umbral de alucinación se cumple en el modelo recomendado, no en todo el catálogo.");

s = pres.addSlide({ masterName: "OSCURA", sectionTitle: "1. Problema" });
chip(s, "CAP. 1", true);
s.addText("Hipótesis de trabajo", { placeholder: "title" });
s.addText("Es viable un sistema soberano de extracción y clasificación de entidades financieras para cumplimiento corporativo usando modelos de lenguaje abiertos de 1,5B a 31B parámetros ejecutados en local, alcanzando un desempeño competitivo en español mediante prompt engineering y few-shot learning, eliminando la fuga de datos confidenciales y reduciendo los costos operativos.",
  { placeholder: "body" });
const hip = [
  ["F1 ≥ 70 %", "umbral de viabilidad, en español"],
  ["1,5B – 31B", "rango de modelos evaluados"],
  ["2 variables", "modelo LLM y estrategia de prompt"],
  ["4 medidas", "F1, alucinación, latencia y VRAM"],
];
hip.forEach((h, i) => {
  const w = 2.86, gap = 0.22, x = 0.6 + i * (w + gap);
  s.addShape(pres.ShapeType.roundRect, { x, y: 3.05, w, h: 1.45, rectRadius: 0.06,
    fill: { color: "1A2A52" }, line: { width: 0 }, objectName: "hip-" + i });
  s.addText(h[0], { x: x + 0.18, y: 3.22, w: w - 0.36, h: 0.58, margin: 0, fontSize: 21, bold: true,
    color: THEME.colors.accent6, isTextBox: true });
  s.addText(h[1], { x: x + 0.18, y: 3.82, w: w - 0.36, h: 0.55, margin: 0, fontSize: 10.5,
    color: THEME.colors.lt2, isTextBox: true });
});
s.addText("Variables independientes: el modelo seleccionado y la estrategia de prompt (zero-shot o few-shot, en inglés o en español). Variables dependientes: F1 agregado por artículo, tasa de alucinación extrínseca, latencia en tokens por segundo y consumo de memoria de vídeo. El umbral del 70 % hace la hipótesis falsable: el resultado podía contradecirla.",
  { x: 0.6, y: 4.95, w: 12.1, h: 0.95, fontSize: 12, color: THEME.colors.secOsc, isTextBox: true, margin: 0 });
notas(s, "La hipótesis fija un umbral falsable y declara qué se mide, de modo que el resultado puede contradecirla.");

/* ========================= 2. MARCO TEÓRICO ========================= */

pres.addSection({ title: "2. Marco teórico" });

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "2. Marco teórico" });
chip(s, "CAP. 2", false);
s.addText("Cuatro familias de técnicas, y por qué solo una es viable aquí", { placeholder: "title" });
tabla(s,
  ["Familia", "Datos etiquetados que exige", "Fortaleza", "Por qué se descarta (o se elige)"],
  [
    ["Reglas y diccionarios", "Ninguno", "Adaptación inmediata y trazabilidad total", "Cobertura cerrada: no ve lo que no está catalogado"],
    ["CRF y BiLSTM-CRF", "Miles a decenas de miles de oraciones", "Buen desempeño con rasgos bien diseñados", "Exige anotación del dominio más ingeniería de rasgos"],
    ["Transformer con ajuste fino (BERT)", "Corpus anotado del dominio", "El mejor F1 publicado en la literatura", "No existe corpus AML/KYC anotado en español"],
    [{ t: "LLM generativo en contexto", bold: true, fill: "DCEFEE" },
     { t: "Ninguno", bold: true, fill: "DCEFEE" },
     { t: "Adaptación por prompt, sin reentrenar", bold: true, fill: "DCEFEE" },
     { t: "Vía elegida: su riesgo propio es la alucinación", bold: true, fill: "DCEFEE", color: THEME.colors.accent1 }],
  ],
  { colW: [2.7, 2.9, 3.1, 3.4], rowH: 0.52, name: "familias" });
s.addText("La elección no es por moda. Es la única familia que no depende de un corpus anotado que el dominio no tiene, y a cambio obliga a medir explícitamente dos riesgos que las otras no traen: la salida no estructurada, que se fuerza a un esquema verificable, y la alucinación, que se mide contra el texto de origen.",
  { x: 0.6, y: 4.3, w: 12.1, h: 0.8, fontSize: 13, color: C.text1, isTextBox: true, margin: 0 });
stats(s, [["0 ejemplos", "etiquetados exige la vía elegida"],
          ["2 riesgos", "formato y alucinación, ambos medidos"],
          ["7 familias", "de modelos abiertos evaluadas"],
          ["13 modelos", "en el estudio principal, en 26 grupos"]], 5.25, 0.6, 12.1);
notas(s, "Esta tabla justifica la decisión técnica de fondo. Si alguien pregunta por BERT, la respuesta es el corpus que no existe.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "2. Marco teórico" });
content(s, "CAP. 2",
  "Aprendizaje en contexto: enseñar sin reentrenar",
  [
    "Un modelo generativo se adapta a una tarea nueva sin actualizar sus pesos, solo a partir de lo que recibe en el prompt. Es lo que Brown y sus colegas documentaron en el trabajo fundacional de GPT-3.",
    "En la variante few-shot el prompt antepone un puñado de ejemplos resueltos; en zero-shot el modelo deduce formato y criterio solo de la instrucción.",
    "Los ejemplos cumplen tres funciones: fijan el formato de salida en JSON, calibran el umbral semántico —qué cuenta como entidad— y adaptan el modelo a la terminología regulatoria.",
    "El efecto es real y se replicó con cinco semillas, pero no se comporta igual en los tres corpus: ese matiz se desarrolla en la lámina siguiente.",
  ],
  "A2",
  [["0", "pesos actualizados"], ["2 ejemplos", "bastan para fijar el criterio"]]);
notas(s, "Aquí conviene ser preciso: el aprendizaje en contexto no es entrenamiento. No hay gradientes ni pesos nuevos.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "2. Marco teórico" });
chip(s, "CAP. 2", false);
s.addText("Diseño factorial del prompt: idioma por ejemplos", { placeholder: "title" });
tabla(s,
  ["Configuración", "F1", "Precisión", "Recall", "Alucinación", "Δ vs. baseline"],
  [
    ["Zero-shot inglés (baseline)", "66,77 %", "64,70 %", "70,16 %", "0,25 %", "—"],
    ["Zero-shot español", "75,78 %", "74,60 %", "78,68 %", "0,18 %", { t: "+9,01 pp", bold: true }],
    ["Few-shot inglés", "70,38 %", "69,92 %", "72,47 %", "0,07 %", "+3,61 pp"],
    [{ t: "Few-shot español", bold: true, fill: "DCEFEE" },
     { t: "79,96 %", bold: true, fill: "DCEFEE", color: THEME.colors.accent1 },
     { t: "81,17 %", bold: true, fill: "DCEFEE" },
     { t: "79,94 %", bold: true, fill: "DCEFEE" },
     { t: "0,14 %", fill: "DCEFEE" },
     { t: "+13,19 pp", bold: true, fill: "DCEFEE", color: THEME.colors.accent1 }],
  ],
  { colW: [3.7, 1.7, 1.7, 1.7, 1.7, 1.6], rowH: 0.42, name: "variantes" });
s.addText([
  { text: "Lectura:  ", options: { bold: true, fontSize: 13, color: THEME.colors.accent1 } },
  { text: "ninguno de los dos factores basta por separado, pero su combinación supera la suma de ambos. Media de cinco semillas declaradas (42 a 46) sobre el corpus de quince artículos; la jerarquía se repite en las cinco sin excepción, y el prompt en español produjo el 100 % de salidas parseables frente al 93,3 % del inglés.",
    options: { fontSize: 13, color: C.text1 } },
], { x: 0.6, y: 3.9, w: 12.1, h: 0.85, isTextBox: true, margin: 0 });
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.85, w: 12.1, h: 1.35, rectRadius: 0.06,
  fill: { color: "FDF3E3" }, line: { color: THEME.colors.accent4, width: 1 }, objectName: "matiz" });
s.addText("UNA ADVERTENCIA QUE EL PROPIO TRABAJO SE HACE", { x: 0.9, y: 5.0, w: 11.5, h: 0.26, margin: 0,
  fontSize: 10, bold: true, charSpacing: 1.2, color: "8A5F13", isTextBox: true });
s.addText("Sobre el corpus real de 120 artículos, mayoritariamente en español, el resultado se invierte: los ejemplos en inglés (76,35 %) superan a los españoles (75,57 %) en las cinco semillas. Ni «gana el español» ni «conviene coincidir con el idioma del texto» explican los tres corpus a la vez. El efecto está medido; su mecanismo queda como trabajo futuro.",
  { x: 0.9, y: 5.3, w: 11.5, h: 0.8, margin: 0, fontSize: 12.5, color: C.text1, isTextBox: true });
notas(s, "Decir la inversión en voz alta suma credibilidad: el trabajo publica el dato que contradice su propia explicación inicial.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "2. Marco teórico" });
chip(s, "CAP. 2", false);
s.addText("RAG contextual, no RAG de diccionario", { placeholder: "title" });
bullets(s, [
  "Primera versión, por diccionario: indexó 17 453 documentos —3 605 personas y 1 848 organizaciones de la lista SDN del Tesoro de Estados Unidos, más 12 000 nombres sintéticos— y antepuso al prompt los más próximos al artículo.",
  "Resultado contrario al esperado: de los once modelos con par completo de resultados, diez empeoraron, y entre ellos los de mejor desempeño base.",
  "El diagnóstico es un desajuste semántico estructural: la consulta es un artículo de varios centenares de palabras y lo indexado son cadenas de dos o tres términos. Para una noticia española se recuperaban razones sociales colombianas.",
  "Segunda versión, contextual: en lugar de entidades almacena criterios, es decir guías tipológicas por dominio y ejemplares anotados. La pregunta deja de ser «qué entidades hay» y pasa a ser «de qué dominio es este texto y qué reglas aplican».",
]);
s.addShape(pres.ShapeType.roundRect, { x: 6.9, y: 1.4, w: 5.7, h: 0.5, rectRadius: 0.06,
  fill: { color: THEME.colors.accent2 }, line: { width: 0 }, objectName: "titulo-a3" });
s.addText("QUÉ SE RECUPERA: CRITERIOS, NO NOMBRES", { x: 6.9, y: 1.4, w: 5.7, h: 0.5, margin: 0,
  align: "center", valign: "middle", fontSize: 11, bold: true, charSpacing: 1.2, color: "FFFFFF", isTextBox: true });
s.addShape(pres.ShapeType.rect, { x: 6.9, y: 1.9, w: 5.7, h: 3.3,
  fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 },
  objectName: "marco-A3" });
const cA3 = encajar("A3c", 6.95, 1.98, 5.6, 3.14);
s.addImage({ path: IMG("A3c"), x: cA3.x, y: cA3.y, w: cA3.w, h: cA3.h, objectName: "infografia-A3" });
s.addShape(pres.ShapeType.roundRect, { x: 6.95, y: 5.08, w: 5.6, h: 1.22, rectRadius: 0.06,
  fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 }, objectName: "pie-a3" });
s.addText("Inyectar reglas del dominio orienta al modelo sin coartarlo. Inyectar nombres lo induce a proponerlos: sugiere qué esperar y lo penaliza cuando lo sugerido no viene al caso.",
  { x: 7.18, y: 5.24, w: 5.14, h: 0.95, margin: 0, fontSize: 11.5, color: C.text1, isTextBox: true });
stats(s, [["10 de 11", "empeoran con RAG de diccionario"], ["11 de 13", "mejoran con RAG contextual"]], 5.45, 0.6, 5.75);
notas(s, "Hallazgo conceptual del trabajo: proveer reglas funciona, proveer listas estorba. El pie de la imagen se reemplazó porque el original afirmaba que el RAG elimina las alucinaciones, lo que los datos no sostienen.");

/* ========================= 3. ARQUITECTURA ========================= */

pres.addSection({ title: "3. Arquitectura" });

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "3. Arquitectura" });
content(s, "CAP. 3",
  "Ejecución 100 % local sobre hardware de consumo",
  [
    "Inferencia con Ollama, que encapsula el motor llama.cpp, sobre Apple Silicon con memoria unificada y aceleración Metal.",
    "Cuantización a 4 bits en formato GGUF Q4_K_M y compilaciones nativas MLX, para caber en la memoria disponible sin pérdida crítica de precisión.",
    "Dos escalones de hardware: 16 GB de memoria unificada para los modelos de hasta unos 12B, y 48 GB para los de 31B y las variantes MLX mayores.",
    "La memoria de vídeo fue el factor limitante del estudio: determina qué modelos caben en cada máquina y, por tanto, qué puede evaluarse.",
  ],
  "A4",
  [["Q4_K_M", "cuantización a 4 bits"], ["16 / 48 GB", "los dos escalones evaluados"]]);
notas(s, "La restricción de hardware es parte del aporte: el sistema debe correr en un equipo que la organización ya tiene.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "3. Arquitectura" });
content(s, "CAP. 3",
  "Cinco capas y un controlador que se adapta",
  [
    "Ingesta y cargador de conjunto de datos: parsea y valida el corpus contra su esquema antes de cualquier inferencia.",
    "Pub/Sub multihilo: desacopla la lectura de noticias del consumo por los modelos mediante colas seguras entre hilos.",
    "Controlador AIMD: incremento aditivo y disminución multiplicativa de los hilos activos, con cortacircuitos ante rachas de error. La idea viene del control de congestión en redes.",
    "Factory y Facade: aíslan el sistema del proveedor de inferencia, con Ollama local y conectores de prueba hacia servicios alojados.",
    "Módulo de evaluación: precisión, exhaustividad, F1, alucinaciones, ANOVA y Tukey HSD sobre los resultados almacenados.",
  ],
  V.capas,
  [["AIMD", "control adaptativo de la concurrencia"], ["5 capas", "con el proveedor tras una interfaz"]]);
notas(s, "El AIMD reacciona a límites de tasa del proveedor y a rachas de error. No recibe telemetría de memoria: esa salvedad se declara en la lámina de limitaciones.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "3. Arquitectura" });
chip(s, "CAP. 3", false);
s.addText("Decisiones de ingeniería y pila tecnológica", { placeholder: "title" });
const pila = [
  ["Inferencia", "Ollama 0.6 sobre llama.cpp; compilaciones MLX nativas para Apple Silicon", "Permite cambiar de modelo sin tocar el código de la aplicación"],
  ["Formato de modelo", "GGUF con cuantización Q4_K_M; variantes MLX en precisión mixta", "Reduce el tamaño en memoria lo suficiente para caber en memoria unificada"],
  ["Concurrencia", "Colas entre hilos, patrón productor/consumidor y controlador AIMD", "Evita saturar la GPU y congelar el equipo durante barridos largos"],
  ["Aislamiento del proveedor", "Patrones Factory y Facade sobre una interfaz común", "Hace intercambiables local y nube, que es lo que permitió compararlos"],
  ["Salida estructurada", "Esquema JSON validado por registro, con reintento ante fallo de parseo", "Convierte una salida no estructurada por construcción en dato verificable"],
  ["Evaluación", "Cotejo difuso por distancia de Indel normalizada, umbral de 85 sobre 100", "Tolera variaciones menores de forma sin admitir coincidencias espurias"],
  ["Estadística", "scikit-learn, statsmodels y pandas; ANOVA, Tukey HSD, Friedman y Levene", "Separa el efecto real de la variabilidad entre artículos"],
  ["Operación", "Punto de control automático por corrida y configuración reproducible", "Una corrida de decenas de horas se reanuda sin perder trabajo"],
];
tabla(s, ["Decisión", "Implementación", "Qué resuelve"],
  pila.map((p) => [{ t: p[0], bold: true }, p[1], p[2]]),
  { colW: [2.6, 4.9, 4.6], rowH: 0.47, fsBody: 10.5, name: "pila" });
nota(s, "El entorno completo se documenta en el anexo C del informe: Python 3.14, Ollama 0.6, scikit-learn, statsmodels, pandas y Streamlit sobre Apple Silicon con aceleración Metal.", 6.2);
notas(s, "Lámina de respaldo: útil si preguntan por la implementación. En la pasada rápida basta nombrar Ollama, AIMD y el esquema JSON.");

/* ========================= 4. DISEÑO EXPERIMENTAL ========================= */

pres.addSection({ title: "4. Diseño experimental" });

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "4. Diseño experimental" });
content(s, "CAP. 4",
  "Tres corpus complementarios, no intercambiables",
  [
    "Corpus 1 (N=15): artículos periodísticos reales sobre corrupción financiera, lavado y sanciones, en inglés, anotados a mano. Largos: unos 4 833 caracteres de media. Exploratorio.",
    "Corpus 2 (N=30): artículos breves sintéticos construidos desde pares de entidades fijados de antemano, para alcanzar el umbral que habilita las pruebas paramétricas.",
    "Corpus 3 (N=120): la validación principal, con 105 artículos reales en español de CoNLL-2002 y los 15 en inglés. Ningún texto generado por un modelo.",
    "Los tres se conservan: el sintético como validación de mínima potencia sobre el dominio propio, el real como validación de mayor potencia y menor especificidad.",
  ],
  V.corpus,
  [["120", "artículos en la validación principal"], ["0", "textos sintéticos en ese corpus"]]);
notas(s, "El corpus sintético no es el resultado: sirve para tener potencia estadística. La validación principal es sobre texto real.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "4. Diseño experimental" });
chip(s, "CAP. 4", false);
s.addText("Los trece modelos del estudio principal", { placeholder: "title" });
const fam = [
  ["Gemma", "gemma4:31b-mlx · gemma4:12b-mlx · gemma4:latest (9B) · gemma:latest (7B)", "Las variantes gemma4 copan las primeras posiciones; gemma (7B) queda en la franja baja"],
  ["Gemma alojado", "gemma4:31b-cloud (31B, BF16 sin cuantizar)", "Única referencia en la nube, de acceso gratuito"],
  ["Llama", "llama3.1:8b · llama3.2:latest (3B)", "El de 3B es el candidato a cribado masivo"],
  ["Qwen", "qwen2.5:14b · qwen3:8b", "Franja intermedia, movimiento escaso con RAG"],
  ["Mistral", "mistral-nemo:latest (12B)", "Único que empeora de forma apreciable con RAG"],
  ["GPT-OSS", "gpt-oss:20b", "Incorporado solo en el estudio principal"],
  ["Nemotron / DeepSeek", "nemotron-mini:4b · deepseek-r1:1.5b", "Los dos más débiles; se descartan para producción"],
];
tabla(s, ["Familia", "Configuraciones evaluadas", "Observación"],
  fam.map((f) => [{ t: f[0], bold: true }, f[1], f[2]]),
  { colW: [2.5, 5.8, 3.8], rowH: 0.5, fsBody: 11, name: "modelos" });
s.addText("Doce modelos en trece configuraciones sobre el corpus exploratorio, y trece modelos en veintiséis grupos sobre el corpus principal, cada modelo medido con recuperación contextual y sin ella. Entre un conjunto y otro se incorporan gemma4:12b-mlx y gpt-oss:20b, y se retira la compilación GGUF simple de gemma4:31b.",
  { x: 0.6, y: 5.3, w: 12.1, h: 0.85, fontSize: 12.5, color: C.text1, isTextBox: true, margin: 0 });
notas(s, "Lámina de respaldo. En la pasada rápida basta decir trece modelos, de 1,5B a 31B, en siete familias.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "4. Diseño experimental" });
chip(s, "CAP. 4", false);
s.addText("Qué se mide, y con qué prueba se decide", { placeholder: "title" });
const met = [
  ["Precisión", "De lo que el modelo afirmó, cuánto era cierto", "Verdaderos positivos sobre el total de propuestas"],
  ["Exhaustividad", "De lo que había que encontrar, cuánto encontró", "Verdaderos positivos sobre el total de la referencia"],
  ["F1", "Resume ambas, castigando el desequilibrio", "Media armónica: se desploma si una componente es baja"],
  ["Tasa de alucinación", "Qué proporción de lo extraído no está en el artículo", "No compara con la referencia, sino con el texto de origen"],
  ["Índice Tok/s/B", "Cuánto rendimiento da cada unidad de capacidad", "Tokens por segundo divididos por miles de millones de parámetros"],
  ["Memoria de vídeo", "Qué modelos caben en cada máquina", "Fue el factor limitante del estudio"],
];
tabla(s, ["Métrica", "A qué pregunta responde", "Cómo se calcula"],
  met.map((m) => [{ t: m[0], bold: true }, m[1], m[2]]),
  { colW: [2.6, 4.9, 4.6], rowH: 0.43, fsBody: 11, name: "metricas" });
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.35, w: 12.1, h: 1.75, rectRadius: 0.06,
  fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2, width: 1 }, objectName: "conv" });
s.addText("TRES CONVENCIONES QUE CAMBIAN LAS CIFRAS, Y QUE POR ESO SE DECLARAN", { x: 0.9, y: 4.5, w: 11.5, h: 0.26, margin: 0,
  fontSize: 10, bold: true, charSpacing: 1.2, color: THEME.colors.accent1, isTextBox: true });
s.addText([
  { text: "Agregación por artículo. ", options: { bold: true } },
  { text: "Las cifras se agregan dentro de cada artículo y después se promedian, de modo que cada artículo pesa lo mismo. Es la única convención del informe.", options: { breakLine: true } },
  { text: "Extracción vacía. ", options: { bold: true } },
  { text: "Una implementación previa asignaba F1 igual a 1 cuando el modelo no extraía nada, lo que premiaba el silencio. Aquí vale 0, y se reserva el 1 para el acierto vacío legítimo.", options: { breakLine: true } },
  { text: "La latencia no caracteriza al modelo. ", options: { bold: true } },
  { text: "Es reloj de pared bajo concurrencia e incluye espera en cola, así que no es comparable entre filas. Por eso se compara el índice Tok/s/B." },
], { x: 0.9, y: 4.8, w: 11.5, h: 1.2, margin: 0, fontSize: 11.5, color: C.text1, isTextBox: true });
notas(s, "Si preguntan por qué las cifras difieren de otras publicadas, la respuesta está aquí: la convención de agregación y la del vacío cambian el número.");

/* ========================= 5. RESULTADOS ========================= */

pres.addSection({ title: "5. Resultados" });

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "5. Resultados" });
chip(s, "CAP. 5", false);
s.addText("Resultado principal: trece modelos sobre corpus real", { placeholder: "title" });
const t7 = [
  ["gemma4:31b-cloud", "nube", "82,13 %", "82,94 %", "+0,81 pp", "no"],
  ["gemma4:31b-mlx", "local", "81,47 %", "82,44 %", "+0,97 pp", "no"],
  ["gemma4:12b-mlx", "local", "77,67 %", "79,96 %", "+2,29 pp", "no"],
  ["gpt-oss:20b", "local", "75,41 %", "77,08 %", "+1,67 pp", "no"],
  ["gemma4:latest (9B)", "local", "75,33 %", "77,86 %", "+2,53 pp", "no"],
  ["qwen2.5:14b", "local", "69,61 %", "70,31 %", "+0,69 pp", "no"],
  ["llama3.1:8b", "local", "69,17 %", "71,48 %", "+2,31 pp", "no"],
  ["qwen3:8b", "local", "69,03 %", "68,98 %", "−0,05 pp", "no"],
  ["llama3.2:latest (3B)", "local", "63,25 %", "69,98 %", "+6,73 pp", "no"],
  ["mistral-nemo (12B)", "local", "60,63 %", "56,35 %", "−4,29 pp", "no"],
  ["gemma:latest (7B)", "local", "59,55 %", "59,58 %", "+0,03 pp", "no"],
  ["deepseek-r1:1.5b", "local", "28,73 %", "30,80 %", "+2,07 pp", "no"],
  ["nemotron-mini:4b", "local", "28,29 %", "40,55 %", "+12,26 pp", "sí"],
];
tabla(s, ["Modelo", "Ejecución", "F1 sin RAG", "F1 con RAG contextual", "Δ RAG", "¿Significativo?"],
  t7.map((r, i) => {
    const hl = (i === 0 || i === 1 || i === 12);
    const f = hl ? "DCEFEE" : undefined;
    return [
      { t: r[0], bold: hl, fill: f },
      { t: r[1], fill: f },
      { t: r[2], bold: i === 1, fill: f, color: i === 1 ? THEME.colors.accent1 : undefined },
      { t: r[3], fill: f },
      { t: r[4], bold: i === 12, fill: f, color: i === 12 ? THEME.colors.accent1 : undefined },
      { t: r[5], bold: i === 12, fill: f, color: i === 12 ? THEME.colors.accent1 : undefined },
    ];
  }),
  { colW: [3.3, 1.6, 2.0, 2.5, 1.5, 1.2], rowH: 0.33, fsBody: 10.5, fsHead: 11, name: "tabla7" });
nota(s, "Corpus real de 120 artículos, 113 observaciones por grupo tras excluir siete que también son fuente de los ejemplares de la base de conocimientos. ANOVA F = 119,75 con p < 10⁻³⁰⁰; 217 de 325 comparaciones de Tukey resultan significativas. La significancia de la última columna es la del modelo respecto de sí mismo al añadir recuperación.", 6.15);
notas(s, "Esta es la tabla madre del trabajo. Señalar solo tres filas: la nube arriba, el mejor local a menos de un punto, y nemotron abajo como único delta significativo.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "5. Resultados" });
content(s, "CAP. 5",
  "Precisión de nivel comercial desde infraestructura propia",
  [
    "Sobre el corpus periodístico, gemma4:31b-mlx en local alcanza 81,47 % de F1, y 82,44 % con base de conocimientos contextual. La hipótesis fijaba 70 %.",
    "Sobre el corpus del dominio AML/KYC el mismo modelo obtiene 80,57 % con intervalo de confianza al 95 % de [74,22 %, 86,92 %], y 90,16 % si la medición se restringe a las categorías que ese corpus anota.",
    "No hubo ninguna extracción fallida en ninguno de los dos corpus, sobre los sesenta registros del corpus del dominio.",
    "llama3.2 de 3B logra 63,25 % sobre este corpus, y su índice de eficiencia, medido en la corrida de hardware, es de 26,44 tokens por segundo y por mil millones de parámetros: ochenta veces el del modelo de 31B. Es el candidato natural para el filtrado previo.",
  ],
  V.ranking,
  [["81,47 %", "F1 local sobre el corpus periodístico"], ["> 70 %", "umbral de la hipótesis, superado"]]);
notas(s, "El umbral de la hipótesis se supera en los dos corpus, y directamente, sin corrección alguna, en el periodístico.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "5. Resultados" });
content(s, "CAP. 5",
  "La soberanía cuesta menos de un punto porcentual",
  [
    "Sobre el corpus principal, la variante en la nube alcanza 82,13 % de F1 y la local, compilación MLX, 81,47 %. La diferencia queda por debajo de un punto.",
    "Sobre el corpus exploratorio de quince artículos la relación se invierte —local 69,12 % frente a 66,99 %—, pero es el experimento de menor potencia estadística.",
    "Lo que el estudio sostiene es lo primero: la soberanía cuesta menos de un punto de F1 sobre el corpus de mayor potencia. No que salga gratis.",
    "Es un precio razonable en un entorno regulado, y se paga a cambio de no transferir texto de clientes a un tercero ni suscribir acuerdos de tratamiento de datos.",
  ],
  V.soberania,
  [["82,13 %", "nube, con el dato en un tercero", THEME.colors.accent3],
   ["81,47 %", "local, con el dato en casa", THEME.colors.accent1]]);
notas(s, "Este es el resultado que responde la pregunta del encuadre: la privacidad total no se paga con precisión.");

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "5. Resultados" });
content(s, "CAP. 5",
  "El RAG contextual salva al modelo más débil, y solo a ese",
  [
    "En nemotron-mini:4b la mejora va de 28,29 % a 40,55 %, es decir +12,26 pp, y es el único de los trece que alcanza significancia tras corregir por comparaciones múltiples (p < 0,001).",
    "El segundo delta bruto, llama3.2 con +6,73 pp, no se distingue del azar una vez aplicada esa corrección (p = 0,2334).",
    "En los modelos de 31B el efecto cae por debajo de un punto: ya traen internalizadas las guías de desambiguación, y el contexto extra consume ventana de atención sin aportar.",
    "La correlación entre capacidad y beneficio no es significativa (ρ = −0,09; p = 0,775) y depende casi enteramente de ese modelo. La conclusión correcta es que beneficia a uno, no a los débiles en general.",
  ],
  V.rag,
  [["+12,26 pp", "único delta significativo"], ["+0,97 pp", "en el modelo de 31B local"]]);
notas(s, "Resistir la tentación de generalizar: retirado nemotron de la muestra, la correlación se desvanece. El trabajo lo dice así.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "5. Resultados" });
chip(s, "CAP. 5", false);
s.addText("Alucinaciones: dónde aparecen y por qué importan", { placeholder: "title" });
bullets2(s, 0.6, 1.45, 5.75, 3.9, [
  "La tasa de alucinación no compara con la anotación de referencia sino con el artículo: mide qué proporción de lo extraído no aparece en el texto de origen. En cumplimiento normativo, una entidad inventada en un informe de sanciones cuesta más que una omitida.",
  "Sobre los sesenta y un grupos medidos el rango va de cero, en las variantes alojadas de gemma4:31b, hasta 21,59 % en deepseek-r1:1.5b con recuperación por diccionario.",
  "Veintiocho de esos sesenta y un grupos quedan por debajo del 1 %, y entre ellos todas las configuraciones de mayor capacidad: la instrucción de restringir la extracción al artículo funciona en casi la mitad de los casos.",
  "El problema se concentra en los dos modelos más pequeños: deepseek-r1:1.5b oscila entre 11,23 % y 21,59 %, y nemotron-mini:4b entre 7,14 % y 14,75 %. Es el defecto que los descarta para producción, más que su exhaustividad.",
]);
s.addText([
  { text: "TAXONOMÍA DE ERRORES", options: { fontSize: 10, bold: true, charSpacing: 1.2, color: THEME.colors.accent1, breakLine: true, paraSpaceAfter: 6 } },
  { text: "Error de límite. ", options: { bold: true } },
  { text: "Todo emparejamiento con similitud entre 50 y 85. Buena parte no son fallos del modelo sino de la referencia: «José María Aznar» frente a su versión con codificación corrupta.", options: { breakLine: true, paraSpaceAfter: 7 } },
  { text: "Confusión de tipo. ", options: { bold: true } },
  { text: "«Estados Unidos» o «Valencia» extraídos como localización donde la anotación registra organización. Es divergencia de convención, no incomprensión.", options: { breakLine: true, paraSpaceAfter: 7 } },
  { text: "Omisión de abreviatura. ", options: { bold: true } },
  { text: "Variantes de sigla como «EFE» y «EFECOM», que designan lo mismo con 66,7 de similitud.", options: { breakLine: true, paraSpaceAfter: 7 } },
  { text: "Alucinación extrínseca. ", options: { bold: true } },
  { text: "La categoría grave: entidades ausentes del texto, procedentes de la memoria de entrenamiento." },
], { x: 6.9, y: 1.45, w: 5.8, h: 3.9, fontSize: 11.5, color: C.text1, isTextBox: true, margin: 0 });
stats(s, [["0,00–0,16 %", "en gemma4:31b-mlx, el recomendado"], ["21,59 %", "en el peor caso medido", THEME.colors.accent3]], 5.45, 0.6, 5.75);
notas(s, "La taxonomía es honesta en los dos sentidos: parte de los errores contados son defectos de la anotación de origen, no del modelo.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "5. Resultados" });
chip(s, "CAP. 5", false);
s.addText("Eficiencia en hardware soberano y costo por artículo", { placeholder: "title" });
tabla(s, ["Modelo", "Memoria de vídeo", "Tokens/s", "Parámetros", "Índice Tok/s/B", "Costo estimado por artículo"],
  [
    ["gemma4:31b", "18 795 MB", "10,23", "31B", "0,33", "USD 0,052"],
    ["gemma4:31b-mlx", "24 607 MB", "22,80", "31B", { t: "0,74", bold: true }, "USD 0,052"],
    [{ t: "llama3.2 (3B)", bold: true, fill: "DCEFEE" },
     { t: "4 018 MB", fill: "DCEFEE" },
     { t: "79,35", fill: "DCEFEE" },
     { t: "3B", fill: "DCEFEE" },
     { t: "26,44", bold: true, fill: "DCEFEE", color: THEME.colors.accent1 },
     { t: "USD 0,052", fill: "DCEFEE" }],
  ],
  { colW: [2.8, 2.1, 1.6, 1.6, 2.0, 2.0], rowH: 0.42, name: "tabla8" });
s.addText([
  { text: "Por qué el costo es idéntico en las tres filas. ", options: { bold: true, color: THEME.colors.accent1 } },
  { text: "No mide cómputo: es el costo amortizado de la infraestructura, unos USD 0,050 por artículo de amortización del equipo a un año más unos USD 0,002 de electricidad. Al ser un costo de capital repartido entre el volumen procesado, no varía con el modelo. Lo que sí varía es cuántos artículos permite procesar ese mismo hardware en el mismo tiempo, y de eso da cuenta el índice Tok/s/B.",
    options: { color: C.text1 } },
], { x: 0.6, y: 3.3, w: 12.1, h: 1.1, fontSize: 12.5, isTextBox: true, margin: 0 });
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.5, w: 12.1, h: 1.6, rectRadius: 0.06,
  fill: { color: THEME.colors.accent2 }, line: { width: 0 }, objectName: "dosniveles" });
s.addText("LA ASIMETRÍA QUE HABILITA UNA ARQUITECTURA EN DOS NIVELES", { x: 0.9, y: 4.66, w: 11.5, h: 0.26, margin: 0,
  fontSize: 10, bold: true, charSpacing: 1.2, color: THEME.colors.accent6cl, isTextBox: true });
s.addText("Un modelo de 3B rinde ochenta veces más por unidad de capacidad instalada que uno de 31B, aun siendo peor en F1. Como el costo de un falso negativo en el cribado es muy inferior al de un falso positivo confirmado, conviene cribar con el pequeño y validar con el grande. Las cifras económicas son estimaciones: dependen del precio del equipo, su vida útil, la tarifa eléctrica y el volumen realmente procesado.",
  { x: 0.9, y: 4.96, w: 11.5, h: 1.0, margin: 0, fontSize: 12.5, color: "FFFFFF", isTextBox: true });
notas(s, "Ochenta a uno es la cifra que justifica la arquitectura de producción de la lámina de cierre.");

/* ========================= 6. CONCLUSIONES ========================= */

pres.addSection({ title: "6. Conclusiones" });

s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: "6. Conclusiones" });
content(s, "CAP. 6-7",
  "Viabilidad operativa y reducción de costos",
  [
    "El riesgo de fuga desaparece por construcción: el texto nunca sale de la organización, y con él desaparece la necesidad de acuerdos de tratamiento de datos con terceros.",
    "El costo unitario por artículo cae un 99,4 % frente a la revisión manual, lo que equivale a una reducción del 60 % al 80 % del costo operativo total, que incluye la supervisión humana.",
    "Las alucinaciones van de cero, en las variantes alojadas de gemma4:31b, hasta 21,59 % en deepseek-r1:1.5b con recuperación por diccionario; veintiocho de sesenta y un grupos quedan bajo el 1 %.",
    "El objetivo de mantenerlas bajo el 5 % se cumple en el modelo recomendado, entre 0,00 % y 0,16 %, pero no en el catálogo completo. Por eso los dos modelos pequeños se descartan.",
  ],
  V.viabilidad,
  [["−99,4 %", "costo unitario, estimación declarada"], ["28 de 61", "grupos bajo el 1 % de alucinación"]]);
notas(s, "Separar el 99,4 % del costo unitario directo del 60-80 % del costo operativo total, que incluye al analista.");

s = pres.addSlide({ masterName: "ANCHO", sectionTitle: "6. Conclusiones" });
chip(s, "RIGOR", false);
s.addText("Limitaciones declaradas, y qué cambia cada una", { placeholder: "title" });
const lim = [
  ["Fuga de ejemplares", "En el modo combinado, el 94 % de los ejemplares recuperados procede de otro artículo del propio corpus de evaluación.", "La mejora del RAG contextual no puede descartarse como beneficio parcial de esa fuga."],
  ["Observaciones apareadas", "Los veintiséis grupos evalúan los mismos 113 artículos, de modo que las observaciones no son independientes.", "El ANOVA resulta conservador; el contraste se repite con Friedman y el rechazo se sostiene."],
  ["Cifras económicas", "Tanto los USD 8,75 de la revisión manual como los USD 0,052 del sistema son estimaciones internas, no mediciones.", "El ahorro real depende de cuánto se reduzca el volumen que llega a revisión humana."],
  ["Latencia no comparable", "Es reloj de pared bajo concurrencia variable, no tiempo de inferencia.", "No se usa para comparar modelos; se compara el índice Tok/s/B."],
  ["Potencia del corpus N=30", "Con treinta artículos por grupo, la potencia frente al efecto observado es del 8 %.", "Los datos no permiten distinguir ambas compilaciones; no acreditan que sean iguales."],
  ["Categoría de localizaciones", "El prompt la solicita en los tres corpus, pero la anotación de referencia quedó vacía por un defecto ya corregido de la preparación de datos.", "Parte de la confusión de tipo medida proviene de ahí, no del modelo."],
  ["Alcance del controlador", "El AIMD reacciona a límites de tasa y a rachas de error, pero no recibe telemetría de memoria.", "No previene el agotamiento de memoria: eso se contiene ejecutando un modelo por turno."],
];
tabla(s, ["Limitación", "En qué consiste", "Qué implica para la lectura de los resultados"],
  lim.map((l) => [{ t: l[0], bold: true }, l[1], l[2]]),
  { colW: [2.4, 5.0, 4.7], rowH: 0.56, fsBody: 10.5, name: "limitaciones" });
nota(s, "Ninguna de estas limitaciones se descubrió en la revisión: todas están declaradas en el propio informe, con el apartado donde se discuten.", 6.3);
notas(s, "Lámina deliberada: adelantarse a las preguntas difíciles vale más que esperarlas. Si el tiempo aprieta, dejarla para la ronda de preguntas.");

s = pres.addSlide({ masterName: "OSCURA", sectionTitle: "6. Conclusiones" });
chip(s, "CIERRE", true);
s.addText("Lo que queda demostrado, y lo que viene", { placeholder: "title" });
s.addText("Arquitectura propuesta para producción, en dos niveles: llama3.2 de 3B filtra el flujo masivo a alta velocidad y descarta los falsos positivos evidentes; gemma4:31b-mlx analiza en profundidad solo los casos sospechosos, con máxima precisión y sin fuga de datos.",
  { placeholder: "body" });
const road = [
  ["Fase 1", "Ampliar la base de conocimientos de 5 a más de 10 dominios del ecosistema AML latinoamericano: UAF chilena, resoluciones de la CMF y sanciones OFAC en español"],
  ["Fase 2", "Ajuste fino supervisado con LoRA sobre ejemplares del dominio, para cubrir los 4,43 puntos que separan el resultado sobre el corpus del dominio de la meta interna de 85 % de F1"],
  ["Fase 3", "Ensamble en producción, con votación ponderada entre el modelo rápido y el de mayor capacidad"],
  ["Fase 4", "Despliegue piloto con feeds de noticias en tiempo real para oficiales de cumplimiento"],
  ["Fase 5", "Soporte multiidioma, partiendo por el portugués para cobertura regional"],
];
road.forEach((r, i) => {
  const y = 2.85 + i * 0.66;
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 1.1, h: 0.42, rectRadius: 0.06,
    fill: { color: THEME.colors.accent6 }, line: { width: 0 }, objectName: "fase-" + i });
  s.addText(r[0], { x: 0.6, y, w: 1.1, h: 0.42, margin: 0, align: "center", valign: "middle",
    fontSize: 11, bold: true, color: THEME.colors.dk2, isTextBox: true });
  s.addText(r[1], { x: 1.85, y: y + 0.02, w: 10.85, h: 0.4, margin: 0, fontSize: 12.5,
    color: THEME.colors.lt2, valign: "middle", isTextBox: true });
});
s.addText("Viabilidad demostrada por encima del umbral declarado, soberanía garantizada en operación desconectada y costo operativo reducido: las tres afirmaciones de la hipótesis quedan contrastadas sobre corpus real.",
  { x: 0.6, y: 6.3, w: 12.1, h: 0.5, fontSize: 12, italic: true, color: THEME.colors.accent6, isTextBox: true, margin: 0 });
notas(s, "Cierre: volver al encuadre del curso. Una función organizacional automatizada, con el dato bajo control y un camino de mejora ya trazado.");

/* --- cierre / preguntas --- */
s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "6. Conclusiones" });
s.addText("GRACIAS · ESPACIO DE PREGUNTAS Y COMENTARIOS", { placeholder: "kicker" });
s.addText("Se puede automatizar sin entregar el dato", { placeholder: "title" });
s.addText([
  { text: "Trece modelos abiertos y 120 artículos reales: 81,47 % de F1 en local sobre el corpus periodístico, a menos de un punto de la mejor alternativa en la nube, y 90,16 % sobre el corpus del dominio AML/KYC.", options: { breakLine: true } },
  { text: "El código, los corpus anotados y los resultados de cada corrida son reproducibles desde su fichero de configuración.", options: { fontSize: 13, color: THEME.colors.secOsc } },
], { placeholder: "sub" });
s.addText([
  { text: "Eduardo Mauricio Ahumada Gallardo", options: { bold: true, color: "FFFFFF", breakLine: true } },
  { text: "Magíster en Tecnologías de la Información · Universidad Técnica Federico Santa María", options: { breakLine: true } },
  { text: "Borrador de proyecto final · Aplicaciones de inteligencia artificial · 3 de octubre de 2026" },
], { placeholder: "meta" });
notas(s, "Cerrar con la frase del título y abrir preguntas. Preguntas probables: por qué no BERT, si el dato de costo está medido, qué pasa con la fuga de ejemplares, y si esto corre en un equipo corriente.");

/* ============================ escribir ============================ */

(async () => {
  const out = path.join(DIR, "Tesina_MTI_IA_Aplicada.pptx");
  await pres.writeFile({ fileName: out });
  const { applyTheme } = require("/root/.claude/skills/synced/5c749a67-a47d-4ee9-ba16-557e4d67b48a_ed57fffc-bc2f-4b80-9574-da57507ab289/pptx/scripts/apply_theme.js");
  await applyTheme(out, THEME);
  console.log("OK ->", out);
})();

# REFERENCIA DE DATASETS NER Y REGISTRO OPENSANCTIONS
## Análisis Comparativo de Corpuses para NLP de Cumplimiento y Sanciones

Este documento recopila la información sobre datasets de Named Entity Recognition (NER) similares a Kleptotrace/CoNLL-2002 y el registro de fuentes de OpenSanctions para su posterior incorporación en el Informe de Avance del Magíster MTI.

---

## 📋 1. DATASETS ACADÉMICOS Y CORPORATIVOS NER SIMILARES

La siguiente lista detalla los corpuses de evaluación de extracción de entidades más representativos en los dominios financiero, legal y de privacidad. Estos datasets sirven como línea base (*baseline*) para justificar la escala de pruebas en la tesina:

### 📊 FiNER-139 (Financial Named Entity Recognition)
* **Cantidad de Registros:** **~1,100,000 sentencias** (Masivo).
* **Tipo/Clases:** 139 etiquetas financieras basadas en taxonomías XBRL de la SEC.
* **Uso en MTI:** Es el benchmark principal para validar la extracción de entidades corporativas y de firmas financieras complejas en informes públicos de la SEC (10-K/10-Q).

### 📰 CoNLL-2003 (Gold Standard Académico)
* **Cantidad de Registros:** **20,747 sentencias** en total:
  * *Entrenamiento (Train):* 14,042 sentencias
  * *Validación (Dev):* 3,251 sentencias
  * *Prueba (Test):* 3,454 sentencias
* **Tipo/Clases:** Personas (PER), Organizaciones (ORG), Locaciones (LOC), Misceláneos (MISC).
* **Uso en MTI:** Sirve como el conjunto de prueba base para medir la capacidad de generalización zero-shot de modelos como GLiNER sobre noticias del ámbito general de Reuters.

### 🌐 MultiCoNER (Complex Named Entity Recognition)
* **Cantidad de Registros:** **~1,500 sentencias por idioma** (Total acumulado de 26 millones de tokens).
* **Tipo/Clases:** Entidades complejas, ambiguas y nombres propios multilingües.
* **Uso en MTI:** Justifica la robustez de los algoritmos ante nombres de PEPs o testaferros con ortografía ambigua o procedentes de traducciones cirílicas/árabes.

### ⚡ Flare-NER (Financial Language Evaluation)
* **Cantidad de Registros:** **~10,000 sentencias**.
* **Tipo/Clases:** Personas (PER), Organizaciones (ORG), Locaciones (LOC).
* **Uso en MTI:** Evaluación dedicada de NLP en contratos, acuerdos comerciales e informes de fusiones y adquisiciones.

### 🛡️ AI4Privacy PII Dataset
* **Cantidad de Registros:** **~1,500,000 sentencias** (Masivo).
* **Tipo/Clases:** Información Personal Identificable (PII) financiera (nombres de cuenta, bancos, transferencias, transacciones).
* **Uso en MTI:** Representa el corpus ideal para evaluar la anonimización de datos en flujos de auditoría previos a la inspección por entes reguladores.

---

## 🌐 2. REGISTRO DE DATASETS CONSOLIDADOS EN OPENSANCTIONS

OpenSanctions organiza su base de datos bajo el modelo FollowTheMoney (FtM). A continuación, se listan las fuentes oficiales y colecciones con sus recuentos de entidades y tipos de datos:

* **`us_ofac_sdn`**: ~71,006 entidades | Tipo: Sanciones Financieras (EE.UU. OFAC) | Entidades: Personas, Organizaciones, Buques, Aeronaves, Billeteras Cripto.
* **`eu_fsf`**: ~14,622 entidades | Tipo: Sanciones Financieras (Unión Europea) | Entidades: Personas, Organizaciones, Grupos.
* **`everypolitician`**: ~120,000 entidades | Tipo: Personas Políticamente Expuestas (PEP) | Entidades: Personas, Relaciones Familiares, Cargos Públicos.
* **`interpol_red_notices`**: ~7,500 entidades | Tipo: Delitos y Capturas Internacionales (Interpol) | Entidades: Personas, Nacionalidades, Delitos Imputados.
* **`un_sc_sanctions`**: ~1,500 entidades | Tipo: Sanciones Multilaterales (ONU Security Council) | Entidades: Personas, Organizaciones, Direcciones, Pasaportes.
* **`gb_hmt`**: ~3,200 entidades | Tipo: Sanciones Financieras (Reino Unido HM Treasury) | Entidades: Personas, Organizaciones, Entidades Soberanas.
* **`warrants`**: ~80,000 entidades | Tipo: Órdenes de Arresto y Prófugos (Colección Global) | Entidades: Personas, Organizaciones, Relaciones Criminales.
* **`ch_seco_sanctions`**: ~4,500 entidades | Tipo: Sanciones Económicas (Suiza SECO) | Entidades: Personas, Organizaciones, Direcciones.
* **`ca_sema_sanctions`**: ~2,500 entidades | Tipo: Medidas Económicas Especiales (Canadá SEMA) | Entidades: Personas, Organizaciones, Relaciones Comercialess.
* **`ua_sfms`**: ~12,000 entidades | Tipo: Monitoreo Financiero y Terrorismo (Ucrania SFMS) | Entidades: Personas, Organizaciones, Direcciones.

---

## 📈 3. NOTA METODOLÓGICA SOBRE SIGNIFICANCIA ESTADÍSTICA ($N \ge 30$) Y DATASETS AUMENTADOS

Para la tesis de MTI, la adopción de datasets aumentados basados en Kleptotrace/CoNLL-2002 responde a la necesidad metodológica de validación estadística y estrés computacional:

1. **Kleptotrace/CoNLL-2002 (Original 15 registros):** La fuente original de Kleptotrace/CoNLL-2002 es un dataset público de noticias relacionadas con lavado de activos y crímenes financieros. Consiste en reportajes y recortes periodísticos en los que se extraen nombres de PEPs (Personas Expuestas Políticamente) y organizaciones ficticias o reales. Debido a que 15 artículos resultan muy pocos para una prueba estadística robusta, se optó por una estrategia de aumento de datos (*data augmentation*).

2. **Dataset 30 Registros (`benchmark_balanced_120.json`):** Fue construido preservando los primeros 15 artículos de Kleptotrace/CoNLL-2002 y complementándolos con 15 registros adicionales curados a mano. Estos incluyen casos icónicos del mundo real (ej. Cártel de Sinaloa en HSBC, Danske Bank, multas de la SEC y OFAC). Su principal fin metodológico es alcanzar el **Teorema del Límite Central (TLC)** ($N \ge 30$), permitiendo aplicar pruebas paramétricas como el análisis de varianza (ANOVA de una vía) y la prueba Tukey HSD de manera válida.

3. **Datasets 60 y 120 Registros (`benchmark_balanced_120.json` y `benchmark_balanced_120.json`):** Estos archivos fueron generados de manera algorítmica utilizando plantillas sintácticas extraídas de los patrones observados en los primeros 30 artículos. Se incorporó una lista representativa de personas y organizaciones operando en marcos regulatorios globales (OFAC, FCA, SEC, Interpol, etc.) y se aseguró el etiquetado del *ground truth* exacto para asegurar una validación determinista de Precisión y Recall. Estos datasets sirven para realizar pruebas de estrés de infraestructura y escalabilidad computacional en la inferencia LLM local.

# REFERENCIA DE DATASETS NER Y REGISTRO OPENSANCTIONS
## Análisis Comparativo de Corpuses para NLP de Cumplimiento y Sanciones

Este documento recopila la información sobre datasets de Named Entity Recognition (NER) similares a Kleptotrace y el registro de fuentes de OpenSanctions para su posterior incorporación en el Informe de Avance del Magíster MTI.

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

## 📈 3. NOTA METODOLÓGICA SOBRE SIGNIFICANCIA ESTADÍSTICA ($N \ge 30$)

Para la tesis de MTI, la adopción del dataset aumentado `data/kleptotrace_augmented_30.json` con **$N=30$ registros breves** se justifica metodológicamente en:
1. **Teorema del Límite Central (TLC):** Un tamaño de muestra $N \ge 30$ permite asegurar que la distribución muestral de las medias del F1-Score se aproxime a una distribución normal, validando la aplicación de pruebas paramétricas como el análisis de varianza (ANOVA de una vía) y la prueba de comparaciones múltiples Tukey HSD.
2. **Eficiencia Computacional en Hardware Soberano:** Al utilizar registros cortos de 1 a 2 párrafos, la latencia promedio del benchmark disminuye drásticamente, permitiendo que modelos locales de gran escala (como `gemma4:31b-mlx` en Apple Silicon M4) se evalúen secuencialmente en menos de 2 minutos sin saturar la VRAM ni el consumo eléctrico.

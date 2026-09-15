# Auditoría de Calidad y Fidelidad de Traducción — Corpus N=30 (R4)

**Fecha:** 2026-09-14 23:33:04  
**Traductor Principal:** `gemma4:31b` (19 GB)  
**Revisor Adicional:** `mistral-nemo:latest`  
**Corpus Auditado:** `repos/ner-llm-entity-benchmark/data/kleptotrace_augmented_30_es.json` (30 artículos)  

---

## 1. Resumen Ejecutivo de Métricas

| Métrica | Resultado | Veredicto |
|---|---|---|
| **Fluidez Media en Español (1 a 5)** | **4.83 / 5.00** | ✅ ÓPTIMA |
| **Fidelidad Semántica Media (1 a 5)** | **4.73 / 5.00** | ✅ ÓPTIMA |
| **Preservación Global de Entidades** | **93.6%** (117/125) | ✅ ACREDITADA |
| • Personas (`Persons`) | 100.0% (36/36) | ✅ |
| • Organizaciones (`Organizations`) | 94.2% (65/69) | ✅ |
| • Localizaciones (`Locations`) | 80.0% (16/20) | ⚠️ |

---

## 2. Detalle de Auditoría por Artículo

### Artículo ID 1: Caso OFAC UAE
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y fluida, preservando todas las entidades mencionadas en el texto original.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/3 · Locs: 1/4

### Artículo ID 2: Caso DOJ HSBC
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 2/2 · Orgs: 2/3 · Locs: 1/1

### Artículo ID 3: La EU sanciona a Belarus
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y fluida, preservando todas las entidades mencionadas en el texto original.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 1/2 · Locs: 1/1

### Artículo ID 4: Prevención del blanqueo de capitales de la SFC en Hong Kong
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 3/3 · Locs: 0/0

### Artículo ID 5: Sanciones de OFSI UK
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y fluida, preservando todas las entidades mencionadas en el texto original.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 3/3 · Locs: 1/1

### Artículo ID 6: El caso de la lista gris del FATF
- **Revisor (mistral-nemo:latest):** Fluidez: 4/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es bastante buena y preserva todas las entidades mencionadas en el texto original. Sin embargo, se podría mejorar la fluidez utilizando un lenguaje más natural en español.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 3/3 · Locs: 2/2

### Artículo ID 7: Multa de la SEC por FCPA
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 1/1

### Artículo ID 8: Caso Venezuela OFAC
- **Revisor (mistral-nemo:latest):** Fluidez: 4/5 · Fidelidad: 3/5
- **Dictamen Revisor:** La traducción es comprensible pero no captura con precisión algunos detalles del texto original. 'Billions' se traduce como 'miles de millones', lo cual puede ser una exageración, ya que 'billions' significa miles de millones. Además, el uso de la preposición 'en' antes de los países 'Switzerland' y 'Panama' no es correcto en este contexto; debería ser 'en Switzerland y Panama'.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 2/2

### Artículo ID 9: German BaFin AML
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 0/1

### Artículo ID 10: Iran Cargo Arrest
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y fluida, preservando todas las entidades mencionadas en el texto original.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 0/0

### Artículo ID 11: Detención por blanqueo de criptomonedas
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y fluida, preservando todas las entidades mencionadas en el texto original.
- **Entidades Preservadas:** Persons: 3/3 · Orgs: 1/1 · Locs: 0/0

### Artículo ID 12: Danske Bank Denmark
- **Revisor (mistral-nemo:latest):** Fluidez: 4/5 · Fidelidad: 3/5
- **Dictamen Revisor:** La traducción es comprensible pero no captura completamente el sentido original. 'Billions' se tradujo como 'miles de millones', lo que puede ser confuso ya que miles de millones son una cantidad mayor que billions. Además, la estructura gramatical del texto en español es diferente a la del texto en inglés.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 1/1 · Locs: 0/0

### Artículo ID 13: Incautación de activos de Libya
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 2/2 · Orgs: 1/1 · Locs: 1/1

### Artículo ID 14: Sanciones de la UN a la DRC
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y fluida, preservando todas las entidades mencionadas en el texto original.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 1/2 · Locs: 1/1

### Artículo ID 15: Multa a Credit Suisse por prevención del blanqueo de capitales
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 0/0

### Artículo ID 16: Caso SEC Ripple
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente.
- **Entidades Preservadas:** Persons: 2/2 · Orgs: 2/2 · Locs: 0/0

### Artículo ID 17: BNP Paribas Sudan
- **Revisor (mistral-nemo:latest):** Fluidez: 4/5 · Fidelidad: 3/5
- **Dictamen Revisor:** La traducción es comprensible pero no es del todo precisa. 'Billions of dollars' se tradujo como 'miles de millones de dólares', lo cual es correcto, pero suena menos preciso que la versión original en inglés. Además, el uso de 'CFO' sin traducir podría ser más claro si se traduce como 'Director Financiero'.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 2/2

### Artículo ID 18: Caso Abacha de Nigeria
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 0/0

### Artículo ID 19: Caso OFAC Cuba
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y fluida, preservando todas las entidades mencionadas en el texto original.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 0/0

### Artículo ID 20: Fraude de Valores de Madoff
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente con fluidez.
- **Entidades Preservadas:** Persons: 2/2 · Orgs: 1/1 · Locs: 0/0

### Artículo ID 21: Sanciones de Standard Chartered
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente con fluidez.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 4/4 · Locs: 2/2

### Artículo ID 22: Goldman Sachs 1MDB
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 3/3 · Locs: 0/0

### Artículo ID 23: SEB Sweden Baltic
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 3/3 · Locs: 0/0

### Artículo ID 24: Blanqueo de capitales en Eurasian Bank
- **Revisor (mistral-nemo:latest):** Fluidez: 4/5 · Fidelidad: 3/5
- **Dictamen Revisor:** La traducción es comprensible pero no es completamente fiel al original. 'Proper customer due diligence' se traduce como 'adecuada debida diligencia de los clientes', lo cual es algo redundante ya que 'debida diligencia' ya implica que se está hablando de una diligencia adecuada. Además, el término 'PEP clients' no se ha traducido literalmente como 'clientes PEP'. En general, la traducción podría mejorarse para ser más precisa y fluida.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 1/1

### Artículo ID 25: Incumplimientos de las sanciones de RBS
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente con fidelidad.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 5/5 · Locs: 0/0

### Artículo ID 26: Malaysia Najib Razak
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son apropiados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 0/0

### Artículo ID 27: El fraude de Luckin Coffee
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 2/2 · Locs: 0/0

### Artículo ID 28: Prevención del lavado de activos de Westpac Australia
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto fuente con fidelidad.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 3/3 · Locs: 0/0

### Artículo ID 29: El caso del CFO de Danske Bank
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del mensaje original.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 1/1 · Locs: 0/0

### Artículo ID 30: Filtración de datos de Equifax AML
- **Revisor (mistral-nemo:latest):** Fluidez: 5/5 · Fidelidad: 5/5
- **Dictamen Revisor:** La traducción es precisa y conserva todas las entidades mencionadas en el texto original. La gramática y el vocabulario utilizados son adecuados para transmitir el significado del texto de manera clara y comprensible.
- **Entidades Preservadas:** Persons: 1/1 · Orgs: 3/3 · Locs: 0/0


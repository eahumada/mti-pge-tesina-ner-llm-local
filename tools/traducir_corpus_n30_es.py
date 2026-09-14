#!/usr/bin/env python3
"""
tools/traducir_corpus_n30_es.py
--------------------------------
R4 — Traduce kleptotrace_augmented_30.json (EN) al español para el par emparejado.

Reglas de traducción:
- Solo se traduce el campo 'text' (y opcionalmente 'title')
- Las entidades (name_entities, organizations, locations) se CONSERVAN SIN CAMBIAR
  (son los ground truth; cambiarlos requeriría nueva anotación experta)
- El modelo usa gemma4:latest (disponible local, buena calidad ES)
- Se guarda el corpus en data/kleptotrace_augmented_30_es.json
- Cada artículo lleva campo 'language': 'es' y 'translated_from': 'en'

Uso:
    python3 tools/traducir_corpus_n30_es.py [--dry-run] [--resume]

El script es re-ejecutable: si ya existe traducción guardada, la reutiliza (--resume).
"""
import json
import os
import sys
import time
import logging
import argparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("traducir_n30")

_raw_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_BASE_URL = _raw_url.rstrip("/").removesuffix("/v1")
MODEL = "gemma4:31b"
INPUT_PATH = "repos/ner-llm-entity-benchmark/data/kleptotrace_augmented_30.json"
OUTPUT_PATH = "repos/ner-llm-entity-benchmark/data/kleptotrace_augmented_30_es.json"
CHECKPOINT_PATH = "repos/ner-llm-entity-benchmark/data/kleptotrace_augmented_30_es.checkpoint.json"

SYSTEM_PROMPT = (
    "Eres un traductor experto de inglés a español para textos periodísticos de finanzas y cumplimiento regulatorio. "
    "Traduce el texto que te doy al español, respetando el estilo periodístico formal. "
    "IMPORTANTE: conserva exactamente los nombres propios de personas, organizaciones y lugares tal como aparecen en el original "
    "(por ejemplo: 'Alexey Shevchenko' se mantiene igual, 'OFAC' se mantiene igual, 'Dubai' se mantiene igual). "
    "Devuelve SOLO la traducción, sin explicaciones ni aclaraciones adicionales."
)


def translate_text(text: str, model: str = MODEL, dry_run: bool = False) -> str:
    """Traduce un texto usando la API REST de Ollama directamente."""
    if dry_run:
        return f"[TRADUCCIÓN SIMULADA] {text[:80]}..."

    import requests as _req
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Traduce este texto al español:\n\n{text}"},
        ],
        "options": {"temperature": 0.1, "seed": 42, "num_predict": 1024},
        "stream": False,
    }
    try:
        url = f"{OLLAMA_BASE_URL}/api/chat"
        resp = _req.post(url, json=payload, timeout=300)
        resp.raise_for_status()
        translated = resp.json()["message"]["content"].strip()
        if not translated:
            logger.warning("Respuesta vacía del modelo, usando texto original")
            return text
        return translated
    except Exception as e:
        logger.error(f"Error en traducción ({url}): {e}")
        return text  # fallback: texto original si falla


def main():
    parser = argparse.ArgumentParser(description="Traduce corpus N=30 EN→ES")
    parser.add_argument("--dry-run", action="store_true", help="No llama a Ollama, simula traducción")
    parser.add_argument("--resume", action="store_true", help="Retoma desde checkpoint si existe")
    parser.add_argument("--model", default=MODEL, help="Modelo Ollama a usar para la traducción (default: gemma4:31b)")
    parser.add_argument("--input", default=INPUT_PATH, help="Corpus fuente")
    parser.add_argument("--output", default=OUTPUT_PATH, help="Corpus destino")
    args = parser.parse_args()

    # Cargar corpus fuente
    logger.info(f"Cargando corpus fuente: {args.input}")
    raw = json.load(open(args.input, encoding="utf-8"))
    articles = raw.get("dataset", raw.get("articles", raw.get("data", raw if isinstance(raw, list) else [])))
    logger.info(f"Artículos a traducir: {len(articles)}")
    logger.info(f"Modelo para traducción: {args.model}")

    # Cargar checkpoint si existe y --resume
    checkpoint = {}
    if args.resume and os.path.exists(CHECKPOINT_PATH):
        checkpoint = json.load(open(CHECKPOINT_PATH, encoding="utf-8"))
        logger.info(f"Reanudando desde checkpoint: {len(checkpoint)} artículos ya traducidos")

    translated_articles = []
    for i, art in enumerate(articles):
        art_id = str(art.get("article_id", i))
        
        # Reutilizar del checkpoint si existe
        if art_id in checkpoint:
            logger.info(f"[{i+1:02d}/{len(articles)}] id={art_id} → reutilizado del checkpoint")
            translated_articles.append(checkpoint[art_id])
            continue

        original_text = art.get("text", art.get("caption", ""))
        original_title = art.get("title", "")

        logger.info(f"[{i+1:02d}/{len(articles)}] id={art_id} Traduciendo texto ({len(original_text)} chars)...")
        t0 = time.time()
        translated_text = translate_text(original_text, model=args.model, dry_run=args.dry_run)
        elapsed = time.time() - t0
        logger.info(f"  → {len(translated_text)} chars en {elapsed:.1f}s")

        # Traducir también el título (corto, rápido)
        if original_title and not args.dry_run:
            translated_title = translate_text(original_title, model=args.model, dry_run=args.dry_run)
        else:
            translated_title = original_title

        # Construir artículo traducido
        # IMPORTANTE: ground truth (name_entities, organizations, locations) SIN CAMBIAR
        translated_art = {
            **art,
            "text": translated_text,
            "title": translated_title,
            # Campo caption para compatibilidad con el pipeline (main.py usa 'caption')
            "caption": translated_text,
            "language": "es",
            "translated_from": "en",
            "original_text": original_text,
            "original_title": original_title,
        }

        # Si el artículo original usa 'caption' en vez de 'text', actualizar
        if "caption" in art:
            translated_art["caption"] = translated_text

        translated_articles.append(translated_art)

        # Guardar checkpoint incremental
        checkpoint[art_id] = translated_art
        json.dump(checkpoint, open(CHECKPOINT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        
        # Pausa breve para no saturar Ollama
        if not args.dry_run:
            time.sleep(0.5)

    # Construir corpus final
    output_corpus = {
        "dataset": translated_articles,
        "metadata": {
            "source": args.input,
            "target_language": "es",
            "translation_model": MODEL if not args.dry_run else "dry-run",
            "translation_date": time.strftime("%Y-%m-%d"),
            "total_articles": len(translated_articles),
            "note": (
                "Corpus traducido automáticamente EN→ES para R4 (par emparejado). "
                "Los ground truth (name_entities, organizations, locations) NO se tradujeron: "
                "son nombres propios que el modelo debe reconocer en su forma original. "
                "La reserva de que es traducción automática se declara en el informe."
            ),
        },
    }

    # Guardar corpus final
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_corpus, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ Corpus ES guardado en: {args.output}")
    logger.info(f"   Total artículos: {len(translated_articles)}")

    # Limpieza del checkpoint
    if not args.dry_run and os.path.exists(CHECKPOINT_PATH):
        os.remove(CHECKPOINT_PATH)
        logger.info("   Checkpoint eliminado (completado)")

    # Verificación rápida
    logger.info("\n--- VERIFICACIÓN ---")
    for art in translated_articles[:3]:
        logger.info(f"  id={art['article_id']} texto_es={art['text'][:100]}...")
        logger.info(f"  entities={art.get('name_entities', [])} orgs={art.get('organizations', [])} locs={art.get('locations', [])}")


if __name__ == "__main__":
    main()

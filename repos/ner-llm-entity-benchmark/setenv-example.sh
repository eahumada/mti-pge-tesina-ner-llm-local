#!/bin/bash
# Template for environment variables - NER-LLM Entity Benchmark
# Copy this file to '.setenv.sh' and fill in your real API credentials.
# DO NOT commit '.setenv.sh' containing actual secrets to Git.

# Google AI Studio / Gemini API credentials
export GEMINI_API_KEY=""
export GOOGLE_API_KEY=""

# Google Cloud Platform (Vertex AI SDK optional configuration)
export GOOGLE_CLOUD_PROJECT=""
export GOOGLE_CLOUD_LOCATION="us-central1"

# OpenAI API credentials (optional)
export OPENAI_API_KEY=""
export OPENAI_BASE_URL="" # Optional proxy/Azure endpoint URL

# Anthropic API credentials (optional)
export ANTHROPIC_API_KEY=""

# Ollama Endpoint Configuration (optional override)
export OLLAMA_BASE_URL="http://localhost:11434"

# Redis Pub/Sub Queue (optional override)
export REDIS_URL="redis://localhost:6379"

echo "ℹ️ Template loaded. Please make sure to fill in actual API keys in your active .setenv.sh script."

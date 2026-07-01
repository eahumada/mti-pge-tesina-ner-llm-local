#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=================================================="
echo "🚀 NER-LLM Entity Benchmark Environment Setup"
echo "=================================================="

# Helper function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Detect Operating System
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Windows;;
    MINGW*)     MACHINE=Windows;;
    MSYS_NT*)   MACHINE=Windows;;
    *)          MACHINE="Unknown:${OS}"
esac

echo "Detected OS: ${MACHINE}"

# 2. Install Native Dependencies (Ollama)
if ! command_exists ollama; then
    echo "Ollama is not installed. Attempting installation for ${MACHINE}..."
    if [ "${MACHINE}" = "Mac" ]; then
        if command_exists brew; then
            echo "Installing Ollama via Homebrew..."
            brew install --cask ollama
        else
            echo "Homebrew not found. Please install Ollama manually from: https://ollama.com/download"
        fi
    elif [ "${MACHINE}" = "Linux" ]; then
        echo "Installing Ollama via official installer script..."
        curl -fsSL https://ollama.com/install.sh | sh
    elif [ "${MACHINE}" = "Windows" ]; then
        echo "Please install Ollama for Windows manually from: https://ollama.com/download"
        echo "If using WSL (Windows Subsystem for Linux), you can install Ollama using:"
        echo "  curl -fsSL https://ollama.com/install.sh | sh"
    fi
else
    echo "✅ Ollama is already installed: $(ollama --version 2>/dev/null || echo 'Installed')"
fi

# 3. Initialize Python Virtual Environment (venv)
echo "Setting up Python virtual environment (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created successfully."
else
    echo "✅ Virtual environment 'venv' already exists."
fi

# 4. Activate Virtual Environment and Install Dependencies
echo "Activating virtual environment..."
# Determine activation script based on shell/OS
if [ "${MACHINE}" = "Windows" ]; then
    if [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
else
    source venv/bin/activate
fi

echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

echo "Installing requirements from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Python dependencies installed successfully."
else
    echo "⚠️ requirements.txt not found. Skipping pip install."
fi

# 5. Model Verification
echo "Verifying local Ollama models..."
if command_exists ollama; then
    # Start Ollama service if not running (Linux-only, Mac normally runs app)
    if [ "${MACHINE}" = "Linux" ]; then
        if ! pgrep -x "ollama" >/dev/null; then
            echo "Starting Ollama service..."
            ollama serve > /dev/null 2>&1 &
            sleep 3
        fi
    fi
    
    # Pull default model (gemma4 or similar)
    echo "Pulling default evaluation model (gemma4)..."
    ollama pull gemma4 || echo "⚠️ Could not pull gemma4 model. Please ensure Ollama service is running."
else
    echo "⚠️ Ollama command line utility not available. Skipping model pull."
fi

echo "=================================================="
echo "🎉 Setup complete! To activate the environment run:"
echo "   source venv/bin/activate"
echo "=================================================="

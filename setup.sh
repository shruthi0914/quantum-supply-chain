#!/bin/bash

# Quantum Supply Chain Agent: One-Click Setup
echo "="*60
echo "🚀 Initializing Quantum Supply Chain Agentic AI System"
echo "="*60

# 1. Create venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate and install
source venv/bin/activate
echo "🔧 Installing high-performance dependencies..."
pip install --upgrade pip
pip install -r requirements.txt --quiet

# 3. Initialize data directories
mkdir -p data/raw
mkdir -p data/vector_store/chroma_db

# 4. Check for Olist data
if [ -z "$(ls -A data/raw)" ]; then
    echo "⚠️  Note: No Olist CSVs found in data/raw. Running with simulated data."
else
    echo "📊 Olist datasets detected. Ready for full ingestion."
fi

# 5. Run Demo
echo "🏁 Running System Simulation..."
python3 demo_run.py

echo "="*60
echo "✅ Setup Complete. To launch the UI, run: docker-compose up --build"
echo "="*60

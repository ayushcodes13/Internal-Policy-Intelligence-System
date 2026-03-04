#!/bin/bash
# run_app.sh
# Script to run the Streamlit frontend for the Internal Policy Intelligence System

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Starting the Internal Policy Intelligence System frontend..."
streamlit run app.py

#!/bin/bash

# Create the ChromaDB
echo "Creating the email databse..."
echo "Now at" 
pwd
python /app/create_retriever.py

# Run any setup steps or pre-processing tasks here
echo "Starting AllAboutErik FastAPI service..."

# Start the main application
uvicorn main:app --host 0.0.0.0 --port 8000
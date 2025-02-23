# Makefile for AI Agents Lab
# Usage:
#   make setup-env  - Create and activate virtual environment
#   make run       - Run the application
#   make clean-env - Clean up the virtual environment

.PHONY: run setup-env clean-env

# the app should be run from the root directory 
# NOTE: all agents are defined in src/agents/
# NOTE: You can switch between agents by adding the agent name
run:
	python src/main.py

# Install dependencies
setup-env:
	uv sync


# spin up a local server for text to speech model
# run the tts server with GPU
run-tts-gpu:
	docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:v0.2.2

# run the tts server with CPU
run-tts-cpu:
	docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:v0.2.2

# to stop the tts server
stop-tts:
	docker stop $(docker ps -q --filter ancestor=ghcr.io/remsky/kokoro-fastapi-gpu:v0.2.2)
	docker stop $(docker ps -q --filter ancestor=ghcr.io/remsky/kokoro-fastapi-cpu:v0.2.2)
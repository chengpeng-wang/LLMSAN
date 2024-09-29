#!/bin/bash

# Set the path of the log directory relative to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../log"

source_bashrc() {
  if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
  fi
}

# source_bashrc

python3 batchrun.py \
  --bug-type=apt \
  --detection-model=gpt-3.5-turbo \
  --sanitization-model=gpt-3.5-turbo \
  --analysis-mode=eager \
  --project-mode=single \
  --engine=baseline \
  --global-temperature=0.0 \
  -step-by-step-check \
  --self-consistency-k=3

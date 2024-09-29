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
  --bug-type=npd \
  --detection-model=gpt-3.5-turbo \
  --sanitization-model=gpt-3.5-turbo \
  --analysis-mode=lazy \
  --project-mode=single \
  --engine=llmsan \
  -functionality-sanitize \
  -reachability-sanitize \
  --global-temperature=0.0 \
  --self-consistency-k=1
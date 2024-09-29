#!/bin/bash

python3 batchreport.py \
  --bug-type=apt \
  --detection-model=gpt-3.5-turbo \
  --sanitization-model=gpt-3.5-turbo \
  --project-mode=single \
  --engine=baseline \
  -step-by-step-check \
  --global-temperature=0.0 \
  --self-consistency-k=1
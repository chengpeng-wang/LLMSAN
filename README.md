# LLMSAN

LLMSAN is a tool for analyzing Java projects using large language models (LLMs) for bug detection and sanitization. This repository includes scripts for running batch analyses, generating reports, and transforming Java projects for analysis.

## Structure of the project

TODO: Please help me list the directory structure in this project

## Use LLMSAN

1. **Clone the repository**:
   ```sh
   git clone https://github.com/chengpeng-wang/LLMSAN.git
   cd LLMSAN
   ```

2. Install the dependencies

   ```sh
   pip install -r requirements.txt
   cd lib && python3 build.py
   ```

3. Detect NPD bug in demo file with LLMSAN

   ```
   sh run_llmsan.sh
   ```

4. Detect NPD bug in demo file with baseline

   ```
   sh run_baseline.sh
   ```

5. Check report

    ```
    sh report.sh
    ```

## More Configurations

This script runs the LLMSAN analysis. Below are the key configurations:

- `--bug-type`: Specify the bug type (e.g., npd for Null Pointer Dereference).
- `--detection-model`: Specify the LLM model for initial detection (e.g., gpt-3.5-turbo).
- `--sanitization-model`: Specify the LLM model for sanitization (e.g., gpt-3.5-turbo).
- `--analysis-mode`: Specify the analysis mode (lazy or eager).
- `--project-mode`: Specify the project mode (single or all).
- `--engine`: Specify the analyzer (llmsan or baseline).
- `-functionality-sanitize`: Enable functionality sanitization.
- `-reachability-sanitize`: Enable reachability sanitization.
- `--global-temperature`: Specify the temperature for the model.
- `--self-consistency-k`: Specify the number of self-consistency iterations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
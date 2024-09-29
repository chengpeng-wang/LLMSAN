# LLMSAN: Sanitizing Large Language Models in Bug Detection with Data-Flow

LLMSAN is a tool for prompting-based bug detection. Equipped with the sanitization technique, LLMSAN can recognize false positives in the reported bugs without introducing huge additional token costs.

## Structure of the project

```
├── README.md                              # README 
├── benchmark                              # Dataset
│   ├── Java                               # Java programs
│   │   ├── juliet-test-suite-APT          # Absolute Path Traversal
│   │   ├── juliet-test-suite-CI           # OS Command Injection
│   │   ├── juliet-test-suite-DBZ          # Divide-by-Zero
│   │   ├── juliet-test-suite-NPD          # Null Pointer Dereference
│   │   └── juliet-test-suite-XSS          # Cross-Site Scripting
│   └── case                               # Evaluation cases
├── lib                                    # Library
│   └── build.py                           # Build tree-sitter locally
├── log                                    # Output of LLMSAN and baselines
│   ├── baseline                           # Output of baselines
│   ├── llmsan                             # Output of LLMSAN
│   ├── batchreport.py                     # Summarize analysis reports
├── requirements.txt                       # requirement file
└── src                                    # Source code directory
 ├── batchrun.py                        # Entry of analysis
 ├── data                               # Data transform directory
 │   └── transform.py                   # Prepare data by obfuscation
 ├── model                              # LLM model related
 │   ├── detector.py                    # End-to-end CoT prompting-based detection
 │   ├── llm.py                         # LLM module
 │   └── utils.py                       # Basic setting of LLMs
 ├── parser                             # Parsing related
 │   └── parser.py                      # Parse LLM output
 ├── pipeline.py                        # Pipelines of LLMSAN and baselines
 ├── prompt                             # Prompt templates of different bug types
 └── sanitizer                          # Sanitizer related
 ├── analyzer.py                    # Program parsing-based analysis
 └── passes.py                      # Implementation of four sanitizers
```

## Installation

1. Clone the repository:
 ```sh
    git clone https://github.com/chengpeng-wang/LLMSAN.git
    cd LLMSAN
 ```

2. Install the required dependencies:
 ```sh
    pip install -r requirements.txt
 ```

3. Ensure you have the Tree-sitter library and language bindings installed:
 ```sh
    cd lib
    python build.py
 ```

4. Configure the keys:
 ```sh
    export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx >> ~/.bashrc
 ```

 Similarly, the other two keys can be set as follows:
 ```sh
    export REPLICATE_API_TOKEN=xxxxxx >> ~/.bashrc
    export GEMINI_KEY=xxxxxx >> ~/.bashrc
 ```

## Quick Start

1. **Analyze a demo case using LLMSAN**
 We can run the following commands to detect the XSS bug in the file `CWE80_XSS__CWE182_Servlet_database_66.java` as a demo.

 ```bash
   source ~/.bashrc

   python3 batchrun.py \
      --bug-type=xss \
     --detection-model=gpt-3.5-turbo \
      --sanitization-model=gpt-3.5-turbo \
     --analysis-mode=lazy \
      --project-mode=single \
     --engine=llmsan \
      -functionality-sanitize \
     -reachability-sanitize \
      --global-temperature=0.0 \
     --self-consistency-k=1
 ```

 If you want to detect all the XSS bugs, change `--project-mode=single` to `--project-mode=all`.

 If you want to detect kinds of bugs, change `xss` in `--bug-type=xss` to other bug types, which can be `apt`, `ci`, `npd`, and `dbz`.

 Then, you can summarize the analysis reports by running the command. Remember that you should make the values of the common options of batchrun and batchreport the same.

 ```sh
   cd log
   python3 batchreport.py \
      --bug-type=xss \
     --detection-model=gpt-3.5-turbo \
      --sanitization-model=gpt-3.5-turbo \
     --project-mode=single \
      --engine=llmsan \
     --global-temperature=0.0 \
      --self-consistency-k=1
 ```

 The summary of the analysis will be dumped to `report.json` in the directory `log`. In each item, the following dictionary shows the details of the detection and sanitization: 

 ```json
    "result": {
        "type_sanitize": 1,
        "functionality_sanitize": 1,
        "order_sanitize": 1,
        "reachability_sanitize": 1,
        "total": 1,
        "final": 1
    }
 ```

 The values of "xxx_sanitize" indicate whether the data-flow path violate the syntactic or semantic properties. If the value is 1, the property is not violated. If the value of "final" is 1, the bug report is recognized as true bug as all the sanitizers do not discover any violations.

  
2. **Analyze a demo case using Baselines**
   
 You can execute the following commands to run the baseline SC-CoT-Check upon the file `CWE80_XSS__CWE182_Servlet_database_66.java` as a demo, where `self-consistency-k` is set to 5 and the temperature is 0.5.

 ```bash
   source ~/.bashrc
   python3 batchrun.py \
    --bug-type=xss \
    --detection-model=gpt-3.5-turbo \
    --sanitization-model=gpt-3.5-turbo \
    --analysis-mode=lazy \
    --project-mode=single \
    --engine=baseline \
    --global-temperature=0.5 \
    -step-by-step-check \
    --self-consistency-k=5
 ```

 You can remove `-step-by-step-check` to disable CoT strategy and set `self-consistency-k` to 1 to disable self-consistency.

 Similarly, if you want to get the summarized report of a baseline, just run 

 ```sh
   cd log
   python3 batchreport.py \
      --bug-type=xss \
     --detection-model=gpt-3.5-turbo \
      --sanitization-model=gpt-3.5-turbo \
     --project-mode=single \
      --engine=baseline \
     -step-by-step-check \
      --global-temperature=0.5 \
     --self-consistency-k=5
 ```

 In the generated file `log/report.json`, if the boolean value attached to each data-flow path is true, the data-flow path is recognized as the true bug.

3. **Remark**

 To avoid the leakage of ground truth to LLMs, we obfuscate the code in the Juliet Test Suite. The details of the obfuscation can be found in the function `obfuscate` in the file `src/data/transform.py`. Also, we concatenate multiple Java files belonging to the same test case into a single file for convenience in prompting, even though the resulting file may not be compilable.


## Options in LLMSAN

You can configure the analysis by specifying the proper options. Here are the descriptions of the options in LLMSAN

- `--bug-type`: Specify the bug type, including `apt`, `ci`, `dbz`, `npd`, and `xss`.
- `--detection-model`: Specify the LLM model for initial detection (e.g., `gpt-3.5-turbo`).
- `--sanitization-model`: Specify the LLM model for sanitization (e.g., `gpt-3.5-turbo`). Please note that the detection model and sanitization model are not necessarily the same, although we set them to be the same in our work.
- `--analysis-mode`: Specify the analysis mode (lazy or eager). In the lazy mode, the initial bug detection would be skipped if the case has been analyzed before. In the eager mode, the detection phase is always enabled.
- `--project-mode`: Specify the project mode (single or all). In the single-analysis mode, run LLMSAN and baselines on single files as a demo. In the all-analysis mode, all the experimental subjects are analyzed.
- `--engine`: Specify the analyzer (llmsan or baseline).
- `-functionality-sanitize`: Enable functionality sanitization.
- `-reachability-sanitize`: Enable reachability sanitization.
- `-step-by-step-check`: Enable CoT
- `--global-temperature`: Specify the temperature for the model. The temperature of LLMSAN is always set to 0.0. 
- `--self-consistency-k`: Specify the number of self-consistency iterations. The self-consistency-k value of LLMSAN is always set to 1

### More Programming Languages

LLMSAN is language-agnostic. To migrate the current implementations to other programming languages or extract more syntactic facts, please refer to the grammar files in the corresponding Tree-sitter libraries and refactor the code in `sanitizer/analyzer.py`. Basically, you only need to change the node types when invoking `find_nodes_by_type`.

Here are the links to grammar files in Tree-sitter libraries targeting mainstream programming languages:

- C: https://github.com/tree-sitter/tree-sitter-c/blob/master/src/grammar.json
- C++: https://github.com/tree-sitter/tree-sitter-cpp/blob/master/src/grammar.json
- Java: https://github.com/tree-sitter/tree-sitter-java/blob/master/src/grammar.json
- Python: https://github.com/tree-sitter/tree-sitter-python/blob/master/src/grammar.json
- JavaScript: https://github.com/tree-sitter/tree-sitter-javascript/blob/master/src/grammar.json

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, please contact [wang6590@purdue.edu](mailto:wang6590@purdue.edu) or [stephenw.wangcp@gmail.com](mailto:stephenw.wangcp@gmail.com).
import concurrent.futures
import sys
import shutil
import json
import os
import re
from typing import List, Dict
from pathlib import Path
from model.llm import *
from datetime import datetime
import openai
from model.utils import *
from sanitizer.analyzer import *
from pipeline import *
import argparse
import tree_sitter
from data.transform import *


class BatchRun:
    def __init__(
        self,
        spec_file: str,
        project_name: str,
        test_cases: List[str],
        detection_model_name: str,
        detection_key: str,
        sanitization_model_name: str,
        sanitization_key: str,
        analysis_mode: str,
    ):
        """
        Initialize the BatchRun with the given parameters.
        :param spec_file: Specification file name
        :param project_name: Name of the project
        :param test_cases: List of test cases
        :param detection_model_name: Name of the detection model
        :param detection_key: API key for the detection model
        :param sanitization_model_name: Name of the sanitization model
        :param sanitization_key: API key for the validation model
        :param analysis_mode: Analysis mode (e.g., 'lazy' or 'eager')
        """
        self.spec_file = spec_file
        self.project_name = project_name
        self.test_cases = test_cases
        self.simplified_project_name = f"{self.project_name}_simplified"
        self.all_java_files = []
        self.all_single_files = []

        self.detection_model_name = detection_model_name
        self.detection_key = detection_key
        self.sanitization_model_name = sanitization_model_name
        self.sanitization_key = sanitization_key

        self.batch_run_statistics = {}
        self.code_in_support_files = {}
        cwd = Path(__file__).resolve().parent.parent.absolute()
        support_dir = str(cwd / "benchmark/Java" / self.simplified_project_name / "testcasesupport")
        for root, dirs, files in os.walk(support_dir):
            for file in files:
                with open(root + "/" + file, "r") as support_file:
                    code_in_support_file = support_file.read()
                    self.code_in_support_files[file] = obfuscate(code_in_support_file)
        self.analysis_mode = analysis_mode

    def batch_transform_projects(self) -> None:
        """
        Transform the projects by copying and simplifying the Java files.
        """
        cwd = Path(__file__).resolve().parent.parent.absolute()
        full_project_name = cwd / "benchmark/Java" / self.project_name
        new_full_project_name = cwd / "benchmark/Java" / self.simplified_project_name

        if os.path.exists(new_full_project_name):
            shutil.rmtree(new_full_project_name)
        shutil.copytree(full_project_name, new_full_project_name)

        cluster_list = []
        history = set()
        for root, dirs, files in os.walk(new_full_project_name):
            for file in files:
                if file.endswith(".java") and file.startswith("CWE"):
                    if not re.search(r"_\d+[a-z]$", file.replace(".java", "")):
                        continue
                    file_path = os.path.join(root, file)
                    match_str = file.replace(".java", "")[:-1]
                    if file_path in history:
                        continue
                    cluster = [file_path]
                    history.add(file_path)

                    for root2, dirs2, files2 in os.walk(new_full_project_name):
                        for file2 in files2:
                            if file2 in history or "_base.java" in file2:
                                continue
                            full_path2 = os.path.join(root2, file2)
                            if file2.startswith(match_str) and full_path2 not in history:
                                cluster.append(full_path2)
                                history.add(full_path2)
                    cluster_list.append(cluster)

        for file_cluster in cluster_list:
            is_class_split = all(re.search(r"_\d+[a-z]$", file_path.replace(".java", "")) for file_path in file_cluster)
            if is_class_split:
                transform_class_split_cluster_files(file_cluster)
            else:
                transform_function_split_cluster_files(file_cluster)

        for root, dirs, files in os.walk(new_full_project_name):
            for file in files:
                if file.endswith(".java") and file.startswith("CWE"):
                    if re.search(r"_\d+$", file.replace(".java", "")):
                        self.all_java_files.append(os.path.join(root, file))

        for full_java_file_path in self.all_java_files:
            if re.search(r"_\d+$", full_java_file_path.replace(".java", "")):
                self.all_single_files.append(full_java_file_path)

    def start_batch_run_llmsan(
        self,
        main_test_file: str,
        project_mode: str,
        neural_sanitize_strategy: Dict[str, bool],
        is_measure_token_cost: bool = False
    ) -> None:
        """
        Start the batch run for LLM-HAL-SPOT.
        :param main_test_file: Main test file to analyze
        :param project_mode: Project mode ('single', 'all')
        :param neural_check_strategy: Dictionary of neural sanitization strategies
        :param is_measure_token_cost: Flag to measure token cost
        """
        self.batch_transform_projects()
        total_false_cnt_dict = {
            "type_sanitize": 0,
            "functionality_sanitize": 0,
            "order_sanitize": 0,
            "reachability_sanitize": 0,
            "total": 0,
            "final": 0
        }

        total_cnt = 0
        inference_log_dir_path = str(Path(__file__).resolve().parent / "../../log/initial_detection/")
        if not os.path.exists(inference_log_dir_path):
            os.makedirs(inference_log_dir_path)

        inference_log_dir_path = str(Path(__file__).resolve().parent / "../../log/initial_detection" / self.detection_model_name)
        if not os.path.exists(inference_log_dir_path):
            os.makedirs(inference_log_dir_path)

        for java_file in self.all_single_files:
            if project_mode == "single" and main_test_file not in java_file:
                continue

            case_name = java_file[java_file.rfind("/") + 1:].replace(".java", "")
            if case_name not in self.test_cases:
                continue

            total_cnt += 1
            print("Analyze ID: ", total_cnt)

            false_cnt_dict = start_llmsan(
                java_file,
                self.code_in_support_files,
                self.detection_model_name,
                self.detection_key,
                self.sanitization_model_name,
                self.sanitization_key,
                self.spec_file,
                self.analysis_mode,
                neural_sanitize_strategy,
                is_measure_token_cost
            )
            total_false_cnt_dict = {key: total_false_cnt_dict[key] + false_cnt_dict[key] for key in false_cnt_dict}
        print(total_false_cnt_dict)
        return 


    def start_batch_baselines(
        self,
        main_test_file: str,
        project_mode: str,
        is_measure_token_cost: bool = False,
        step_by_step_check: bool = False,
        global_self_consistency_k: int = 1,
        temperature: float = 0.0
    ) -> None:
        """
        Start the batch run for baselines.
        :param main_test_file: Main test file to analyze
        :param project_mode: Project mode ('single', 'all')
        :param is_measure_token_cost: Flag to measure token cost
        :param step_by_step_check: Flag to enable step-by-step check
        :param global_self_consistency_k: Number of self-consistency iterations
        :param temperature: Temperature setting for the model
        """
        self.batch_transform_projects()

        total_cnt = 0
        for java_file in self.all_single_files:
            if project_mode == "single" and main_test_file not in java_file:
                continue

            case_name = java_file[java_file.rfind("/") + 1:].replace(".java", "")
            if case_name not in self.test_cases:
                continue

            total_cnt += 1
            print("Analyze ID: ", total_cnt)

            # Start the self-check run
            start_self_check_run(
                java_file,
                self.code_in_support_files,
                self.sanitization_model_name,
                self.sanitization_key,
                self.spec_file,
                is_measure_token_cost,
                step_by_step_check,
                global_self_consistency_k,
                temperature
            )


def run():
    """
    Run the release mode with specified parameters.
    """
    bug_types = ["juliet-test-suite-DBZ", "juliet-test-suite-NPD", "juliet-test-suite-XSS", "juliet-test-suite-CI", "juliet-test-suite-APT"]
    bug_names = ["Divide_by_Zero", "NULL_Pointer_Dereference", "XSS", "OS_Command_Injection", "Absolute_Path_Traversal"]
    specs = ["dbz.json", "npd.json", "xss.json", "ci.json", "apt.json"]
    models = ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o-mini", "gemini", "claude-3-haiku-20240307"]
    modes = ["lazy", "eager"]

    main_test_files = [
        "CWE369_Divide_by_Zero__int_Environment_modulo_73",
        "CWE476_NULL_Pointer_Dereference__StringBuilder_07",
        "CWE80_XSS__CWE182_Servlet_database_66",
        "CWE78_OS_Command_Injection__connect_tcp_06",
        "CWE36_Absolute_Path_Traversal__connect_tcp_14"
    ]

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--bug-type", choices=["xss", "dbz", "npd", "ci", "apt"], help="Specify the bug type")
    parser.add_argument("--detection-model", choices=models, help="Specify LLM model for initial detectioin")
    parser.add_argument("--sanitization-model", choices=models, help="Specify LLM model for sanitization")
    parser.add_argument("--analysis-mode", choices=modes, help="Specify analysis mode: lazy (load original reports of initial detection and sanitize only) or eager (re-detect)")
    parser.add_argument("--project-mode", choices=["single", "all"], help="Specify the project mode: a single file and all files (100 cases)")
    parser.add_argument("--engine", choices=["llmsan", "baseline"], help="Specify the analyzer: llmsan or baseline")

    parser.add_argument("-functionality-sanitize", action="store_true", help="Check the functionality")
    parser.add_argument("-reachability-sanitize", action="store_true", help="Check the reachability")
    
    parser.add_argument("-measure-token-cost", action="store_true", help="Measure token cost")
    parser.add_argument("--global-temperature", choices=["0.0", "0.5", "0.7", "1.0", "1.5", "1.7", "2.0"], help="Specify the temperature")
    parser.add_argument("-step-by-step-check", action="store_true", help="Enable the step-by-step check (CoT)")
    parser.add_argument("--self-consistency-k", choices=["1", "3", "5", "7", "9", "11", "13", "15", "17", "19"], help="Specify the number of self-consistency iterations")

    args = parser.parse_args()

    bug_type_id = -1
    if args.bug_type == "dbz":
        bug_type_id = 0
    elif args.bug_type == "npd":
        bug_type_id = 1
    elif args.bug_type == "xss":
        bug_type_id = 2
    elif args.bug_type == "ci":
        bug_type_id = 3
    elif args.bug_type == "apt":
        bug_type_id = 4

    case_path = str(Path(__file__).resolve().parent.parent / "benchmark/case/")
    case_json_files = [file for file in os.listdir(case_path)]

    test_cases = []
    for case_json_file in case_json_files:
        if bug_names[bug_type_id] in case_json_file:
            file_path = os.path.join(case_path, case_json_file)
            with open(file_path, 'r') as json_file:
                test_cases = json.load(json_file)["cases"]

    spec = specs[bug_type_id]
    detection_model = args.detection_model
    sanitization_model = args.sanitization_model
    analysis_mode = args.analysis_mode
    project_mode = args.project_mode

    project_name = bug_types[bug_type_id]
    is_measure_token_cost = args.measure_token_cost
    step_by_step_check = args.step_by_step_check

    global_temperature = float(args.global_temperature)
    global_self_consistency_k = int(args.self_consistency_k)

    neural_sanitize_strategy = {
        "functionality_sanitize": args.functionality_sanitize,
        "reachability_sanitize": args.reachability_sanitize
    }

    detection_key = standard_key
    sanitization_key = standard_key

    if args.engine == "llmsan":
        main_test_file = main_test_files[bug_type_id]
        batch_run = BatchRun(spec, project_name, test_cases, detection_model, detection_key, sanitization_model, sanitization_key, analysis_mode)
        batch_run.start_batch_run_llmsan(main_test_file, project_mode, neural_sanitize_strategy, is_measure_token_cost)
    elif args.engine == "baseline":
        main_test_file = main_test_files[bug_type_id]
        batch_run = BatchRun(spec, project_name, test_cases, detection_model, detection_key, sanitization_model, sanitization_key, analysis_mode)
        batch_run.start_batch_baselines(main_test_file, project_mode, is_measure_token_cost, step_by_step_check, global_self_consistency_k, global_temperature)


if __name__ == "__main__":
    run()

import json
import os
from typing import List, Dict
from pathlib import Path
import argparse


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
    parser.add_argument("--project-mode", choices=["single", "all"], help="Specify the project mode: a single file and all files (100 cases)")
    parser.add_argument("--engine", choices=["llmsan", "baseline"], help="Specify the analyzer: llmsan or baseline")
    
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

    detection_model = args.detection_model
    sanitization_model = args.sanitization_model
    project_mode = args.project_mode

    project_name = bug_types[bug_type_id]
    is_measure_token_cost = args.measure_token_cost
    step_by_step_check = args.step_by_step_check

    global_temperature = float(args.global_temperature)
    global_self_consistency_k = int(args.self_consistency_k)

    if args.engine == "llmsan":
        main_test_file = main_test_files[bug_type_id]
        collect_statistics_llmsan(project_name, test_cases, main_test_file, 
                                  detection_model, sanitization_model, project_mode)
    elif args.engine == "baseline":
        main_test_file = main_test_files[bug_type_id]
        collect_statistics_baseline(project_name, test_cases, main_test_file, 
                                    detection_model, sanitization_model, project_mode, 
                                    step_by_step_check, global_self_consistency_k, global_temperature)
        

def collect_statistics_llmsan(project_name, test_cases, main_test_file, 
                              detection_model, sanitization_model, project_mode):
    cwd = Path(__file__).resolve().parent
    json_dir = cwd / "llmsan" / "sanitization" / sanitization_model
    json_files = [file for file in os.listdir(json_dir)]
    final_report = {}
    if project_mode == "single":
        for file in json_files:
            if file == main_test_file + ".json":
                file_path = os.path.join(json_dir, file)
                with open(file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    final_report[file] = json_data["trace_check_results"]
    else:
        for file in json_files:
            if file.replace(".json", "") in test_cases:
                file_path = os.path.join(json_dir, file)
                with open(file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    final_report[file] = json_data["trace_check_results"]
    
    dump_json_file = os.path.join(cwd, "report.json")
    with open(dump_json_file, 'w') as json_file:
        json.dump(final_report, json_file, indent=4)
    return


def collect_statistics_baseline(project_name, test_cases, main_test_file, 
                                detection_model, sanitization_model, project_mode, 
                                step_by_step_check, global_self_consistency_k, global_temperature):
    cwd = Path(__file__).resolve().parent
    json_dir = cwd / "baseline" / "self_check" / sanitization_model
    json_files = [file for file in os.listdir(json_dir)]
    final_report = {}

    suffix = ("_step_by_step" if step_by_step_check else "") + "_" + str(global_self_consistency_k) + "_" + str(global_temperature) + ".json"

    if project_mode == "single":
        for file in json_files:
            if file == main_test_file + suffix:
                file_path = os.path.join(json_dir, file)
                with open(file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    final_report[file] = json_data["check_result"]
    else:
        for file in json_files:
            if suffix in file and file.replace(suffix, "") in test_cases:
                file_path = os.path.join(json_dir, file)
                with open(file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    final_report[file] = json_data["check_result"]
    
    dump_json_file = os.path.join(cwd, "report.json")
    with open(dump_json_file, 'w') as json_file:
        json.dump(final_report, json_file, indent=4)
    return


if __name__ == "__main__":
    run()

from data.transform import *
from sanitizer.analyzer import *
from sanitizer.passes import *
from parser.parser import *
from model.detector import *
import time
import openai
import tiktoken
import json
import signal
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def start_llmsan(
    java_file: str,
    code_in_support_files: Dict[str, str],
    detection_online_model_name: str,
    detection_key: str,
    sanitization_online_model_name: str,
    sanitization_key: str,
    spec_file_name: str,
    analysis_mode: str,
    neural_sanitize_strategy: Dict[str, bool],
    is_measure_token_cost: bool
) -> Dict[str, int]:
    """
    Start the LLMsan process.
    :param java_file: Path to the Java file to analyze
    :param code_in_support_files: Dictionary of support files with their content
    :param detection_online_model_name: Name of the online model for detection
    :param detection_key: API key for the detection model
    :param sanitization_online_model_name: Name of the online model for sanitization
    :param sanitization_key: API key for the sanitization model
    :param spec_file_name: Name of the specification file
    :param analysis_mode: Analysis mode for the detection model
    :param neural_check_strategy: Dictionary of neural check strategies
    :param is_measure_token_cost: Flag to measure token cost
    :return: Dictionary containing the count of each type of sanitization
    """
    cnt = 0
    case_name = java_file[java_file.rfind("/") + 1:].replace(".java", "")
    print("-----------------------------------------------------------")
    print("Analyzing ", case_name)
    print("-----------------------------------------------------------")

    is_detected = False
    log_dir_path = str(
        Path(__file__).resolve().parent.parent / ("log/llmsan/initial_detection/" + detection_online_model_name)
    )
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)
    existing_json_file_names = set([])

    for root, dirs, files in os.walk(log_dir_path):
        for file in files:
            if case_name in file:
                is_detected = True
                cnt += 1
                json_file_name = root + "/" + file
                existing_json_file_names.add(json_file_name)

    if detection_online_model_name == sanitization_online_model_name:
        sanitization_log_file_dir = str(
            Path(__file__).resolve().parent.parent / ("log/llmsan/sanitization/" + detection_online_model_name)
        )
    else:
        sanitization_log_file_dir = str(
            Path(__file__).resolve().parent.parent / (
                "log/llmsan/sanitization/" + detection_online_model_name + "_" + sanitization_online_model_name)
        )

    if not os.path.exists(sanitization_log_file_dir):
        os.makedirs(sanitization_log_file_dir)

    with open(java_file, "r") as file:
        source_code = file.read()
        new_code = obfuscate(source_code)
        lined_new_code = add_line_numbers(new_code)

    total_traces = []

    if not is_detected or analysis_mode == "eager":
        detector = Detector(detection_online_model_name, detection_key, spec_file_name)
        json_file_name = java_file[java_file.rfind("/") + 1:].replace(".java", "")

        iterative_cnt = 0
        while True:
            output = detector.start_detection(
                java_file,
                json_file_name,
                log_dir_path,
                source_code,
                lined_new_code,
                code_in_support_files,
                False,
                is_measure_token_cost
            )
            print("--------------------------")
            print("Detection output:")
            print("--------------------------")
            print(output)
            print("--------------------------")

            bug_num, traces, first_report = parse_bug_report(output)
            if len(traces) == bug_num:
                break
            iterative_cnt += 1
            if iterative_cnt > iterative_count_bound:
                bug_num = 0
                traces = []
                break
        total_traces = traces

        # Dump initial detection result
        existing_result = {
            "response": {
                "original code": source_code,
                "analyzed code": lined_new_code,
                "response": output,
                "intput token": 0,
                "output token": 0,
                "program line": 0
            }
        }
        output_json_file_name = (Path(log_dir_path).parent.parent / "initial_detection"
                                 / detection_online_model_name / (case_name + ".json"))
        
        if os.path.exists(output_json_file_name):
            os.remove(output_json_file_name)
        with open(output_json_file_name, "w") as file:
            json.dump(existing_result, file, indent=4)

    else:
        for json_file_name in existing_json_file_names:
            with open(json_file_name) as existing_json_file:
                existing_result = json.load(existing_json_file)
                output = existing_result["response"]["response"]
                bug_num, traces, report = parse_bug_report(output)

                if bug_num != len(traces):
                    bug_num = 0
                    traces = []

                total_traces.extend(traces)

    ts_analyzer = TSAnalyzer(java_file, source_code, new_code, code_in_support_files)
    passes = Passes(sanitization_online_model_name, sanitization_key, spec_file_name)

    trace_cnt = 0
    cnt_dict = {
        "type_sanitize": 0,
        "functionality_sanitize": 0,
        "order_sanitize": 0,
        "reachability_sanitize": 0,
        "total": 0,
        "final": 0
    }
    trace_check_results = []
    history_trace_strs = set([])

    for trace in total_traces:
        print("Analyzing trace: ", str(trace))
        cnt_dict_in_single_trace = {
            "type_sanitize": 0,
            "functionality_sanitize": 0,
            "order_sanitize": 0,
            "reachability_sanitize": 0,
            "total": 0,
            "final": 0
        }

        if str(trace) in history_trace_strs:
            continue
        history_trace_strs.add(str(trace))

        trace_cnt += 1
        cnt_dict["total"] += 1
        cnt_dict_in_single_trace["total"] += 1

        # data sanitization
        syntactic_check_result = passes.type_sanitize(ts_analyzer, trace)
        if syntactic_check_result:
            cnt_dict["type_sanitize"] += 1
            cnt_dict_in_single_trace["type_sanitize"] += 1

        functionality_sanitize_result, function_check_output_results = (
            passes.functionality_sanitize(ts_analyzer, trace, is_measure_token_cost)) \
            if neural_sanitize_strategy["functionality_sanitize"] else (True, {})
        if functionality_sanitize_result:
            cnt_dict["functionality_sanitize"] += 1
            cnt_dict_in_single_trace["functionality_sanitize"] += 1
        with open(sanitization_log_file_dir + "/" + case_name + "_" + str(trace_cnt)
                  + "_functionality_sanitize.json", "w") as file:
            json.dump(function_check_output_results, file, indent=4)

        # flow sanitization
        order_sanitize_result = passes.order_sanitize(ts_analyzer, trace)
        if order_sanitize_result:
            cnt_dict["order_sanitize"] += 1
            cnt_dict_in_single_trace["order_sanitize"] += 1

        reachability_sanitize_result, reachability_sanitize_output_results = (
            passes.reachability_sanitize(ts_analyzer, trace, is_measure_token_cost)) \
            if neural_sanitize_strategy["reachability_sanitize"] else (True, {})
        if reachability_sanitize_result:
            cnt_dict["reachability_sanitize"] += 1
            cnt_dict_in_single_trace["reachability_sanitize"] += 1
        with open(sanitization_log_file_dir + "/" + case_name + "_" + str(trace_cnt)
                  + "_reachability_sanitize.json", "w") as file:
            json.dump(reachability_sanitize_output_results, file, indent=4)

        if syntactic_check_result and functionality_sanitize_result and order_sanitize_result and reachability_sanitize_result:
            # report is a trug bug
            cnt_dict["final"] += 1
            cnt_dict_in_single_trace["final"] += 1
        print("Trace sanitization result: ", cnt_dict_in_single_trace)
        trace_check_results.append({
            "trace": trace,
            "result": cnt_dict_in_single_trace
        })

    output_results = {
        "original code": source_code,
        "analyzed code": lined_new_code,
        "trace_check_results": trace_check_results,
    }

    output_json_file_name = (Path(sanitization_log_file_dir) / (case_name + ".json"))
    with open(output_json_file_name, "w") as file:
        json.dump(output_results, file, indent=4)

    return cnt_dict


def start_self_check_run(
    java_file: str,
    code_in_support_files: Dict[str, str],
    online_model_name: str,
    key: str,
    spec_file_name: str,
    is_measure_token_cost: bool,
    step_by_step_check: bool,
    global_self_consistency_k: int,
    temperature: float
) -> None:
    """
    Start the self-check run process.
    :param java_file: Path to the Java file to analyze
    :param code_in_support_files: Dictionary of support files with their content
    :param online_model_name: Name of the online model for inference
    :param key: API key for the model
    :param spec_file_name: Name of the specification file
    :param is_measure_token_cost: Flag to measure token cost
    :param step_by_step_check: Flag to indicate step-by-step check (CoT or direct ask)
    :param global_self_consistency_k: Number of self-consistency iterations
    :param temperature: Temperature setting for the model
    """
    model = LLM(online_model_name, key, temperature)
    case_name = java_file[java_file.rfind("/") + 1:].replace(".java", "")
    print("-----------------------------------------------------------------------------")
    print("Analyzing ", case_name)
    print("-----------------------------------------------------------------------------")

    input_log_dir_path = str(
        Path(__file__).resolve().parent.parent / ("log/llmsan/initial_detection/" + online_model_name)
    )
    if not os.path.exists(input_log_dir_path):
        os.makedirs(input_log_dir_path)

    existing_json_file_names = set([])

    for root, dirs, files in os.walk(input_log_dir_path):
        for file in files:
            if case_name in file:
                json_file_name = root + "/" + file
                existing_json_file_names.add(json_file_name)

    with open(java_file, "r") as file:
        source_code = file.read()
        new_code = obfuscate(source_code)
        lined_new_code = add_line_numbers(new_code)

    for json_file_name in existing_json_file_names:
        check_result = []

        output_json_file_name = json_file_name.replace("initial_detection", "self_check").replace("llmsan", "baseline")
        strategy = "step_by_step" if step_by_step_check else "direct_ask"
        output_json_file_name = output_json_file_name.replace(".json", "") + "_" \
                                + strategy + "_" + str(global_self_consistency_k) + "_" + str(temperature) + ".json"
        
        if not os.path.exists(output_json_file_name[:output_json_file_name.rfind("/")]):
            os.makedirs(output_json_file_name[:output_json_file_name.rfind("/")])

        with open(json_file_name) as existing_json_file:
            existing_result = json.load(existing_json_file)
            output = existing_result["response"]["response"]

            bug_num, traces, first_report = parse_bug_report(output)
            trace_cnt = 0

            for trace in traces:
                trace_cnt += 1
                iterative_cnt = 0
                input_token_cost = 0
                output_token_cost = 0
                answers = []
                print("Analyzing trace: ", str(trace))

                for i in range(global_self_consistency_k):

                    while True:
                        with open(
                                Path(__file__).resolve().parent / "prompt" / spec_file_name,
                                "r",
                        ) as read_file:
                            spec = json.load(read_file)

                        message = spec["task"] + "\n"
                        message += "\n".join(spec["analysis_rules"]) + "\n"
                        message += "\n".join(spec["analysis_examples"]) + "\n"

                        program = ""
                        for support_file in code_in_support_files:
                            program += "The following is the file " + support_file + ":\n"
                            program += "```\n" + code_in_support_files[support_file] + "\n```\n\n"
                        program += (
                                "The following is the file " + json_file_name[json_file_name.rfind("/") + 1:] + ":\n"
                        )
                        program += "```\n" + lined_new_code + "\n```\n\n"

                        if step_by_step_check:
                            message += "\n".join(spec["meta_prompts_with_verification_step_by_step"]) + "\n"
                        else:
                            message += "\n".join(spec["meta_prompts_with_verification_direct_ask"]) + "\n"
                        message = message.replace("<PROGRAM>", program).replace(
                            "<BUG_TRACE>", str(trace)
                        )
                        message = message.replace("<RE_EMPHASIZE_RULE>", "\n".join(spec["re_emphasize_rules"]))

                        single_output, single_input_token_cost, single_output_token_cost = model.infer(message,
                                                                                                       is_measure_token_cost)
                        input_token_cost += single_input_token_cost
                        output_token_cost += single_output_token_cost

                        print(single_output)

                        if "yes" in single_output.split("\n")[-1].lower() or "no" in single_output.split("\n")[
                            -1].lower():
                            break
                        if iterative_cnt > iterative_count_bound:
                            break
                    if single_output == "":
                        is_false_positive = False
                    else:
                        is_false_positive = "no" in single_output.split("\n")[-1].lower() or "yes" not in \
                                        single_output.split("\n")[-1].lower()
                    answers.append(not is_false_positive)
                is_report = answers.count(True) > answers.count(False)
                check_result.append([trace, output, is_report, input_token_cost, output_token_cost])

            output_results = {
                "original code": existing_result["response"]["original code"],
                "analyzed code": existing_result["response"]["analyzed code"],
                "check_result": check_result,
            }

            with open(output_json_file_name, "w") as file:
                json.dump(output_results, file, indent=4)

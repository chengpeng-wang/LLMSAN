import json
import openai
import time
import signal
import os
import tiktoken
import sys
from pathlib import Path
from model.llm import LLM
from typing import Dict
from model.utils import *


class Detector:
    """
    Detector class for running models and analyzing code based on specifications.
    """

    def __init__(self, online_model_name: str, key: str, spec_file_name: str) -> None:
        """
        Initialize the Detector with model name, API key, and specification file name.
        :param online_model_name: Name of the online model to use
        :param key: API key for the model
        :param spec_file_name: Name of the specification file
        """
        self.online_model_name = online_model_name
        self.key = key
        self.model = LLM(self.online_model_name, self.key, 0)
        self.spec_file_name = spec_file_name

    def start_detection(
        self,
        file_name: str,
        json_file_name: str,
        log_file_path: str,
        original_code: str,
        analyzed_code: str,
        code_in_support_files: Dict[str, str],
        is_reflection: bool = False,
        is_measure_token_cost: bool = False,
        previous_report: str = "",
    ) -> str:
        """
        Start running the model with the provided parameters and analyze the code.
        :param file_name: Name of the file to analyze
        :param json_file_name: Name of the JSON file to save the results
        :param log_file_path: Path to save the log file
        :param original_code: Original code content
        :param analyzed_code: Analyzed code content
        :param code_in_support_files: Dictionary of support files with their content
        :param is_reflection: Flag to indicate if reflection is used
        :param is_measure_token_cost: Flag to measure token cost
        :param previous_report: Previous report content for reflection
        :return: Response from the model
        """
        # Load the specification file
        with open(
            Path(__file__).resolve().parent.parent / "prompt" / self.spec_file_name,
            "r",
        ) as read_file:
            spec = json.load(read_file)

        # Construct the message from the specification
        message = self._construct_message(spec, code_in_support_files, file_name, analyzed_code, is_reflection, previous_report)

        # Perform inference with the model
        response, input_token_cost, output_token_cost = self.model.infer(message, is_measure_token_cost)

        # Prepare the output results
        output_results = {
            "original code": original_code,
            "analyzed code": analyzed_code,
            "response": response,
            "all program size": len(message.split("\n")),
            "input_token_cost": input_token_cost,
            "output_token_cost": output_token_cost
        }

        # Save the results to a JSON file
        self._save_results(log_file_path, json_file_name, output_results)

        return response

    def _construct_message(
        self,
        spec: Dict,
        code_in_support_files: Dict[str, str],
        file_name: str,
        analyzed_code: str,
        is_reflection: bool,
        previous_report: str
    ) -> str:
        """
        Construct the message to be sent to the model based on the specification and code.
        :param spec: Specification dictionary
        :param code_in_support_files: Dictionary of support files with their content
        :param file_name: Name of the file to analyze
        :param analyzed_code: Analyzed code content
        :param is_reflection: Flag to indicate if reflection is used
        :param previous_report: Previous report content for reflection
        :return: Constructed message string
        """
        message = spec["task"] + "\n"
        message += "\n".join(spec["analysis_rules"]) + "\n"
        message += "\n".join(spec["output_constraints"]) + "\n"
        message += "\n".join(spec["analysis_examples"]) + "\n"

        program = ""
        for support_file in code_in_support_files:
            program += f"The following is the file {support_file}:\n"
            program += f"```\n{code_in_support_files[support_file]}\n```\n\n"
        program += f"The following is the file {file_name[file_name.rfind('/') + 1:]}:\n"
        program += f"```\n{analyzed_code}\n```\n\n"

        if not is_reflection:
            message += "\n".join(spec["meta_prompts_without_reflection"]) + "\n"
            message = message.replace("<PROGRAM>", program)
            message = message.replace("<RE_EMPHASIZE_RULE>", "\n".join(spec["re_emphasize_rules"]))
        else:
            message += "\n".join(spec["meta_prompts_with_reflection"]) + "\n"
            message = message.replace("<PROGRAM>", program).replace("<PREVIOUS_REPORT>", previous_report)
            message = message.replace("<RE_EMPHASIZE_RULE>", "\n".join(spec["re_emphasize_rules"]))

        return message

    def _save_results(self, log_file_path: str, json_file_name: str, output_results: Dict) -> None:
        """
        Save the output results to a JSON file.
        :param log_file_path: Path to save the log file
        :param json_file_name: Name of the JSON file to save the results
        :param output_results: Dictionary of output results
        """
        with open(f"{log_file_path}/{json_file_name}.json", "w") as file:
            json.dump({"response": output_results}, file, indent=4)
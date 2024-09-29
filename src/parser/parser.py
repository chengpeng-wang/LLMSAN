import re
from typing import Dict, List, Optional, Tuple

# bug report parser
def parse_bug_report(output: str) -> Tuple[Optional[int], List[List[Tuple[int, str]]], str]:
    """
    Parse the bug report from the given output string.
    :param output: The output string containing the bug report
    :return: A tuple containing the bug number, traces, and the full report as a string
    """
    begin_marker = "BEGIN REPORT"
    end_marker = "END REPORT"

    lines = output.split("\n")
    start_parsing = False
    report_lines = []

    for line in lines:
        line = line.strip()

        if begin_marker in line:
            start_parsing = True
            continue

        if end_marker in line:
            break

        if start_parsing:
            report_lines.append(line)

    bug_num = None
    explanations = []
    traces = []

    if report_lines:
        first_line_parts = report_lines[0].split()
        if len(first_line_parts) > 3 and first_line_parts[2].isdigit():
            bug_num = int(first_line_parts[2])

    for line in report_lines:
        if line.startswith("- "):
            if not ("[Explanation" in line and "]" in line and "[Trace" in line):
                continue
            bug_trace = line[line.find("[Trace:") + 7 : -1].strip()
            trace = []
            # Use regular expression to find and extract line numbers and data
            for item in bug_trace.replace("(Line ", "(")[1:-1].split("), ("):
                line_number_str = item[:item.find(", ")]
                var_name_str = item[item.find(", ") + 2:]
                if len(var_name_str) <= 2:
                    continue
                var_name_str = var_name_str[:-1]
                if "is_null" in var_name_str:
                    var_name_str = var_name_str.replace("is_null", "")
                elif "is_zero" in var_name_str:
                    var_name_str = var_name_str.replace("is_zero", "")
                elif "is_sensitive" in var_name_str:
                    var_name_str = var_name_str.replace("is_sensitive", "")
                else:
                    continue
                var_name_str = var_name_str[1:]
                if line_number_str.isdigit():
                    trace.append((int(line_number_str), var_name_str))
            traces.append(trace)
    return bug_num, traces, "\n".join(report_lines)


def parse_neural_sanitizer_output(output: str) -> bool:
    """
    Determine if the output contains a 'yes' or 'no' answer.
    :param output: The output string to analyze
    :return: Boolean indicating if the output contains 'yes' (True) or 'no' (False)
    """
    lines = output.strip().splitlines()
    lines.reverse()

    for line in lines:
        if "yes" in line.lower() or "no" in line.lower():
            return "no" not in line.lower()

    return False

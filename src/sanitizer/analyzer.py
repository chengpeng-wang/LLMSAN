import sys
import os
from os import path
import tree_sitter
from tree_sitter import Language
import tree_sitter_java as tsjava
from typing import List, Tuple, Dict
from enum import Enum
from data.transform import *
from pathlib import Path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

class Function:
    def __init__(self, function_id: int, function_name: str, function_code: str, start_line_number: int, end_line_number: int) -> None:
        """
        Record basic facts of the function
        """
        self.function_id: int = function_id
        self.function_name: str = function_name
        self.function_code: str = function_code
        self.start_line_number = start_line_number
        self.end_line_number = end_line_number

        self.parse_tree: tree_sitter.Tree = None
        self.is_transformed: bool = False
        self.is_parsed: bool = False

        # field initialization statements
        self.field_inits: Dict[int, str] = {}

        # call site nodes and line numbers (conform to control flow order)
        self.call_site_nodes: List[Tuple[tree_sitter.Node, int]] = []

        # if statement info
        self.if_statements: Dict[Tuple, Tuple] = {}

        # switch statement info
        self.switch_statements: Dict[Tuple, List] = {}

    def set_parse_tree(self, parse_tree: tree_sitter.Tree) -> None:
        """
        Set the parse tree for the function
        """
        self.parse_tree = parse_tree
        self.is_parsed = True

    def set_call_sites(self, call_sites: List[Tuple[tree_sitter.Node, int]]) -> None:
        """
        Set the call sites for the function
        """
        self.call_site_nodes = call_sites

    def set_field_inits_info(self, field_inits: Dict[int, str]) -> None:
        """
        Set the field initialization info for the function
        """
        self.field_inits = field_inits


class TSParser:
    """
    TSParser class for extracting information from Java files using tree-sitter.
    """

    def __init__(self, java_file_path: str) -> None:
        """
        Initialize TSParser with a java file path
        :param java_file_path: The path of a java file.
        """
        self.java_file_path: str = java_file_path
        self.methods: Dict[int, (str, str, int, int)] = {}
        self.classToFunctions: Dict[str, List[int]] = {}
        self.classToFields: Dict[str, List[int]] = {}
        self.fields: Dict[int, str] = {}
        self.fields_init: Dict[int, str] = {}

        self.fileToPackage: Dict[str, str] = {}
        self.fileToImports: Dict[str, set[str]] = {}
        self.fileToClasses: Dict[str, set[str]] = {}
        self.functionToFile: Dict[int, str] = {}
        self.packageToClasses: Dict[str, set[str]] = {}

        self.static_field_info: Dict[str, str] = {}

        cwd = Path(__file__).resolve().parent.absolute()
        TSPATH = cwd / "../../lib/build/"
        language_path = TSPATH / "my-languages.so"
        # Load the Java language
        self.java_lang: Language = Language(str(language_path), "java")

        # Initialize the parser
        self.parser: tree_sitter.Parser = tree_sitter.Parser()
        self.parser.set_language(self.java_lang)

    def parse_package_info(self, file_path: str, source_code: str, root_node: tree_sitter.Tree) -> str:
        """
        Extract package, Assume only have one package declaration
        :param file_path: The path of the Java file.
        :param source_code: The content of the source code
        :param root_node: The root node the parse tree
        :return package name
        """
        package_code = ""
        for node in root_node.children:
            if node.type == "package_declaration":
                for child_node in node.children:
                    if child_node.type in {"scoped_identifier", "identifier"}:
                        package_code = source_code[child_node.start_byte : child_node.end_byte]
                        if package_code != "":
                            break
                self.fileToPackage[file_path] = package_code
                break
        return package_code

    def parse_import_info(self, file_path: str, source_code: str, root_node: tree_sitter.Tree) -> None:
        """
        Extract imported packages or classes
        :param file_path: The path of the Java file.
        :param source_code: The content of the source code
        :param root_node: The root node the parse tree
        """
        for node in root_node.children:
            import_code = ""
            if node.type == "import_declaration":
                for child_node in node.children:
                    if child_node.type in {"scoped_identifier", "identifier"}:
                        import_code = source_code[child_node.start_byte : child_node.end_byte]
                    if import_code == "":
                        continue
                    if file_path not in self.fileToImports:
                        self.fileToImports[file_path] = set([])
                    self.fileToImports[file_path].add(import_code)

    def parse_class_declaration_info(self, file_path: str, source_code: str, package_name: str, root_node: tree_sitter.Tree) -> None:
        """
        Extract class declaration info: class name, fields, and methods
        :param file_path: The path of the Java file.
        :param source_code: The content of the source code
        :param package_name: The package name
        :param root_node: The root node the parse tree
        """
        for node in root_node.children:
            class_name = ""
            if node.type == "class_declaration":
                # Extract class name
                for child_node in node.children:
                    if child_node.type == "identifier":
                        class_name = source_code[child_node.start_byte : child_node.end_byte]
                        break
                if file_path not in self.fileToClasses:
                    self.fileToClasses[file_path] = set([])
                self.fileToClasses[file_path].add(class_name)
                if package_name not in self.packageToClasses:
                    self.packageToClasses[package_name] = set([])
                self.packageToClasses[package_name].add(class_name)

                # Extract method name and method content
                for child_node in node.children:
                    if child_node.type == "class_body":
                        for child_child_node in child_node.children:
                            # Extract methods
                            if child_child_node.type == "method_declaration":
                                method_name = ""
                                for child_child_child_node in child_child_node.children:
                                    if child_child_child_node.type == "identifier":
                                        method_name = source_code[child_child_child_node.start_byte : child_child_child_node.end_byte]
                                        break
                                method_code = source_code[child_child_node.start_byte : child_child_node.end_byte]
                                start_line_number = source_code[: child_child_node.start_byte].count("\n") + 1
                                end_line_number = source_code[: child_child_node.end_byte].count("\n") + 1
                                method_id = len(self.methods) + 1
                                self.methods[method_id] = (method_name, method_code, start_line_number, end_line_number)
                                if class_name not in self.classToFunctions:
                                    self.classToFunctions[class_name] = []
                                self.classToFunctions[class_name].append(method_id)
                                self.functionToFile[method_id] = file_path

                            # Extract fields
                            if child_child_node.type == "field_declaration":
                                for child_child_child_node in child_child_node.children:
                                    if child_child_child_node.type == "variable_declarator":
                                        for child_child_child_child_node in child_child_child_node.children:
                                            if child_child_child_child_node.type == "identifier":
                                                field_id = len(self.fields)
                                                self.fields[field_id] = source_code[child_child_child_child_node.start_byte : child_child_child_child_node.end_byte]
                                                self.fields_init[field_id] = source_code[child_child_child_node.start_byte : child_child_child_node.end_byte]
                                                if class_name not in self.classToFields:
                                                    self.classToFields[class_name] = []
                                                self.classToFields[class_name].append(field_id)

    def extract_single_file(self, file_path, source_code: str) -> None:
        """
        Extract information from a single Java file
        :param file_path: The path of the Java file
        :param source_code: The content of the source code
        """
        # Parse the Java code
        tree: tree_sitter.Tree = self.parser.parse(bytes(source_code, "utf8"))

        # Get the root node of the parse tree
        root_node: tree_sitter.Node = tree.root_node

        # Obtain package, import, and class info
        package_name = self.parse_package_info(file_path, source_code, root_node)
        self.parse_import_info(file_path, source_code, root_node)
        self.parse_class_declaration_info(file_path, source_code, package_name, root_node)

    def extract_static_field_from_support_files(self, support_files):
        """
        Extract static fields from support files
        :param support_files: A dictionary of support files with their content
        """
        def find_nodes(root_node: tree_sitter.Node, node_type: str) -> List[tree_sitter.Node]:
            nodes = []
            if root_node.type == node_type:
                nodes.append(root_node)

            for child_node in root_node.children:
                nodes.extend(find_nodes(child_node, node_type))
            return nodes

        for support_file in support_files:
            source_code = support_files[support_file]

            # Parse the Java code
            tree: tree_sitter.Tree = self.parser.parse(bytes(source_code, "utf8"))

            # Get the root node of the parse tree
            root_node: tree_sitter.Node = tree.root_node
            class_body_items = find_nodes(root_node, "class_declaration")

            for class_body_item in class_body_items:
                class_name = ""
                for child_node in class_body_item.children:
                    if child_node.type == "identifier":
                        class_name = source_code[child_node.start_byte : child_node.end_byte]
                    elif child_node.type == "class_body":
                        for child_child_node in child_node.children:
                            if child_child_node.type == "field_declaration":
                                if " static " in source_code[child_child_node.start_byte : child_child_node.end_byte]:
                                    for field_token in child_child_node.children:
                                        if field_token.type == "variable_declarator":
                                            info_str = source_code[field_token.start_byte : field_token.end_byte]
                                            field_name = info_str.split("=")[0].rstrip()
                                            assigned_value = info_str.split("=")[1].lstrip()
                                            self.static_field_info[class_name + "." + field_name] = class_name + "." + field_name + " = " + assigned_value


class TSAnalyzer:
    """
    TSAnalyzer class for retrieving necessary facts or functions for LMAgent
    """

    def __init__(
        self,
        java_file_path: str,
        original_code: str,
        analyzed_code: str,
        support_files: Dict[str, str],
    ) -> None:
        """
        Initialize TSAnalyzer with the project path.
        Currently, we only analyze a single Java file.
        :param java_file_path: The path of a Java file
        :param original_code: The original code of the Java file
        :param analyzed_code: The analyzed code of the Java file
        :param support_files: A dictionary of support files with their content
        """
        self.java_file_path: str = java_file_path
        self.ts_parser: TSParser = TSParser(java_file_path)
        self.original_code = original_code
        self.analyzed_code = analyzed_code
        self.support_files = support_files

        self.ts_parser.extract_single_file(self.java_file_path, self.analyzed_code)
        self.ts_parser.extract_static_field_from_support_files(self.support_files)

        self.environment = {}
        self.caller_callee_map = {}
        self.callee_caller_map = {}

        for function_id in self.ts_parser.methods:
            name, function_code, start_line_number, end_line_number = (
                self.ts_parser.methods[function_id]
            )
            current_function = Function(
                function_id, name, function_code, start_line_number, end_line_number
            )
            current_function.parse_tree = self.ts_parser.parser.parse(
                bytes(function_code, "utf8")
            )
            current_function = self.extract_call_meta_data_in_single_function(
                current_function
            )
            self.environment[function_id] = current_function

        self.main_ids: List[int] = self.find_all_top_functions()
        self.tmp_variable_count = 0


    # Functionality: Extracting Metadata
    def extract_call_meta_data_in_single_function(
        self, current_function: Function
    ) -> Function:
        """
        Extract call metadata in a single function.
        :param current_function: Function object
        :return: Function object with updated parse tree and call info
        """
        tree: tree_sitter.Tree = self.ts_parser.parser.parse(
            bytes(current_function.function_code, "utf8")
        )
        current_function.set_parse_tree(tree)
        root_node: tree_sitter.Node = tree.root_node

        # Identify call site info and maintain the environment
        all_call_sites = self.find_nodes_by_type(root_node, "method_invocation")
        white_call_sites = []

        for call_site_node in all_call_sites:
            callee_ids = self.find_callee(
                current_function.function_id,
                current_function.function_code,
                call_site_node,
            )
            if callee_ids:
                line_number = (
                    current_function.function_code[: call_site_node.start_byte].count("\n") + 1
                )

                # Update the call graph
                for callee_id in callee_ids:
                    caller_id = current_function.function_id
                    if caller_id not in self.caller_callee_map:
                        self.caller_callee_map[caller_id] = set()
                    self.caller_callee_map[caller_id].add(callee_id)
                    if callee_id not in self.callee_caller_map:
                        self.callee_caller_map[callee_id] = set()
                    self.callee_caller_map[callee_id].add(caller_id)

        current_function.set_call_sites(white_call_sites)

        # Compute the shared fields that can be accessed by the current function
        field_inits = self.find_field_initialization(current_function.function_id)
        current_function.set_field_inits_info(field_inits)

        # Compute the scope of the if-statements to guide the further path feasibility validation
        if_statements = self.find_if_statements(
            current_function.function_code,
            current_function.parse_tree.root_node,
        )
        current_function.if_statements = if_statements

        # Compute the scope of the switch statements to guide the further path feasibility validation
        switch_statements = self.find_switch_statements(
            current_function.function_code,
            current_function.parse_tree.root_node,
        )
        current_function.switch_statements = switch_statements

        # Compute the scope of the loop statements to guide the further path feasibility validation
        loop_statements = self.find_loop_statements(
            current_function.function_code,
            current_function.parse_tree.root_node,
        )
        current_function.loop_statements = loop_statements
        return current_function
    

    # Call Graph Analysis
    def find_callee(
        self, method_id: int, source_code: str, call_site_node: tree_sitter.Node
    ) -> List[int]:
        """
        Find callees that are invoked by a specific method.
        :param method_id: Caller function ID
        :param source_code: The content of the source file
        :param call_site_node: The node of the call site. The type is 'method_invocation'
        :return: The list of the IDs of called functions
        """
        assert call_site_node.type == "method_invocation"
        method_name = ""
        previous_str = ""
        current_str = ""
        for node2 in call_site_node.children:
            previous_str = current_str
            current_str = source_code[node2.start_byte : node2.end_byte]
            if node2.type == "argument_list":
                method_name = previous_str
                break

        # Grep callees with names
        callee_ids = []
        for class_name in self.ts_parser.classToFunctions:
            for method_id in self.ts_parser.classToFunctions[class_name]:
                if method_id not in self.ts_parser.methods:
                    continue
                name, code, start_line_number, end_line_number = self.ts_parser.methods[method_id]
                if name == method_name:
                    callee_ids.append(method_id)
        return callee_ids

    # Functionality: Finding Functions and Nodes
    def find_function_by_line_number(self, line_number: int) -> List[Function]:
        """
        Find all functions that contain the given line number.
        :param line_number: The line number to search for
        :return: A list of functions that contain the given line number
        """
        for function_id in self.environment:
            function = self.environment[function_id]
            if function.start_line_number <= line_number <= function.end_line_number:
                return [function]
        return []

    def find_node_by_line_number(
        self, line_number: int
    ) -> List[Tuple[str, tree_sitter.Node]]:
        """
        Find all nodes that correspond to the given line number.
        :param line_number: The line number to search for
        :return: A list of tuples containing the function code and the node
        """
        code_node_list = []
        for function_id in self.environment:
            function = self.environment[function_id]
            if not function.start_line_number <= line_number <= function.end_line_number:
                continue
            all_nodes = TSAnalyzer.find_all_nodes(function.parse_tree.root_node)
            for node in all_nodes:
                start_line = (
                    function.function_code[: node.start_byte].count("\n")
                    + function.start_line_number
                )
                end_line = (
                    function.function_code[: node.end_byte].count("\n")
                    + function.start_line_number
                )
                if start_line == end_line == line_number:
                    code_node_list.append((function.function_code, node))
        return code_node_list

    # Functionality: Finding Classes and Fields
    def find_class_by_function(self, function_id: int) -> str:
        """
        Find the class name that contains the given function.
        :param function_id: The ID of the function
        :return: The class name containing the function
        """
        for class_name in self.ts_parser.classToFunctions:
            if function_id in self.ts_parser.classToFunctions[class_name]:
                return class_name
        return ""

    def find_available_fields(self, function_id: int) -> Dict[int, str]:
        """
        Find all available fields for the given function.
        :param function_id: The ID of the function
        :return: A dictionary of field IDs to field names
        """
        class_name = self.find_class_by_function(function_id)
        if class_name not in self.ts_parser.classToFields:
            return {}
        return {field_id: self.ts_parser.fields[field_id] for field_id in self.ts_parser.classToFields[class_name]}

    def find_field_initialization(self, function_id: int) -> Dict[int, str]:
        """
        Find the initialization information for fields in the given function.
        :param function_id: The ID of the function
        :return: A dictionary of field IDs to their initialization code
        """
        class_name = self.find_class_by_function(function_id)
        if class_name not in self.ts_parser.classToFields:
            return {}
        return {field_id: self.ts_parser.fields_init[field_id] for field_id in self.ts_parser.classToFields[class_name]}

    # Functionality: Finding Statements
    def find_if_statements(self, source_code, root_node) -> Dict[Tuple, Tuple]:
        """
        Find all if statements in the given source code and root node.
        :param source_code: The source code of the function
        :param root_node: The root node of the parse tree
        :return: A dictionary of if statement information
        """
        targets = self.find_nodes_by_type(root_node, "if_statement")
        if_statements = {}

        for target in targets:
            condition_str = ""
            condition_line = 0
            true_branch_start_line = 0
            true_branch_end_line = 0
            else_branch_start_line = 0
            else_branch_end_line = 0
            block_num = 0
            for sub_target in target.children:
                if sub_target.type == "parenthesized_expression":
                    condition_line = source_code[: sub_target.start_byte].count("\n") + 1
                    condition_str = source_code[sub_target.start_byte : sub_target.end_byte]
                if sub_target.type == "block":
                    if block_num == 0:
                        true_branch_start_line = source_code[: sub_target.start_byte].count("\n") + 1
                        true_branch_end_line = source_code[: sub_target.end_byte].count("\n") + 1
                        block_num += 1
                    elif block_num == 1:
                        else_branch_start_line = source_code[: sub_target.start_byte].count("\n") + 1
                        else_branch_end_line = source_code[: sub_target.end_byte].count("\n") + 1
                        block_num += 1
            if_statement_end_line = max(true_branch_end_line, else_branch_end_line)
            if_statements[(condition_line, if_statement_end_line)] = (
                condition_line,
                condition_str,
                (true_branch_start_line, true_branch_end_line),
                (else_branch_start_line, else_branch_end_line),
            )
        return if_statements

    def find_switch_statements(self, source_code, root_node) -> Dict[Tuple, Tuple]:
        """
        Find all switch statements in the given source code and root node.
        :param source_code: The source code of the function
        :param root_node: The root node of the parse tree
        :return: A dictionary of switch statement information
        """
        targets = self.find_nodes_by_type(root_node, "switch_expression")
        switch_statements = {}
        for target in targets:
            parenthesized_node = self.find_nodes_by_type(target, "parenthesized_expression")[0]
            condition_line = source_code[: parenthesized_node.start_byte].count("\n") + 1
            parenthesized_node_str = source_code[parenthesized_node.start_byte : parenthesized_node.end_byte]
            switch_statement_start_line = condition_line
            switch_statement_end_line = source_code[: target.end_byte].count("\n") + 1

            case_group = self.find_nodes_by_type(target, "switch_block_statement_group")
            items = []
            for case_item in case_group:
                case_start_line = source_code[: case_item.start_byte].count("\n") + 1
                case_end_line = source_code[: case_item.end_byte].count("\n") + 1

                switch_label_node = self.find_nodes_by_type(case_item, "switch_label")[0]
                switch_label = source_code[switch_label_node.start_byte : switch_label_node.end_byte]
                label_str = switch_label.replace("case ", "").strip() if "case " in switch_label else ""
                items.append((label_str, case_start_line, case_end_line))

            switch_statements[(switch_statement_start_line, switch_statement_end_line)] = (parenthesized_node_str, items)
        return switch_statements

    def find_loop_statements(self, source_code, root_node) -> Dict[Tuple, Tuple]:
        """
        Find all loop statements in the given source code and root node.
        :param source_code: The source code of the function
        :param root_node: The root node of the parse tree
        :return: A dictionary of loop statement information
        """
        loop_statements = {}
        for_statement_nodes = self.find_nodes_by_type(root_node, "for_statement")
        for_statement_nodes.extend(self.find_nodes_by_type(root_node, "enhanced_for_statement"))
        while_statement_nodes = self.find_nodes_by_type(root_node, "while_statement")

        for loop_node in for_statement_nodes:
            loop_start_line = source_code[: loop_node.start_byte].count("\n") + 1
            loop_end_line = source_code[: loop_node.end_byte].count("\n") + 1

            header_line_start = 0
            header_line_end = 0
            header_str = ""
            loop_body_start_line = 0
            loop_body_end_line = 0

            header_start_byte = 0
            header_end_byte = 0

            for loop_child_node in loop_node.children:
                if loop_child_node.type == "(":
                    header_line_start = source_code[: loop_child_node.start_byte].count("\n") + 1
                    header_start_byte = loop_child_node.end_byte
                if loop_child_node.type == ")":
                    header_line_end = source_code[: loop_child_node.end_byte].count("\n") + 1
                    header_end_byte = loop_child_node.start_byte
                    header_str = source_code[header_start_byte: header_end_byte]
                if loop_child_node.type == "block":
                    lower_lines = []
                    upper_lines = []
                    for loop_child_child_node in loop_child_node.children:
                        if loop_child_child_node.type not in {"{", "}"}:
                            lower_lines.append(source_code[: loop_child_child_node.start_byte].count("\n") + 1)
                            upper_lines.append(source_code[: loop_child_child_node.end_byte].count("\n") + 1)
                    loop_body_start_line = min(lower_lines)
                    loop_body_end_line = max(upper_lines)
                if loop_child_node.type == "expression_statement":
                    loop_body_start_line = source_code[: loop_child_node.start_byte].count("\n") + 1
                    loop_body_end_line = source_code[: loop_child_node.end_byte].count("\n") + 1
            loop_statements[(loop_start_line, loop_end_line)] = (
                header_line_start,
                header_line_end,
                header_str,
                loop_body_start_line,
                loop_body_end_line,
            )

        for loop_node in while_statement_nodes:
            loop_start_line = source_code[: loop_node.start_byte].count("\n") + 1
            loop_end_line = source_code[: loop_node.end_byte].count("\n") + 1

            header_line_start = 0
            header_line_end = 0
            header_line = 0
            header_str = ""
            loop_body_start_line = 0
            loop_body_end_line = 0

            for loop_child_node in loop_node.children:
                if loop_child_node.type == "parenthesized_expression":
                    header_line_start = source_code[: loop_child_node.start_byte].count("\n") + 1
                    header_line_end = source_code[: loop_child_node.end_byte].count("\n") + 1
                    assert header_line_start == header_line_end
                    header_line = header_line_start
                    header_str = source_code[loop_child_node.start_byte: loop_child_node.end_byte]
                if loop_child_node.type == "block":
                    lower_lines = []
                    upper_lines = []
                    for loop_child_child_node in loop_child_node.children:
                        if loop_child_child_node.type not in {"{", "}"}:
                            lower_lines.append(source_code[: loop_child_child_node.start_byte].count("\n") + 1)
                            upper_lines.append(source_code[: loop_child_child_node.end_byte].count("\n") + 1)
                    loop_body_start_line = min(lower_lines)
                    loop_body_end_line = max(upper_lines)
            loop_statements[(loop_start_line, loop_end_line)] = (
                header_line,
                header_str,
                loop_body_start_line,
                loop_body_end_line,
            )

    # Functionality: Utility Functions
    @staticmethod
    def find_all_nodes(root_node: tree_sitter.Node) -> List[tree_sitter.Node]:
        """
        Find all nodes in the given root node.
        :param root_node: The root node of the parse tree
        :return: A list of all nodes
        """
        if root_node is None:
            return []
        nodes = [root_node]
        for child_node in root_node.children:
            nodes.extend(TSAnalyzer.find_all_nodes(child_node))
        return nodes

    @staticmethod
    def find_nodes_by_type(
        root_node: tree_sitter.Node, node_type: str
    ) -> List[tree_sitter.Node]:
        """
        Find all nodes of a specific type in the given root node.
        :param root_node: The root node of the parse tree
        :param node_type: The type of nodes to find
        :return: A list of nodes of the specified type
        """
        nodes = []
        if root_node.type == node_type:
            nodes.append(root_node)
        for child_node in root_node.children:
            nodes.extend(TSAnalyzer.find_nodes_by_type(child_node, node_type))
        return nodes

    def find_all_top_functions(self) -> List[int]:
        """
        Collect all the main functions, which are ready for analysis.
        :return: A list of IDs indicating main functions
        """
        main_ids = []
        for method_id in self.ts_parser.methods:
            name, code, start_line_number, end_line_number = self.ts_parser.methods[method_id]
            if code.count("\n") < 2:
                continue
            if name == "main":
                main_ids.append(method_id)
        return main_ids

    def collect_syntactic_types(self, node_list: List[Tuple[str, tree_sitter.Node]]):
        """
        Collect all syntactic types from the given list of nodes.
        :param node_list: A list of tuples containing the function code and the node
        :return: A set of syntactic types
        """
        syntactic_types = set()
        for code, node in node_list:
            if "expression" in node.type or "declarator" in node.type:
                sub_nodes = self.find_all_nodes(node)
                for sub_node in sub_nodes:
                    if (
                        any(char.isalpha() for char in sub_node.type)
                        and "identifier" not in sub_node.type
                        and "declarator" not in sub_node.type
                    ):
                        syntactic_types.add(sub_node.type)
        return syntactic_types

    # debug use
    def dump_call_graph(self):
        """
        Dump the call graph for debugging.
        """
        for caller_id in self.caller_callee_map:
            caller_name = self.ts_parser.methods[caller_id][0]
            callee_ids = self.caller_callee_map[caller_id]
            callee_names = [self.ts_parser.methods[callee_id][0] for callee_id in callee_ids]
            print(f"{caller_name} calls {callee_names}")

from typing import *
import tree_sitter
from pathlib import Path
from tree_sitter import Language
import tree_sitter_java as tsjava


def transform_function_split_cluster_files(file_cluster: List[str]) -> None:
    file_lines_dic = {}
    main_file = None
    for file_path in file_cluster:
        is_main_class = False
        trim_file_path = file_path.replace(".java", "")
        if trim_file_path.endswith("a"):
            main_file = file_path
            is_main_class = True
        with open(file_path, "r") as file:
            lines = file.readlines()
        transformed_lines = []
        if is_main_class:
            for line in lines:
                if "action(" in line:
                    prev_line = transformed_lines.pop()
                    function_name = prev_line[
                        prev_line.rfind("new ") + 4 : prev_line.rfind("(")
                    ]
                    para = line[line.rfind("(") : line.rfind(")") + 1]
                    whitespace_count = len(line) - len(line.lstrip())
                    new_line = " " * whitespace_count + function_name + para + ";\n"
                    transformed_lines.append(new_line)
                else:
                    transformed_lines.append(line)
        else:
            class_name = ""
            for line in lines:
                if " class " in line:
                    class_name = line.lstrip(" ").split(" ")[2]
                    continue
                if not line.startswith("    "):
                    continue
                if line.startswith("    public"):
                    transformed_line = line.replace("action", class_name)
                else:
                    transformed_line = line
                transformed_lines.append(transformed_line)
        file_lines_dic[file_path] = transformed_lines

    new_file_path = main_file.replace(".java", "")[0:-1] + ".java"
    new_lines = file_lines_dic[main_file][:-1]
    for file_path in file_lines_dic:
        if file_path == main_file:
            continue
        new_lines.extend(file_lines_dic[file_path])
    new_lines.append("}")
    with open(new_file_path, "w") as file:
        for new_line in new_lines:
            file.write(new_line)
    return


def transform_class_split_cluster_files(file_cluster: List[str]) -> None:
    file_lines_dic = {}
    main_file = None
    for file_path in file_cluster:
        is_main_class = False
        trim_file_path = file_path.replace(".java", "")
        if trim_file_path.endswith("a"):
            main_file = file_path
            is_main_class = True
        with open(file_path, "r") as file:
            lines = file.readlines()
        transformed_lines = []
        if is_main_class:
            for line in lines:
                if "(new CWE" in line:
                    transformed_line = line.replace("(new ", "").replace("()).", "_")
                else:
                    transformed_line = line
                transformed_lines.append(transformed_line)
        else:
            for line in lines:
                if not line.startswith("    "):
                    continue
                if "(new CWE" in line:
                    transformed_line = line.replace("(new ", "").replace("()).", "_")
                elif line.startswith("    public "):
                    split_tokens = line.replace("    ", "").split(" ")
                    class_name = file_path[file_path.rfind("/") + 1 :].replace(
                        ".java", ""
                    )
                    split_tokens[2] = class_name + "_" + split_tokens[2]
                    transformed_line = "    "
                    transformed_line += " ".join(split_tokens)
                else:
                    transformed_line = line
                transformed_lines.append(transformed_line)
        file_lines_dic[file_path] = transformed_lines

    new_file_path = main_file.replace(".java", "")[0:-1] + ".java"
    new_lines = file_lines_dic[main_file][:-1]
    for file_path in file_lines_dic:
        if file_path == main_file:
            continue
        new_lines.extend(file_lines_dic[file_path])
    new_lines.append("}")
    with open(new_file_path, "w") as file:
        for new_line in new_lines:
            file.write(new_line)
    return


def obfuscate(source_code):
    def find_nodes(
        root_node: tree_sitter.Node, node_type: str
    ) -> List[tree_sitter.Node]:
        """
        Find all the nodes with node_type type underlying the root node.
        :param root_node: root node
        :return the list of the nodes with node_type type
        """
        nodes = []
        if root_node.type == node_type:
            nodes.append(root_node)

        for child_node in root_node.children:
            nodes.extend(find_nodes(child_node, node_type))
        return nodes

    cwd = Path(__file__).resolve().parent.parent.absolute()
    TSPATH = cwd / "../lib/build/"
    language_path = TSPATH / "my-languages.so"

    JAVA_LANGUAGE = Language(str(language_path), "java")
    parser = tree_sitter.Parser()
    parser.set_language(JAVA_LANGUAGE)

    t = parser.parse(bytes(source_code, "utf8"))
    root_node = t.root_node
    nodes = find_nodes(root_node, "line_comment")
    nodes.extend(find_nodes(root_node, "block_comment"))
    nodes.extend(find_nodes(root_node, "javadoc_comment"))

    new_code = source_code

    for node in nodes:
        comment = source_code[node.start_byte : node.end_byte]
        new_code = new_code.replace(comment, "\n" * comment.count("\n"))

    new_code = (
        new_code.replace("good", "foo")
        .replace("bad", "hoo")
        .replace("G2B", "xx")
        .replace("B2G", "yy")
    )
    return new_code


def add_line_numbers(source_code):
    line_number = 0
    new_lines = []
    for line in source_code.split("\n"):
        line_number += 1
        new_line = str(line_number) + "  " + line
        new_lines.append(new_line)
    return "\n".join(new_lines)

import sys
import os
import gzip
from lxml import etree
from typing import List, Tuple, Dict, Any


def open_xml_file(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rb")
    return open(path, "rb")


def build_tree_structure(xml_path) -> List[Dict[str, Any]]:
    try:
        with open_xml_file(xml_path) as f:
            content = f.read()
            tree = etree.fromstring(content)
            return [_build_node_structure(tree, content)]
    except Exception as e:
        raise RuntimeError(f"Failed to parse {xml_path}: {e}")


def _build_node_structure(element, content: bytes) -> Dict[str, Any]:
    # Get the start and end positions of this element in the content
    start_line = element.sourceline
    end_line = start_line + content[element.sourceline :].count(b"\n")

    # Get the element's opening tag
    start_tag = f"<{element.tag}".encode()
    start_pos = content.find(start_tag, element.sourceline)
    if start_pos != -1:
        end_pos = content.find(b">", start_pos)
        if end_pos != -1:
            opening_tag = content[start_pos : end_pos + 1].decode()
        else:
            opening_tag = f"<{element.tag}>"
    else:
        opening_tag = f"<{element.tag}>"

    node = {
        "tag": element.tag,
        "children": [],
        "start_line": start_line,
        "end_line": end_line,
        "opening_tag": opening_tag,
    }

    for child in element:
        node["children"].append(_build_node_structure(child, content))
    return node


def compare_structures(
    struct1: List[Dict[str, Any]], struct2: List[Dict[str, Any]], path: str = ""
) -> List[str]:
    diffs = []
    current_group = []

    # Compare root elements
    if len(struct1) != len(struct2):
        current_group.append(f"Different number of root elements at {path}")
        diffs.append("\n".join(current_group))
        return diffs

    for i, (node1, node2) in enumerate(zip(struct1, struct2)):
        current_path = f"{path} > {node1['tag']}" if path else node1["tag"]

        # Compare tags
        if node1["tag"] != node2["tag"]:
            current_group.append(
                f"Different tags at {current_path}: {node1['tag']} vs {node2['tag']}\n"
                f"  File 1 (line {node1['start_line']}): {node1['opening_tag']}\n"
                f"  File 2 (line {node2['start_line']}): {node2['opening_tag']}"
            )
            continue

        # Compare children
        if len(node1["children"]) != len(node2["children"]):
            current_group.append(
                f"Different number of children at {current_path}\n"
                f"  File 1 (line {node1['start_line']}): {node1['opening_tag']}\n"
                f"  File 2 (line {node2['start_line']}): {node2['opening_tag']}"
            )

        # Compare child tags
        child_tags1 = {child["tag"] for child in node1["children"]}
        child_tags2 = {child["tag"] for child in node2["children"]}

        if child_tags1 != child_tags2:
            missing_in_1 = child_tags2 - child_tags1
            missing_in_2 = child_tags1 - child_tags2
            if missing_in_1:
                current_group.append(
                    f"Missing elements in File 1 at {current_path}: {', '.join(missing_in_1)}\n"
                    f"  File 1 (line {node1['start_line']}): {node1['opening_tag']}\n"
                    f"  File 2 (line {node2['start_line']}): {node2['opening_tag']}"
                )
            if missing_in_2:
                current_group.append(
                    f"Missing elements in File 2 at {current_path}: {', '.join(missing_in_2)}\n"
                    f"  File 1 (line {node1['start_line']}): {node1['opening_tag']}\n"
                    f"  File 2 (line {node2['start_line']}): {node2['opening_tag']}"
                )

        # Recursively compare children
        child_diffs = compare_structures(
            node1["children"], node2["children"], current_path
        )
        if child_diffs:
            if current_group:
                diffs.append("\n".join(current_group))
                current_group = []
            diffs.extend(child_diffs)

    if current_group:
        diffs.append("\n".join(current_group))

    return diffs


def format_diff(diffs: List[str]) -> str:
    if not diffs:
        return "No structural differences found."

    # Group related changes together
    grouped_diffs = []
    current_group = []

    for diff in diffs:
        if diff.startswith("- "):
            if current_group:
                grouped_diffs.append("\n".join(current_group))
                current_group = []
            current_group.append(diff)
        else:
            current_group.append(diff)

    if current_group:
        grouped_diffs.append("\n".join(current_group))

    return "Structural differences:\n" + "\n".join(grouped_diffs)


def main():
    if len(sys.argv) != 3:
        print("Usage: python xmlstructdiff.py file1.xml file2.xml")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    if not os.path.exists(file1):
        print(f"Error: {file1} not found.")
        sys.exit(1)
    if not os.path.exists(file2):
        print(f"Error: {file2} not found.")
        sys.exit(1)

    try:
        struct1 = build_tree_structure(file1)
        struct2 = build_tree_structure(file2)
        diffs = compare_structures(struct1, struct2)
        print(format_diff(diffs))
    except RuntimeError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

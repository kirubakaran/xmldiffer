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
            tree = etree.parse(f)
            root = tree.getroot()
            return [_build_node_structure(root)]
    except Exception as e:
        raise RuntimeError(f"Failed to parse {xml_path}: {e}")


def _build_node_structure(element) -> Dict[str, Any]:
    node = {"tag": element.tag, "children": []}
    for child in element:
        node["children"].append(_build_node_structure(child))
    return node


def compare_structures(
    struct1: List[Dict[str, Any]], struct2: List[Dict[str, Any]], path: str = ""
) -> List[str]:
    diffs = []

    # Compare root elements
    if len(struct1) != len(struct2):
        diffs.append(f"Different number of root elements at {path}")
        return diffs

    for i, (node1, node2) in enumerate(zip(struct1, struct2)):
        current_path = f"{path}/{node1['tag']}" if path else node1["tag"]

        # Compare tags
        if node1["tag"] != node2["tag"]:
            diffs.append(
                f"Different tags at {current_path}: {node1['tag']} vs {node2['tag']}"
            )
            continue

        # Compare children
        if len(node1["children"]) != len(node2["children"]):
            diffs.append(f"Different number of children at {current_path}")
            continue

        # Recursively compare children
        child_diffs = compare_structures(
            node1["children"], node2["children"], current_path
        )
        diffs.extend(child_diffs)

    return diffs


def format_diff(diffs: List[str]) -> str:
    if not diffs:
        return "No structural differences found."

    return "Structural differences:\n" + "\n".join(f"- {diff}" for diff in diffs)


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

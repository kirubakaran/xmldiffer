import sys
import os
import gzip
import difflib
from lxml import etree

def open_xml_file(path):
    if path.endswith(".gz"):
        return gzip.open(path, 'rb')
    return open(path, 'rb')

def extract_structure(xml_path):
    try:
        with open_xml_file(xml_path) as f:
            events = ('start', 'end')
            depth = 0
            structure = []
            for event, elem in etree.iterparse(f, events=events):
                if event == 'start':
                    structure.append(f"{'  ' * depth}<{elem.tag}>")
                    depth += 1
                elif event == 'end':
                    depth -= 1
                    elem.clear()
            return structure
    except Exception as e:
        raise RuntimeError(f"Failed to parse {xml_path}: {e}")

def diff_structures(path1, path2):
    struct1 = extract_structure(path1)
    struct2 = extract_structure(path2)
    return difflib.unified_diff(struct1, struct2, fromfile=path1, tofile=path2)

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
        diff = diff_structures(file1, file2)
        for line in diff:
            print(line)
    except RuntimeError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()

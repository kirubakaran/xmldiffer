import sys
from lxml import etree


def flatten_xml(element, path=""):
    current_path = path + element.tag if not path else path + " > " + element.tag
    # Get the line number from the element's source info
    line_num = element.sourceline
    print(f"{current_path}\t{line_num}")

    for child in element:
        flatten_xml(child, current_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python flatten.py <xml_file>")
        sys.exit(1)

    xml_file = sys.argv[1]

    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        flatten_xml(root)
    except FileNotFoundError:
        print(f"Error: File '{xml_file}' not found")
        sys.exit(1)
    except etree.ParseError:
        print(f"Error: Invalid XML file '{xml_file}'")
        sys.exit(1)


if __name__ == "__main__":
    main()

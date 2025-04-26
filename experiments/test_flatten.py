import unittest
import io
import sys
from contextlib import redirect_stdout
from xml.etree import ElementTree as ET
from flatten import flatten_xml


class TestXMLFlattener(unittest.TestCase):
    def assert_flattened_output(self, xml_string, expected_output):
        # Parse XML string directly instead of file
        root = ET.fromstring(xml_string)

        # Capture stdout to test the output
        f = io.StringIO()
        with redirect_stdout(f):
            flatten_xml(root)

        # Get output and split into lines, removing empty lines
        output = f.getvalue().strip()
        actual_lines = [line.strip() for line in output.split("\n") if line.strip()]
        expected_lines = [
            line.strip() for line in expected_output.split("\n") if line.strip()
        ]

        self.assertEqual(actual_lines, expected_lines)

    def test_simple_xml(self):
        xml = """
        <root>
            <item>
                <name>x</name>
            </item>
        </root>
        """
        expected = """
        root
        root > item
        root > item > name
        """
        self.assert_flattened_output(xml, expected)

    def test_complex_xml(self):
        xml = """
        <library>
            <book>
                <title>The Great Gatsby</title>
                <author>F. Scott Fitzgerald</author>
                <details>
                    <year>1925</year>
                    <publisher>Charles Scribner's Sons</publisher>
                </details>
            </book>
        </library>
        """
        expected = """
        library
        library > book
        library > book > title
        library > book > author
        library > book > details
        library > book > details > year
        library > book > details > publisher
        """
        self.assert_flattened_output(xml, expected)

    def test_xml_with_attributes(self):
        xml = """
        <contacts>
            <person id="1">
                <name type="full">John Doe</name>
                <email></email>
                <phone type="mobile" country="US">+1-555-0123</phone>
            </person>
        </contacts>
        """
        expected = """
        contacts
        contacts > person
        contacts > person > name
        contacts > person > email
        contacts > person > phone
        """
        self.assert_flattened_output(xml, expected)

    def test_empty_xml(self):
        xml = "<root></root>"
        expected = "root"
        self.assert_flattened_output(xml, expected)

    def test_single_element_xml(self):
        xml = "<root/>"
        expected = "root"
        self.assert_flattened_output(xml, expected)


if __name__ == "__main__":
    unittest.main()

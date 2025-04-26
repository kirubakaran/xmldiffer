import unittest
import io
import sys
import os
import tempfile
from contextlib import redirect_stdout
from lxml import etree
from flatten import flatten_xml


class TestXMLFlattener(unittest.TestCase):
    def assert_flattened_output(self, xml_string, expected_output):
        # Create a temporary file and write the XML to it
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as tmp:
            tmp.write(xml_string.strip())
            tmp_path = tmp.name

        try:
            # Parse XML from the temporary file
            tree = etree.parse(tmp_path)
            root = tree.getroot()

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
        finally:
            # Clean up the temporary file
            os.unlink(tmp_path)

    def test_simple_xml(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item>
        <name>x</name>
    </item>
</root>"""
        expected = """
        root\t2
        root > item\t3
        root > item > name\t4
        """
        self.assert_flattened_output(xml, expected)

    def test_complex_xml(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<library>
    <book>
        <title>The Great Gatsby</title>
        <author>F. Scott Fitzgerald</author>
        <details>
            <year>1925</year>
            <publisher>Charles Scribner's Sons</publisher>
        </details>
    </book>
</library>"""
        expected = """
        library\t2
        library > book\t3
        library > book > title\t4
        library > book > author\t5
        library > book > details\t6
        library > book > details > year\t7
        library > book > details > publisher\t8
        """
        self.assert_flattened_output(xml, expected)

    def test_xml_with_attributes(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<contacts>
    <person id="1">
        <name type="full">John Doe</name>
        <email></email>
        <phone type="mobile" country="US">+1-555-0123</phone>
    </person>
</contacts>"""
        expected = """
        contacts\t2
        contacts > person\t3
        contacts > person > name\t4
        contacts > person > email\t5
        contacts > person > phone\t6
        """
        self.assert_flattened_output(xml, expected)

    def test_empty_xml(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<root></root>"""
        expected = "root\t2"
        self.assert_flattened_output(xml, expected)

    def test_single_element_xml(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<root/>"""
        expected = "root\t2"
        self.assert_flattened_output(xml, expected)


if __name__ == "__main__":
    unittest.main()

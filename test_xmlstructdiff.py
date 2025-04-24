import unittest
import os
import tempfile
import gzip
from xmlstructdiff import (
    open_xml_file,
    build_tree_structure,
    compare_structures,
    format_diff,
)


class TestXMLStructDiff(unittest.TestCase):
    def setUp(self):
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()

        # Create a simple XML file
        self.simple_xml = os.path.join(self.temp_dir, "simple.xml")
        with open(self.simple_xml, "wb") as f:
            f.write(b"<root>\n  <child>text</child>\n</root>")

        # Create a gzipped XML file
        self.gzipped_xml = os.path.join(self.temp_dir, "gzipped.xml.gz")
        with gzip.open(self.gzipped_xml, "wb") as f:
            f.write(b"<root>\n  <child>text</child>\n</root>")

        # Create a malformed XML file
        self.malformed_xml = os.path.join(self.temp_dir, "malformed.xml")
        with open(self.malformed_xml, "wb") as f:
            f.write(b"<root>\n  <child>text</child>")  # Missing closing root tag

        # Create two XML files with different structures
        self.xml1 = os.path.join(self.temp_dir, "file1.xml")
        with open(self.xml1, "wb") as f:
            f.write(
                b"""<root>
  <person>
    <name>John</name>
    <age>30</age>
    <sex>male</sex>
  </person>
</root>"""
            )

        self.xml2 = os.path.join(self.temp_dir, "file2.xml")
        with open(self.xml2, "wb") as f:
            f.write(
                b"""<root>
  <person>
    <name>John</name>
    <age>30</age>
    <detail>
      <sex>male</sex>
    </detail>
  </person>
</root>"""
            )

    def tearDown(self):
        # Clean up temporary files
        for file in [
            self.simple_xml,
            self.gzipped_xml,
            self.malformed_xml,
            self.xml1,
            self.xml2,
        ]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)

    def test_open_xml_file(self):
        # Test opening regular XML file
        with open_xml_file(self.simple_xml) as f:
            content = f.read()
            self.assertEqual(content, b"<root>\n  <child>text</child>\n</root>")

        # Test opening gzipped XML file
        with open_xml_file(self.gzipped_xml) as f:
            content = f.read()
            self.assertEqual(content, b"<root>\n  <child>text</child>\n</root>")

    def test_build_tree_structure(self):
        # Test building structure from simple XML
        structure = build_tree_structure(self.simple_xml)
        self.assertEqual(len(structure), 1)
        self.assertEqual(structure[0]["tag"], "root")
        self.assertEqual(len(structure[0]["children"]), 1)
        self.assertEqual(structure[0]["children"][0]["tag"], "child")
        self.assertEqual(structure[0]["start_line"], 1)
        self.assertEqual(structure[0]["end_line"], 3)

        # Test handling malformed XML
        with self.assertRaises(RuntimeError):
            build_tree_structure(self.malformed_xml)

    def test_compare_structures(self):
        # Test comparing different structures
        struct1 = build_tree_structure(self.xml1)
        struct2 = build_tree_structure(self.xml2)
        diffs = compare_structures(struct1, struct2)

        # Should find the difference in the person element's children
        self.assertTrue(
            any(
                "Missing elements in File 1 at root > person: detail" in diff
                for diff in diffs
            )
        )
        self.assertTrue(
            any(
                "Missing elements in File 2 at root > person: sex" in diff
                for diff in diffs
            )
        )

        # Should include line numbers and content
        self.assertTrue(any("File 1 (line 2): <person>" in diff for diff in diffs))
        self.assertTrue(any("File 2 (line 2): <person>" in diff for diff in diffs))

        # Test comparing identical structures
        struct1 = build_tree_structure(self.simple_xml)
        struct2 = build_tree_structure(self.simple_xml)
        diffs = compare_structures(struct1, struct2)
        self.assertEqual(len(diffs), 0)

    def test_format_diff(self):
        # Test formatting with no differences
        self.assertEqual(format_diff([]), "No structural differences found.")

        # Test formatting with differences
        diffs = ["Difference 1", "Difference 2"]
        formatted = format_diff(diffs)
        self.assertTrue("Difference 1" in formatted)
        self.assertTrue("Difference 2" in formatted)
        self.assertTrue(formatted.startswith("Structural differences:"))


if __name__ == "__main__":
    unittest.main()

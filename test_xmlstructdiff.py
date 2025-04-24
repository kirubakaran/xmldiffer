import unittest
import os
import tempfile
import gzip
from xmlstructdiff import open_xml_file, extract_structure, diff_structures


class TestXMLStructDiff(unittest.TestCase):
    def setUp(self):
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()

        # Create a simple XML file
        self.simple_xml = os.path.join(self.temp_dir, "simple.xml")
        with open(self.simple_xml, "wb") as f:
            f.write(b"<root><child>text</child></root>")

        # Create a gzipped XML file
        self.gzipped_xml = os.path.join(self.temp_dir, "gzipped.xml.gz")
        with gzip.open(self.gzipped_xml, "wb") as f:
            f.write(b"<root><child>text</child></root>")

        # Create a malformed XML file
        self.malformed_xml = os.path.join(self.temp_dir, "malformed.xml")
        with open(self.malformed_xml, "wb") as f:
            f.write(b"<root><child>text</child>")  # Missing closing root tag

        # Create two XML files with different structures
        self.xml1 = os.path.join(self.temp_dir, "file1.xml")
        with open(self.xml1, "wb") as f:
            f.write(b"<root><child1>text1</child1></root>")

        self.xml2 = os.path.join(self.temp_dir, "file2.xml")
        with open(self.xml2, "wb") as f:
            f.write(b"<root><child2>text2</child2></root>")

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
            self.assertEqual(content, b"<root><child>text</child></root>")

        # Test opening gzipped XML file
        with open_xml_file(self.gzipped_xml) as f:
            content = f.read()
            self.assertEqual(content, b"<root><child>text</child></root>")

    def test_extract_structure(self):
        # Test extracting structure from simple XML
        structure = extract_structure(self.simple_xml)
        expected = ["<root>", "  <child>"]
        self.assertEqual(structure, expected)

        # Test extracting structure from gzipped XML
        structure = extract_structure(self.gzipped_xml)
        self.assertEqual(structure, expected)

        # Test handling malformed XML
        with self.assertRaises(RuntimeError):
            extract_structure(self.malformed_xml)

    def test_diff_structures(self):
        # Test diffing two different structures
        diff = list(diff_structures(self.xml1, self.xml2))
        self.assertTrue(len(diff) > 0)
        self.assertTrue(any("child1" in line for line in diff))
        self.assertTrue(any("child2" in line for line in diff))

        # Test diffing identical structures
        diff = list(diff_structures(self.simple_xml, self.simple_xml))
        self.assertEqual(len(diff), 0)


if __name__ == "__main__":
    unittest.main()

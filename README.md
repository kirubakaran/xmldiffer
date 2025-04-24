# XML Structure Diff

This tool compares the **structure only** of two XML files — ignoring text, attributes, and comments — and outputs a unified diff of the tag hierarchy.

## Usage

### Command line

```bash
python xmlstructdiff.py file1.xml file2.xml
```

Also supports `.gz` compressed files.

### With Docker

```bash
docker build -t xmlstructdiff .
docker run --rm -v "$PWD":/data xmlstructdiff /data/file1.xml /data/file2.xml
```

## Example

```bash
<root>
  <item>
    <name>foo</name>
  </item>
</root>
```

vs.

```bash
<root>
  <item>
    <title>bar</title>
  </item>
</root>
```

Will output:

```diff
@@ -2,7 +2,7 @@
   <item>
-    <name>
+    <title>
```

## Notes

- Handles large files by streaming via `lxml.iterparse`
- Ignores attribute values, text, tail text, and comments
- Output format is `diff -u` style


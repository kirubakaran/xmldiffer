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

## Examples

### Simple Example

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

### Real-world Example

Compare two course catalog XML files:

```bash
# Using Python directly
python xmlstructdiff.py examples/file-1a.xml examples/file-1b.xml

# Using Docker
docker build -t xmlstructdiff .

docker run --rm -v "$PWD":/data xmlstructdiff /data/examples/file-1a.xml /data/examples/file-1b.xml
```

The output will show structural differences between the course catalogs, such as:

```diff
@@ -1,5 +1,5 @@
 <root>
   <course>
-    <time>
+    <schedule>
       <start_time>
       <end_time>
```

Also try comparing `file-1a.xml` against `file-1c.xml`

## Notes
- Ignores attribute values, text, tail text, and comments

## Wishlist
- Handling really large files needs streaming via `lxml.iterparse` but this proved difficult to implement with the current requirements of needing to print line numbers as well as parent-child tree.



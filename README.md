# XML Structure Diff

This tool compares the **structure only** of two XML files — ignoring text, attributes, and comments — and outputs a unified diff of the tag hierarchy.

![xmldiff-users](https://github.com/user-attachments/assets/18e4cb21-4a89-44de-80d7-0a11bb9208ad)

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

```xml
<root>
  <item>
    <name>foo</name>
  </item>
</root>
```

vs.

```xml
<root>
  <item>
    <title>bar</title>
  </item>
</root>
```

Will output:

```
Structural differences:
Missing elements in File 1 at root > item: title
  File 1 (line 4): <item>
  File 2 (line 4): <item>
Missing elements in File 2 at root > item: name
  File 1 (line 4): <item>
  File 2 (line 4): <item>
Different tags at root > item > name: name vs title
  File 1 (line 5): <name>
  File 2 (line 5): <title>
```

### Real-World Example

Compare two course catalog XML files:

```bash
# Using Python directly
python xmlstructdiff.py examples/file-1a.xml examples/file-1c.xml

# Using Docker
docker run --rm -v "$PWD":/data xmlstructdiff /data/examples/file-1a.xml /data/examples/file-1c.xml
```

The output will show structural differences between the course catalogs, such as:

```
Structural differences:
Missing elements in File 1 at root > course: now
  File 1 (line 118): <course>
  File 2 (line 118): <course>
Missing elements in File 2 at root > course: time
  File 1 (line 118): <course>
  File 2 (line 118): <course>
Different tags at root > course > time: time vs now
  File 1 (line 127): <time>
  File 2 (line 127): <now>

Missing elements in File 1 at root > course: titles
  File 1 (line 232): <course>
  File 2 (line 234): <course>
Missing elements in File 2 at root > course: title
  File 1 (line 232): <course>
  File 2 (line 234): <course>
Different tags at root > course > title: title vs titles
  File 1 (line 237): <title>
  File 2 (line 239): <titles>
```

## Notes
- Ignores attribute values, text, tail text, and comments

## Wishlist
- Handling really large files needs streaming via `lxml.iterparse` but this proved difficult to implement with the current requirements of needing to print line numbers as well as parent-child tree.



<?php
/**
 * Test file for Markdown Converter
 * This file tests the markdown to HTML conversion functionality
 */

require_once 'markdown_converter.php';

// Test markdown content
$test_markdown = "# Main Title

## Chapter 1: Introduction

This is a **bold** paragraph with some *italic* text and `code` inline.

### Subsection

Here's a list of important points:

- First point
- Second point with **emphasis**
- Third point

And a numbered list:

1. First item
2. Second item
3. Third item

> This is a blockquote with important information.

Here's some code:

```python
def hello_world():
    print('Hello, World!')
```

And some more text with **bold** and *italic* formatting.

---

## Chapter 2: Conclusion

This chapter concludes with:

- Summary points
- Final thoughts
- Call to action

> **Important**: Remember to apply what you've learned!";

echo "<h1>Markdown Converter Test</h1>\n";
echo "<h2>Original Markdown:</h2>\n";
echo "<pre>" . htmlspecialchars($test_markdown) . "</pre>\n";
echo "<hr>\n";
echo "<h2>Converted HTML:</h2>\n";
echo "<div style='border: 1px solid #ccc; padding: 20px; background: #f9f9f9;'>\n";
echo MarkdownConverter::convertSafe($test_markdown);
echo "</div>\n";
echo "<hr>\n";
echo "<h2>Raw HTML Output:</h2>\n";
echo "<pre>" . htmlspecialchars(MarkdownConverter::convertSafe($test_markdown)) . "</pre>\n";
?> 
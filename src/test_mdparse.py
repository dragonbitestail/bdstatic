import unittest
from textnode import *
from mdparse import *

class TestTextParse(unittest.TestCase):

    def test_splitter(self):
        nodes = [TextNode("This is text with a `code block` word and a **bold** word", TextType.TEXT),
                 TextNode("`Code at start of node` followed by text at end", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code block")
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_extract_md_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        tuple_matches = extract_markdown_images(text)
        self.assertEqual(tuple_matches[0][0], "rick roll")
        self.assertEqual(tuple_matches[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")


        text_no_image_link = "This is text with ending punctuation! It should not produce a link!"
        matches = extract_markdown_images(text_no_image_link)
        self.assertEqual(matches, [])

    def test_extract_md_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        tuple_matches = extract_markdown_links(text)
        self.assertListEqual(tuple_matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link text](https://example.com/page1.html) and another [second link](https://example.com/page2.html)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com/page1.html"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://example.com/page2.html"
                ),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                new_nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
# Heading 1

```
print("Hello World")
```

This is a paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

> Block quote
> more text in the block quote

- This is a list
- with items

1. item one
2. item two
3. item three
"""
        assert_block_types = [BlockType.HEADING, BlockType.CODE,
                              BlockType.PARAGRAPH, BlockType.QUOTE,
                              BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]
        blocks = markdown_to_blocks(md)

        for idx, block in enumerate(blocks):
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                assert_block_types[idx],
            )


if __name__ == "__main__":
    unittest.main()

import unittest
from textnode import *
from mdparse import *

class TestTextParse(unittest.TestCase):

    def test_splitter(self):
        nodes = [TextNode("This is text with a `code block` word and a **bold** word", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code block")
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)


if __name__ == "__main__":
    unittest.main()

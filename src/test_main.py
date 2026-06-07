
import unittest
from textnode import *
from mdparse import *
from main import extract_title

class TestMain(unittest.TestCase):

    def test_extract_title(self):
        md = """
# Hello

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
                "# Hello",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        title = extract_title("# Hello")

        self.assertEqual(title, "Hello")

        # Test raised exception and value of raised exception 
        #self.assertRaises(Exception, lambda: extract_title("no title here"))
        self.assertRaises(Exception, extract_title, "no title here")

        with self.assertRaises(Exception) as assert_ex:
            extract_title("no title here")

            ex = assert_ex.exception

            self.assertEqual(ex.value, "title block not found", "Expected exception message \"title block not found\" not raised.")


if __name__ == "__main__":
    unittest.main()

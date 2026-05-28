import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):

    def test_props_none(self):
        node = HTMLNode("a", "Cheese world")
        self.assertEqual(node.props, None)

    def test_props_output(self):
        node = HTMLNode("a", "Cheese world", props={"href": "https://www.example.com/", "alt": "link to example website"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.example.com/\" alt=\"link to example website\"")

    def test_props_none_output(self):
        node = HTMLNode("a", "Cheese world")
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_style(self):
        node = LeafNode("p", "Hello, world!", props={"class": "red"})
        self.assertEqual(node.to_html(), "<p class=\"red\">Hello, world!</p>")

class TestParentNode(unittest.TestCase):

    def test_parent_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_parent_to_html_p_with_style(self):
        node = LeafNode("p", "Hello, world!", props={"class": "red"})
        self.assertEqual(node.to_html(), "<p class=\"red\">Hello, world!</p>")

class TestHTMLTree(unittest.TestCase):

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child2</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

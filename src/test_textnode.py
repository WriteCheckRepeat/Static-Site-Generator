import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD,"link")
        node2 = TextNode("This is a text node", TextType.BOLD,"link")
        self.assertEqual(node, node2)

    def test_eq_second_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD,None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)   

    def test_neq_no_url(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_with_url(self):
        node = TextNode("This is a text node", TextType.ITALIC,"link")
        node2 = TextNode("This is a text node", TextType.BOLD,"link")
        self.assertNotEqual(node, node2)

    def test_neq_second_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD,"link")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)   

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_incorrect_type(self):
        with self.assertRaises(AttributeError):
            node = TextNode("This is a bold text node", TextType.I)
            html_node = text_node_to_html_node(node)

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is a image text node", TextType.IMAGE, "https:imagelink")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https:imagelink")
        self.assertEqual(html_node.props["alt"], "This is a image text node")

    def test_link(self):
        node = TextNode("This is a image text node", TextType.LINK, "https:somelink")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a image text node")
        self.assertEqual(html_node.props["href"], "https:somelink")

if __name__ == "__main__":
    unittest.main()
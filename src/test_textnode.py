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

    def test_text_bold(self):
        with self.assertRaises(AttributeError):
            node = TextNode("This is a bold text node", TextType.I)
            html_node = text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()
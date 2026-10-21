import unittest
from markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class Testmarkdown(unittest.TestCase):
    def test_pass_through_BOLD(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        nodes2 = split_nodes_delimiter([node2],"**",TextType.BOLD)
        self.assertEqual(node, nodes2[0])

    def test_pass_through_LINK_and_ITALIC(self):
        node_link = TextNode("This is a text node", TextType.LINK,"link")
        node2_link = TextNode("This is a text node", TextType.LINK,"link")
        node_italic = TextNode("This is a text node", TextType.ITALIC)
        node2_italic = TextNode("This is a text node", TextType.ITALIC)
        nodes = split_nodes_delimiter([node2_link,node2_italic],"**",TextType.BOLD)
        self.assertEqual(node_link, nodes[0])
        self.assertEqual(node_italic, nodes[1])
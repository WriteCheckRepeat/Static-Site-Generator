import unittest
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_Text_middle_BOLD(self):
        node = TextNode("This is a text **node**, ok?", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertEqual(TextNode("This is a text ",TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("node",TextType.BOLD), nodes[1])
        self.assertEqual(TextNode(", ok?",TextType.TEXT), nodes[2])   

    def test_Text_end_BOLD(self):
        node = TextNode("This is a text **node**", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertEqual(TextNode("This is a text ",TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("node",TextType.BOLD), nodes[1])   

    def test_Text_middle_and_End_BOLD(self):
        node = TextNode("This is a text **node**, ok**?**", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertEqual(TextNode("This is a text ",TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("node",TextType.BOLD), nodes[1])
        self.assertEqual(TextNode(", ok",TextType.TEXT), nodes[2])   
        self.assertEqual(TextNode("?",TextType.BOLD), nodes[3])

    def test_Text_middle_BOLD_wrong_Delimiter_first(self):
        node = TextNode("This is a text *node**, ok?", TextType.TEXT)
        with self.assertRaises(Exception):
            nodes = split_nodes_delimiter([node],"**", TextType.BOLD)

    def test_Text_middle_BOLD_wrong_Delimiter_second(self):
        node = TextNode("This is a text **node*, ok?", TextType.TEXT)
        with self.assertRaises(Exception):
            nodes = split_nodes_delimiter([node],"**", TextType.BOLD)

    def test_Text_middle_BOLD_wrong_Delimiter_third(self):
        node = TextNode("This is a text **node**, ok*?**", TextType.TEXT)
        with self.assertRaises(Exception):
            nodes = split_nodes_delimiter([node],"**", TextType.BOLD)

    def test_Text_middle_BOLD_wrong_Delimiter_fourth(self):
        node = TextNode("This is a text **node**, ok**?*", TextType.TEXT)
        with self.assertRaises(Exception):
            nodes = split_nodes_delimiter([node],"**", TextType.BOLD)

    def test_Text_middle_BOLD_and_End_ITALIC(self):
        node = TextNode("This is a text **node**, ok_?_", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
        self.assertEqual(TextNode("This is a text ",TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("node",TextType.BOLD), nodes[1])
        self.assertEqual(TextNode(", ok",TextType.TEXT), nodes[2])   
        self.assertEqual(TextNode("?",TextType.ITALIC), nodes[3])

    def test_Text_start_BOLD_and_End_ITALIC(self):
        node = TextNode("**This is a text **node, ok_?_", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
        self.assertEqual(TextNode("This is a text ",TextType.BOLD), nodes[0])
        self.assertEqual(TextNode("node, ok",TextType.TEXT), nodes[1])
        self.assertEqual(TextNode("?",TextType.ITALIC), nodes[2])

    def test_Text_start_BOLD_and_two_End_ITALIC(self):
        node = TextNode("**This is a text **node, ok_?__!_", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
        self.assertEqual(TextNode("This is a text ",TextType.BOLD), nodes[0])
        self.assertEqual(TextNode("node, ok",TextType.TEXT), nodes[1])
        self.assertEqual(TextNode("?",TextType.ITALIC), nodes[2])
        self.assertEqual(TextNode("!",TextType.ITALIC), nodes[3])

    def test_Text_middle_BOLD_and_ITALIC_inbetween(self):
        node = TextNode("This is a text **node, _ok?_**", TextType.TEXT)
        nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes,"_", TextType.ITALIC)
        self.assertEqual(TextNode("This is a text ",TextType.TEXT), nodes[0])
        self.assertEqual(TextNode("node, _ok?_",TextType.BOLD), nodes[1]) 
#        self.assertEqual(TextNode("?",TextType.ITALIC), nodes[3])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [some Link](https://i.imgur.com)"
        )
        self.assertListEqual([("some Link", "https://i.imgur.com")], matches)

    def test_split_images_with_end_text(self):
#        self.maxDiff = None
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) we, can go on.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" we, can go on.", TextType.TEXT),
            ],
            new_nodes,
        )

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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" ", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_with_end_text(self):
#        self.maxDiff = None
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) we, can go on.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" we, can go on.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link(self):
#        self.maxDiff = None
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_function_on_links(self):
#        self.maxDiff = None
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_two_link(self):
#        self.maxDiff = None
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

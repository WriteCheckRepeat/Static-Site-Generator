import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_without_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_to_html_raises_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode()
            html = node.to_html()


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "some link text!", {"href": "https://www.some_link.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.some_link.com">some link text!</a>')

    def test_leaf_to_html_no_val(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None, {"href": "https://www.some_link.com"})
            node.to_html()

    def test_leaf_to_html_a_repr(self):
        node = LeafNode("a", "some link text!", {"href": "https://www.some_link.com"})
        self.assertEqual(repr(node), "LeafNode(a, some link text!, {'href': 'https://www.some_link.com'}")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("d", "grandchild_2")
        grandchild_node_3 = LeafNode("e", "grandchild_3")
        child_node_1 = ParentNode("span", [grandchild_node_1])
        child_node_2 = ParentNode("p", [grandchild_node_2, grandchild_node_3])
        parent_node = ParentNode("div", [child_node_1,child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild_1</b></span><p><d>grandchild_2</d><e>grandchild_3</e></p></div>",
        )

    def test_to_html_with_multiple_children_val_error_on_leaf(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("d", "grandchild_2")
        grandchild_node_3 = LeafNode("e", None)
        child_node_1 = ParentNode("span", [grandchild_node_1])
        child_node_2 = ParentNode("p", [grandchild_node_2, grandchild_node_3])
        parent_node = ParentNode("div", [child_node_1,child_node_2])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children_val_error_on_parent(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("d", "grandchild_2")
        grandchild_node_3 = LeafNode("e", "grandchild_3")
        child_node_1 = ParentNode("span", [grandchild_node_1])
        child_node_2 = ParentNode("p", [grandchild_node_2, grandchild_node_3])
        parent_node = ParentNode("div",None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children_val_error_on_child(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("d", "grandchild_2")
        grandchild_node_3 = LeafNode("e", "grandchild_3")
        child_node_1 = ParentNode("span", None)
        child_node_2 = ParentNode("p", [grandchild_node_2, grandchild_node_3])
        parent_node = ParentNode("div", [child_node_1,child_node_2])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children_missing_tag_on_child(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("d", "grandchild_2")
        grandchild_node_3 = LeafNode("e", "grandchild_3")
        child_node_1 = ParentNode("span", [grandchild_node_1])
        child_node_2 = ParentNode(None, [grandchild_node_2, grandchild_node_3])
        parent_node = ParentNode("div", [child_node_1,child_node_2])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children_some_deeper(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("d", "grandchild_2")
        grandgrandchild_node_1 = LeafNode("f", "grandgrandchild_1")
        grandchild_node_3 = ParentNode("e", [grandgrandchild_node_1])
        child_node_1 = ParentNode("span", [grandchild_node_1])
        child_node_2 = ParentNode("p", [grandchild_node_2, grandchild_node_3])
        parent_node = ParentNode("div", [child_node_1,child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild_1</b></span><p><d>grandchild_2</d><e><f>grandgrandchild_1</f></e></p></div>",
        )

    def test_to_html_with_multiple_children_empty_children_list(self):
        grandchild_node_1 = LeafNode("b", "grandchild_1")
        grandchild_node_2 = LeafNode("d", "grandchild_2")
        grandchild_node_3 = LeafNode("e", "grandchild_3")
        child_node_1 = ParentNode("span", [])
        child_node_2 = ParentNode("p", [grandchild_node_2, grandchild_node_3])
        parent_node = ParentNode("div", [child_node_1,child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span></span><p><d>grandchild_2</d><e>grandchild_3</e></p></div>",
        )
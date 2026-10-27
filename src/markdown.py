from collections.abc import Callable
from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    '''
    converts markdown to Text Node Format, that can be converted to HTML Nodes. Doesn't handle links or images.
    '''
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            tmp_strs = old_node.text.split(delimiter)
            if not len(tmp_strs)%2:
                raise Exception(f"Error: Missing a closing '{delimiter}' in '{old_node}'")
            inside_inline = False
            for i in range(len(tmp_strs)):
                if tmp_strs[i] is not "":
                    if inside_inline:
                        new_nodes.append(TextNode(tmp_strs[i],text_type))
                    else:
                        new_nodes.append(TextNode(tmp_strs[i],TextType.TEXT))
                if inside_inline:
                    inside_inline = False
                else:
                    inside_inline = True
    return new_nodes

def extract_markdown_images(text:str) -> list[tuple]:
    '''Placeholder description.
    '''
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text:str) -> list[tuple]:
    '''Placeholder description.
    '''
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    '''
    converts markdown to Text Node Format, that can be converted to HTML Nodes.
    '''
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            tmp_strs = []
            for i in range(len(images)):
            # split the entire markdown syntax for image link to remove it from the resulting Strings.
                tmp_strs += old_node.text.split(f"![{images[i][0]}]({images[i][1]})",maxsplit=1)
            i = 0
            j = 0
            while i < len(tmp_strs) and j < len(images):
                if tmp_strs[i] is not "":
                    if inside_inline:
                        new_nodes.append(TextNode(images[j][0],TextType.IMAGE,images[j][1]))
                        j += 1
                    else:
                        new_nodes.append(TextNode(tmp_strs[i],TextType.TEXT))
                        i += 1
                if inside_inline:
                    inside_inline = False
                else:
                    inside_inline = True



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    '''
    converts markdown to Text Node Format, that can be converted to HTML Nodes.
    '''
    pass
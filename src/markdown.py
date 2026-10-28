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
                if tmp_strs[i] != "":
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

def split_nodes_helper(text:str,extracted_List:list[tuple[str]], text_type:TextType) -> list[str]:
    '''Placeholder description
    '''
    if extracted_List == []: return [TextNode(text,TextType.TEXT)]
    if text_type is TextType.IMAGE:
        tmp = text.partition(f"![{extracted_List[0][0]}]({extracted_List[0][1]})")
    if text_type is TextType.LINK:
        tmp = text.partition(f"[{extracted_List[0][0]}]({extracted_List[0][1]})")

    nodes = []
    if tmp[0] != "":
        nodes.append(TextNode(tmp[0],TextType.TEXT))
    nodes.append(TextNode(extracted_List[0][0],text_type,extracted_List[0][1]))
    if tmp[2] != "":
        nodes.extend(split_nodes_helper(tmp[2], extracted_List[1:], text_type)) 
    return nodes

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
            new_nodes = split_nodes_helper(old_node.text,images,TextType.IMAGE)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    '''
    converts markdown to Text Node Format, that can be converted to HTML Nodes.
    '''
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            new_nodes = split_nodes_helper(old_node.text,links,TextType.LINK)
    return new_nodes
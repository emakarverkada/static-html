import re
from enum import Enum
from htmlnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNLIST = "unordered_list"
    OLIST = "ordered_list"


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        return (self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url
        )
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
            #raise ValueError("Delimited not found in string")      
        text = old_node.text.split(delimiter)
        if len(text) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        text[::2] = [TextNode(x, TextType.TEXT) for x in text[::2]]
        text[1::2] = [TextNode(x, text_type) for x in text[1::2]]
        text = [x for x in text if x.text]
        new_nodes.extend(text)
    return new_nodes

def split_nodes_image(old_nodes):
    pattern = r"!(\[[^\[\]]*\]\([^\(\)]*\))"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if not re.findall(pattern,old_node.text):
            #raise ValueError("Image not found in string")
            new_nodes.append(old_node)
            continue
        text = re.split(pattern, old_node.text)
        text[::2] = [TextNode(x, TextType.TEXT) for x in text[::2]]
        text[1::2] = [TextNode(re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", x)[0][0], TextType.IMAGE, re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", x)[0][1]) for x in text[1::2]]
        text = [x for x in text if x.text]
        new_nodes.extend(text)
    return new_nodes

def split_nodes_link(old_nodes):
    pattern = r"(?<!!)(\[[^\[\]]*\]\([^\(\)]*\))"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if not re.findall(pattern,old_node.text):
            #raise ValueError("Image not found in string")
            new_nodes.append(old_node)
            continue
        text = re.split(pattern, old_node.text)
        text[::2] = [TextNode(x, TextType.TEXT) for x in text[::2]]
        text[1::2] = [TextNode(re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", x)[0][0], TextType.LINK, re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", x)[0][1]) for x in text[1::2]]
        text = [x for x in text if x.text]
        new_nodes.extend(text)
    return new_nodes

def text_to_textnodes(text):
    text = [TextNode(text, TextType.TEXT)]
    text = split_nodes_delimiter(text, "**", TextType.BOLD)
    text = split_nodes_delimiter(text, "*", TextType.ITALIC)
    text = split_nodes_delimiter(text, "`", TextType.CODE)
    text = split_nodes_image(text)
    text = split_nodes_link(text)
    return text

def markdown_to_blocks(text):
    #text to blocks
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, text.strip())

def block_to_block_type(text):
    heading_regex = r"(?m)^#{1,6} .+" #every line starts with
    code_regex = r"^`{3}[\S\s]*?`{3}$" #first and last line equal to
    quote_rexex = r"(?m)^>.*"#matches should = number of lines
    unordered_regex = r"(?m)^\*|- .+"#every line starts with
    #x=1
    #ordered_regex = rf"^{x}+\. " #every line starts with + increments
    x = re.findall(heading_regex, text)
    if len(re.findall(heading_regex, text)) == len(text.split("\n")):
        return BlockType.HEADING
    elif re.match(code_regex, text):
        return BlockType.CODE
    elif len(re.findall(quote_rexex, text)) == len(text.split("\n")):
        return BlockType.QUOTE
    elif len(re.findall(unordered_regex, text)) == len(text.split("\n")):
        return BlockType.UNLIST
    elif all([re.findall(rf"^{i + 1}\. ", x) for i, x in enumerate(text.split("\n"))]):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

block = "1. list\n2. items"
print ([re.findall(rf"^1\. ", x) for x in block.split("\n")])

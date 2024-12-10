from textnode import *
from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNLIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(text):
    #text to blocks
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, text.strip())

def block_to_block_type(text):
    heading_regex = r"(?m)^#{1,6} .+" #every line starts with
    code_regex = r"^`{3}[\S\s]*?`{3}$" #first and last line equal to
    quote_rexex = r"(?m)^>.*"#matches should = number of lines
    unordered_regex = r"(?m)^(\*|-) .+"#every line starts with
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

def block_to_children(block):
    textnodes = text_to_textnodes(block)
    return [text_node_to_html_node(textnode) for textnode in textnodes]

def remove_headings(block, heading):
    text = block.split("\n")
    return [line.lstrip(heading) for line in text]

def markdown_to_html_node(markdown):
    text = markdown_to_blocks(markdown)
    nodes = []
    for block in text:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p",children = block_to_children(" ".join(remove_headings(block,"")))))
            case BlockType.HEADING:
                nodes.append(ParentNode(f"h{block[:5].count("#")}",children = block_to_children(" ".join(remove_headings(block, "# ")))))
            case BlockType.QUOTE:
                nodes.append(ParentNode("blockquote", children = block_to_children(" ".join(remove_headings(block, "> ")))))
            case BlockType.CODE:
                nodes.append(ParentNode("code", children = block_to_children(block.replace('```',''))))
            case BlockType.UNLIST:
                #need to limit to one replacement
                # child_nodes = [ParentNode("li", node) for node in [block_to_children(x) for x in remove_headings(block, "-* ")]]
                child_nodes = [ParentNode("li", node) for node in [block_to_children(x) for x in re.sub(r"^(\*|-) ", "", block, flags=re.MULTILINE).split("\n")]]
                nodes.append(ParentNode("ul", child_nodes))
            case BlockType.OLIST:
                child_nodes = [ParentNode("li", node) for node in [block_to_children(x) for x in re.sub(r"^\d*\. ", "", block, flags=re.MULTILINE).split("\n")]]
                nodes.append(ParentNode("ol", child_nodes))
    return ParentNode("div", nodes)

def extract_title(markdown):
    title = re.findall(r"^# .*?$", markdown, re.MULTILINE)
    if title:
        return title[0].strip("# ")
    raise Exception("No h1 title in string")
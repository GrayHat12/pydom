from typing import List, Literal, Union, overload
from src.interface.element import ElementInterface
from src.elements.element import Element
from src.parser import Parser
# from src.window.document import Document
from src.config.dom_token_list import DomTokenList


@overload
def parse_html(html: str, select_main: Literal[True]) -> ElementInterface: ...

@overload
def parse_html(html: str, select_main: Literal[False]) -> List[ElementInterface]: ...

@overload
def parse_html(html: str, select_main: bool) -> Union[List[ElementInterface], ElementInterface]: ...

def parse_html(html: str, select_main: bool = True) -> Union[List[ElementInterface], ElementInterface]:
    parser = Parser(False)
    parser.feed(html)
    if select_main:
        for element in parser.elements:
            if element.tagName == "html":
                return element
    return parser.elements

@overload
def parse_html_from_file(path: str, select_main: Literal[True]) -> ElementInterface: ...

@overload
def parse_html_from_file(path: str, select_main: Literal[False]) -> List[ElementInterface]: ...

@overload
def parse_html_from_file(path: str, select_main: bool) -> Union[List[ElementInterface], ElementInterface]: ...

def parse_html_from_file(path: str, select_main: bool = True):
    with open(path, "r", encoding="utf-8") as file:
        return parse_html(file.read(), select_main)
import html
from importlib import import_module
from inspect import isclass
import traceback
from typing import Callable, Optional, Tuple, TypeVar
from src.config.parser_settings import clean_tag

# from src.elements.element import Element, TextElement_
# from src.elements._text__element import TextElement_
from src.interface.element import ElementInterface

T = TypeVar('T')


def traverse(
        node: ElementInterface,
        match: Callable[[ElementInterface], bool],
        on_match: Callable[[ElementInterface, T], Tuple[bool, T]],
        on_miss: Callable[[ElementInterface, T], Tuple[bool, T]],
        default_result: T):
    stop = False

    if match(node):
        stop, default_result = on_match(node, default_result)
    else:
        stop, default_result = on_miss(node, default_result)

    if stop:
        return default_result
    for child in node.children:
        default_result = traverse(
            child, match, on_match, on_miss, default_result)

    return default_result


def tag_to_element(tag: str) -> Optional[ElementInterface]:
    tag = clean_tag(tag)
    classpath = f"src.elements.{tag}_element"
    try:
        module = import_module(classpath)
        element_class = getattr(module, f"{tag.upper()}Element")
        if isclass(element_class):
            return element_class()
    except Exception:
        traceback.print_exc()

    return None


def str_to_element(string: str) -> ElementInterface:
    genericpath = f"src.elements._text__element"
    module = import_module(genericpath)
    element_class = getattr(module, "TextElement_")
    if isclass(element_class):
        return element_class(html.unescape(string))
    raise Exception("Could not find TextElement_ class")


def copy_element(element: ElementInterface):
    new_element = createElement(element.tagName)
    for key, value in element.attributes.items():
        new_element.setAttribute(key, value)
    new_element.innerHTML = element.innerHTML
    return new_element


def createElement(tag: str) -> ElementInterface:
    print(f"Creating element {tag}")
    element = tag_to_element(tag)
    if not element:
        genericpath = f"src.elements.element"
        module = import_module(genericpath)
        element_class = getattr(module, "Element")
        if isclass(element_class):
            return element_class(clean_tag(tag))
        raise Exception("Could not find Element class")
    return element

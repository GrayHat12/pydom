from typing import Optional
from src.config.utils import createElement
from src.interface.element import ElementInterface

QUERY_SELECTORS_SYNTAX = {
    "id": r'#([\w-]+)',
    "class": r'\.([\w-]+)',
    "attribute": r'\[([\w-]+)(=[\"\']?([\w-]+)[\"\']?)?\]',
    "pseudo": r':([\w-]+)(\(([\w-]+)\))?',
    "combinator": r'([\s\+>~]+)',
    "universal": r'\*',
    "tag": r'([\w-]+)',
}


class Document:
    def __init__(self, tree: Optional[ElementInterface] = None) -> None:
        if isinstance(tree, ElementInterface):
            self.__doc_tree = tree
        elif tree is None:
            self.__doc_tree = self.__initialize_empty_document()
        else:
            raise TypeError("tree must be an ElementInterface or None")

    def __initialize_empty_document(self):
        html = createElement("html")
        head = createElement("head")
        body = createElement("body")
        html.appendChild(head)
        html.appendChild(body)
        return html

    def createElement(self, tag):
        return createElement(tag)

    def __query_selector(self, query: str, one: bool = False):
        raise NotImplementedError()

    def querySelector(self, query: str):
        return self.__query_selector(query, one=True)

    def querySelectorAll(self, query: str):
        return self.__query_selector(query, one=False)

    def getElementById(self, id: str):
        return self.__doc_tree.getElementById(id)

    def getElementsByClassName(self, class_name: str):
        return self.__doc_tree.getElementsByClassName(class_name)

    def getElementsByTagName(self, tag_name: str):
        return self.__doc_tree.getElementsByTagName(tag_name)

    def getElementsByName(self, name):
        return self.__doc_tree.getElementsByName(name)

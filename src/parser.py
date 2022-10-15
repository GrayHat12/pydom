from html.parser import HTMLParser
from typing import List, Optional, Tuple
from src.config.utils import createElement, str_to_element
from src.interface.element import ElementInterface


class DomStack:
    def __init__(self):
        self.stack: List[Tuple[ElementInterface, bool]] = []

    def start_element(self, element: ElementInterface):
        self.stack.append((element, False))

    def stop_element(self, tag: str):
        current = self.stack[len(self.stack) - 1]

        if not current:
            raise Exception("No element to close")

        if current[0].tagName == tag and not current[1]:
            self.stack[len(self.stack) - 1] = (current[0], True)

        else:
            # find the last unclosed element with the same tag
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0].tagName == tag and not self.stack[i][1]:
                    self.stack[i] = (self.stack[i][0], True)
                    children = self.stack[i+1:]
                    self.stack = self.stack[:i+1]
                    for child in children:
                        self.stack[-1][0].appendChild(child[0])
                    return


class Parser(HTMLParser):

    def __init__(self, convert_charrefs: bool = True):
        if not isinstance(convert_charrefs, bool):
            convert_charrefs = True

        self.__elements = DomStack()
        self.__declarations: List[str] = []

        HTMLParser.__init__(self, convert_charrefs=convert_charrefs)

    @property
    def elements(self) -> List[ElementInterface]:
        elements: List[ElementInterface] = []
        for element in self.__elements.stack:
            elements.append(element[0])
        return elements

    @property
    def declarations(self) -> List[str]:
        return self.__declarations

    def handle_startendtag(self, tag: str, attrs: list[Tuple[str, Optional[str]]]):
        print("Encountered a start-end tag:", tag, attrs)
        element = createElement(tag)
        for attr in attrs:
            element.setAttribute(attr[0], attr[1])

        self.__elements.start_element(element)
        self.__elements.stop_element(element.tagName)

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        print("Encountered a start tag:", tag, attrs)
        element = createElement(tag)
        for attr in attrs:
            element.setAttribute(attr[0], attr[1])

        self.__elements.start_element(element)

        if element.tagName == "script" and element.hasAttribute("src"):
            self.__elements.stop_element(element.tagName)
            print("stopped script tag")

        elif element.tagName == "meta":
            self.__elements.stop_element(element.tagName)
            print("stopped meta tag")

        elif element.tagName == "br":
            self.__elements.stop_element(element.tagName)
            print("stopped br tag")

        elif element.tagName == "img":
            self.__elements.stop_element(element.tagName)
            print("stopped img tag")

    def handle_endtag(self, tag: str):
        print("Encountered an end tag :", tag)

        self.__elements.stop_element(tag)

    def handle_charref(self, name: str):
        print("Encountered a character reference:", name)
        if not name:
            return

        element = str_to_element(name)

        self.__elements.start_element(element)
        self.__elements.stop_element(element.tagName)

    def handle_entityref(self, name: str):
        print("Encountered an entity reference:", name)

        if not name:
            return

        element = str_to_element(name)

        self.__elements.start_element(element)
        self.__elements.stop_element(element.tagName)

    def handle_data(self, data: str):
        print("Encountered some data  :", data)

        data = data.strip(" \t\n")
        if not data:
            return

        element = str_to_element(data)

        self.__elements.start_element(element)
        self.__elements.stop_element(element.tagName)

    def handle_comment(self, data: str):
        print("Encountered comment  :", data)

    def handle_decl(self, decl: str):
        print("Encountered declaration  :", decl)
        self.__declarations.append(decl)

    def handle_pi(self, data: str):
        print("Encountered some PI  :", data)

    def feed(self, data: str):
        data = data.strip(" \n")
        return super().feed(data)

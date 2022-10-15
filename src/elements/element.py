from io import TextIOWrapper
import json
from typing import Optional
from typing import Dict, List, Optional, Union
from src.config.dom_token_list import DomTokenList

from src.config.parser_settings import attribute_to_str
from src.config.utils import str_to_element, traverse
from src.interface.element import ElementInterface
from src.parser import Parser


class Element(ElementInterface):

    def __init__(self, tag: str) -> None:

        if not isinstance(tag, str):
            raise TypeError("tag must be a string")

        self.__tag_name = tag
        self.__attributes: Dict[str, str] = {}
        self.__children: List[Element] = []
        self.__parent: Optional[ElementInterface] = None

    @property
    def tagName(self) -> str:
        return self.__tag_name

    @property
    def id(self) -> Optional[str]:
        return self.attributes.get("id", None)

    @id.setter
    def id(self, value: str) -> None:
        self.setAttribute("id", value)

    @property
    def className(self) -> Optional[str]:
        return self.attributes.get("class", None)

    @className.setter
    def className(self, value: str) -> None:
        self.setAttribute("class", value)

    @property
    def classList(self):
        classlist = (self.className or "").split()

        def on_change(new_classlist: List[str]):
            self.className = " ".join(new_classlist)

        controlled_list = DomTokenList(on_change, classlist)
        return controlled_list

    @property
    def innerHTML(self) -> str:
        return "\n".join([str(child) for child in self.children])

    @innerHTML.setter
    def innerHTML(self, html: Union[str, List[ElementInterface], ElementInterface]):
        if isinstance(html, str):
            parser = Parser()
            parser.feed(html)
            self.__children.clear()
            for element in parser.elements:
                self.appendChild(element)
        if isinstance(html, list) and all([isinstance(element, ElementInterface) for element in html]):
            self.__children.clear()
            for element in html:
                self.appendChild(element)
        elif isinstance(html, ElementInterface):
            self.__children.clear()
            self.appendChild(html)
        else:
            raise TypeError(
                "innerHTML must be a string, list or ElementInterface")

    @property
    def outerHTML(self) -> str:
        return str(self)

    @outerHTML.setter
    def outerHTML(self, html: Union[str, ElementInterface]):
        str_html = None
        if isinstance(html, str):
            str_html = html
        elif isinstance(html, ElementInterface):
            str_html = str(html)

        if str_html:
            parser = Parser()
            parser.feed(str_html)
            self.__children.clear()
            for element in parser.elements:
                self.__tag_name = element.tagName
                self.__attributes = element.attributes
                self.__children = element.children
                break
        else:
            raise TypeError("outerHTML must be a string or ElementInterface")

    @property
    def innerText(self) -> str:
        return "".join([child.innerText for child in self.children])

    @innerText.setter
    def innerText(self, text: str) -> None:
        self.__children.clear()
        self.appendChild(str_to_element(text))

    @property
    def outerText(self) -> str:
        return self.innerText

    @outerText.setter
    def outerText(self, text: str) -> None:
        element = str_to_element(text)
        self.__tag_name = element.tagName
        self.__attributes = element.attributes
        self.__children = element.children

    @property
    def attributes(self) -> Dict[str, str]:
        return self.__attributes

    @property
    def children(self) -> List[ElementInterface]:
        return self.__children

    @property
    def parent(self) -> Optional[ElementInterface]:
        return self.__parent

    @property
    def firstChild(self) -> Optional[ElementInterface]:
        if len(self.children) > 0:
            return self.children[0]
        return None

    @property
    def lastChild(self) -> Optional[ElementInterface]:
        if len(self.children) > 0:
            return self.children[-1]
        return None

    @property
    def nextSibling(self) -> Optional[ElementInterface]:
        if self.parent:
            index = self.parent.children.index(self) + 1
            if index < len(self.parent.children)-1 and index >= 0:
                return self.parent.children[index]
        return None

    @property
    def previousSibling(self) -> Optional[ElementInterface]:
        if self.parent:
            index = self.parent.children.index(self) - 1
            if index < len(self.parent.children)-1 and index >= 0:
                return self.parent.children[index]
        return None

    def appendChild(self, child: Union[ElementInterface, str]):
        if isinstance(child, str):
            child = str_to_element(child)
        if not isinstance(child, ElementInterface):
            raise TypeError("child must be a string or ElementInterface")
        child.__setattr__(f"_{child.__class__.__name__}__parent", self)
        self.__children.append(child)

    def getAttribute(self, name: str) -> Optional[str]:
        return self.__attributes.get(name, None)

    def setAttribute(self, name: str, value: str) -> None:
        return self.__attributes.update({name: value})

    def removeAttribute(self, name: str):
        return self.__attributes.pop(name, None)

    def removeChild(self, child: ElementInterface) -> Optional[str]:
        child.__setattr__(f"_{self.__class__.__name__}__parent", None)
        return self.__children.remove(child)

    def hasAttribute(self, name: str) -> bool:
        return name in self.__attributes.keys()

    def hasAttributes(self) -> bool:
        return len(self.__attributes.keys()) > 0

    def hasChildNodes(self) -> bool:
        return len(self.__children) > 0

    def _get_indentation_str(self, indentation: int) -> str:
        return '\t'*indentation

    def __str__(self) -> str:
        output = ""
        attrs = [attribute_to_str(key, value)
                 for key, value in self.__attributes.items()]
        attrs = " ".join(attrs)
        attr_str = f" {attrs}" if attrs else ""
        output += f"<{self.__tag_name}{attr_str}"
        if self.__children:
            output += ">"
            for child in self.__children:
                output += str(child)
            output += f"</{self.tagName}>"
        else:
            output += "/>"
        return output

    def write_to_file(self, fp: TextIOWrapper, indentation: int = 0):
        indentation_str = self._get_indentation_str(indentation)
        attrs = [attribute_to_str(key, value)
                 for key, value in self.__attributes.items()]
        attrs = " ".join(attrs)
        attr_str = f" {attrs}" if attrs else ""
        fp.write(f"{indentation_str}<{self.__tag_name}{attr_str}")
        if self.__children:
            fp.write(">\n")
            for child in self.__children:
                child.write_to_file(fp, indentation+1)
            fp.write(f"\n{indentation_str}</{self.tagName}>")
        else:
            fp.write("/>")
        fp.write("\n")

    def getElementById(self, id: str):
        if not isinstance(id, str):
            raise TypeError("id must be a string")

        def match(elem: ElementInterface):
            return elem.id == id

        def on_match(elem: ElementInterface, result: Optional[ElementInterface]):
            return True, elem

        def on_miss(elem: ElementInterface, result: Optional[ElementInterface]):
            return False, result

        element = traverse(self, match, on_match, on_miss, None)
        return element

    def getElementsByClassName(self, classname: str):
        if not isinstance(classname, str):
            raise TypeError("id must be a string")

        def match(elem: ElementInterface):
            return elem.className == classname

        def on_match(elem: ElementInterface, result: List[ElementInterface]):
            if not result:
                result = []
            result.append(elem)
            return False, result

        def on_miss(elem: ElementInterface, result: List[ElementInterface]):
            return False, result

        element = traverse(self, match, on_match, on_miss, [])
        return element

    def getElementsByTagName(self, tag_name: str):
        def match(element: ElementInterface):
            return element.tagName == tag_name

        def on_match(element: ElementInterface, result: List[ElementInterface]):
            return False, result + [element]

        def on_miss(element: ElementInterface, result: List[ElementInterface]):
            return False, result

        return traverse(self, match, on_match, on_miss, [])

    def getElementsByName(self, name: str):

        def match(element: ElementInterface):
            return element.getAttribute("name") == name

        def on_match(element: ElementInterface, result: List[ElementInterface]):
            return False, result + [element]

        def on_miss(element: ElementInterface, result: List[ElementInterface]):
            return False, result

        return traverse(self, match, on_match, on_miss, [])

    def dict(self):
        return {
            "tagName": self.tagName,
            "attributes": self.attributes,
            "children": [child.dict() for child in self.children]
        }

    def json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.dict(), indent=indent)

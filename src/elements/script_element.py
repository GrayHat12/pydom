from io import TextIOWrapper
from typing import Union
from src.config.parser_settings import attribute_to_str
from src.elements.element import Element
from src.elements._text__element import TextElement_
from src.interface.element import ElementInterface


class SCRIPTElement(Element):

    def __init__(self) -> None:
        super().__init__('script')

    def appendChild(self, child: Union[ElementInterface, str]):
        if self.hasAttribute("src"):
            raise Exception(
                f"Cannot append child to script element with src attribute {str(self)}")
        elif not isinstance(child, TextElement_):
            raise Exception(
                f"Cannot append non text child to script element {str(child)}")
        super().appendChild(child)

    def __str__(self) -> str:
        output = ""
        attrs = [attribute_to_str(key, value)
                 for key, value in self.attributes.items()]
        attrs = " ".join(attrs)
        attr_str = f" {attrs}" if attrs else ""
        output += f"<{self.tagName}{attr_str}>"
        if self.children:
            output += "\n"
            for child in self.children:
                output += str(child) + "\n"
        output += f"</{self.tagName}>"
        return output

    def write_to_file(self, fp: TextIOWrapper, indentation: int = 0):
        output = str(self)
        indentation_str = self._get_indentation_str(indentation)
        fp.write(f"{indentation_str}{output}")

from io import TextIOWrapper
from src.config.parser_settings import attribute_to_str
from src.elements.element import Element


class SPANElement(Element):

    def __init__(self) -> None:
        super().__init__('span')

    def __str__(self) -> str:
        output = ""
        attrs = [attribute_to_str(key, value)
                 for key, value in self.attributes.items()]
        attrs = " ".join(attrs)
        attr_str = f" {attrs}" if attrs else ""
        output += f"<{self.tagName}{attr_str}>{[str(child) for child in self.children]}</{self.tagName}>"
        return output

    def write_to_file(self, fp: TextIOWrapper, indentation: int = 0):
        indentation_str = self._get_indentation_str(indentation)
        attrs = [attribute_to_str(key, value)
                 for key, value in self.attributes.items()]
        attrs = " ".join(attrs)
        attr_str = f" {attrs}" if attrs else ""
        fp.write(f"{indentation_str}<{self.tagName}{attr_str}>")
        for child in self.children:
            child.write_to_file(fp, indentation+1)
        fp.write(f"</{self.tagName}>")

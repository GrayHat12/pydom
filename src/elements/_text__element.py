import html
from io import TextIOWrapper
from src.elements.element import Element


class TextElement_(Element):

    def __init__(self, text: str = ""):
        super().__init__('#_text')
        self.text = text

    def __str__(self) -> str:
        return html.escape(self.text)

    def write_to_file(self, fp: TextIOWrapper, indentation: int = 0):
        fp.write(f"{str(self)}")

    @property
    def innerText(self) -> str:
        return self.text
    
    @innerText.setter
    def innerText(self, text: str) -> None:
        self.text = text
    
    @property
    def outerText(self) -> str:
        return self.text
    
    @outerText.setter
    def outerText(self, text: str) -> None:
        self.text = text
    
    @property
    def innerHTML(self) -> str:
        return self.text
    
    def dict(self):
        return {
            "text": self.text
        }
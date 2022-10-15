from abc import ABC, abstractmethod, abstractproperty
from io import TextIOWrapper
from typing import Dict, List, Optional, Union

from src.config.dom_token_list import DomTokenList


class ElementInterface(ABC):

    @abstractproperty
    def tagName(self) -> str:
        raise NotImplementedError()

    @abstractproperty
    def id(self) -> Optional[str]:
        raise NotImplementedError()

    @id.setter
    def id(self, value: str) -> None:
        raise NotImplementedError()

    @abstractproperty
    def className(self) -> Optional[str]:
        raise NotImplementedError()

    @className.setter
    def className(self, value: str) -> None:
        raise NotImplementedError()

    @abstractproperty
    def innerHTML(self) -> str:
        raise NotImplementedError()

    @innerHTML.setter
    def innerHTML(self, html: Union[str, List['ElementInterface'], 'ElementInterface']) -> None:
        raise NotImplementedError()

    @abstractproperty
    def outerHTML(self) -> str:
        raise NotImplementedError()

    @outerHTML.setter
    def outerHTML(self, html: Union[str, 'ElementInterface']) -> None:
        raise NotImplementedError()

    @abstractproperty
    def innerText(self) -> str:
        raise NotImplementedError()

    @innerText.setter
    def innerText(self, text: str) -> None:
        raise NotImplementedError()

    @abstractproperty
    def outerText(self) -> str:
        raise NotImplementedError()

    @outerText.setter
    def outerText(self, text: str) -> None:
        raise NotImplementedError()

    @abstractproperty
    def attributes(self) -> Dict[str, str]:
        raise NotImplementedError()

    @abstractproperty
    def children(self) -> List['ElementInterface']:
        raise NotImplementedError()

    @abstractproperty
    def parent(self) -> Optional['ElementInterface']:
        raise NotImplementedError()

    @abstractproperty
    def firstChild(self) -> Optional['ElementInterface']:
        raise NotImplementedError()

    @abstractproperty
    def lastChild(self) -> Optional['ElementInterface']:
        raise NotImplementedError()

    @abstractproperty
    def nextSibling(self) -> Optional['ElementInterface']:
        raise NotImplementedError()

    @abstractproperty
    def previousSibling(self) -> Optional['ElementInterface']:
        raise NotImplementedError()

    @abstractproperty
    def classList(self) -> DomTokenList[str]:
        raise NotImplementedError()

    @abstractmethod
    def appendChild(self, child: Union['ElementInterface', str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getAttribute(self, name: str) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def setAttribute(self, name: str, value: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def removeAttribute(self, name: str) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def removeChild(self, child: 'ElementInterface') -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def hasAttribute(self, name: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def hasAttributes(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def hasChildNodes(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def write_to_file(self, fp: TextIOWrapper, indentation: int = 0) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getElementById(self, id: str) -> Optional['ElementInterface']:
        raise NotImplementedError()

    @abstractmethod
    def getElementsByClassName(self, classname: str) -> List['ElementInterface']:
        raise NotImplementedError()

    @abstractmethod
    def getElementsByTagName(self, tag_name: str) -> List['ElementInterface']:
        raise NotImplementedError()

    @abstractmethod
    def getElementsByName(self, name: str) -> List['ElementInterface']:
        raise NotImplementedError()

    @abstractmethod
    def dict(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def json(self, indent: Optional[int]) -> str:
        raise NotImplementedError()

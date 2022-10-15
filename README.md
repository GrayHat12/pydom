# PyDom

Browser dom like interface for python with type hints.


------------

#### Cool stuff inside this project

1. Type hints:
   [pydom.py](pydom.py)
   ```python
   # Overload syntax for type hints
   @overload
   def parse_html(html: str, select_main: Literal[True]) -> ElementInterface: ...
   
   @overload
   def parse_html(html: str, select_main: Literal[False]) -> List[ElementInterface]: ...
   
   @overload
   def parse_html(html: str, select_main: bool) -> Union[List[ElementInterface], ElementInterface]: ...
   ```
2. Controlled List: [dom_token_list.py](src/config/dom_token_list.py)
3. Type hints inference for generic functions:
   [utils.py](src/config/utils.py)
    ```python
    T = TypeVar('T')

    def traverse(
            node: ElementInterface,
            match: Callable[[ElementInterface], bool],
            on_match: Callable[[ElementInterface, T], Tuple[bool, T]],
            on_miss: Callable[[ElementInterface, T], Tuple[bool, T]],
            default_result: T):
        ...
        # Type hints are automatically inferred for 'T' when calling this function with proper arguments
    ```
4. Using `importlib` can apparantly save you from cyclic dependency problems.
   [utils.py](src/config/utils.py)
    ```python
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
    ```
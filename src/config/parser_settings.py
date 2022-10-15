import html
from typing import Any


def clean_tag(tag: str):
    return tag.lower().strip()

# HTML_SPECIAL_CHAR_MAPPING = {
#     '"': '&quot;',
#     "'": '&apos;',
#     '>': '&gt;',
#     '<': '&lt;',
# }

def attribute_to_str(key: str, value: Any):
    if value is None:
        return f'{key}'
    if isinstance(value, bool):
        value = str(value).lower()
    value = str(value)
    value = html.escape(value, True)
    # for char, replacement in HTML_SPECIAL_CHAR_MAPPING.items():
    #     value = value.replace(char, replacement)
    return f'{key}="{value}"'
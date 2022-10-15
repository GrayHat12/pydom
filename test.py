# import json
from pydom import parse_html_from_file

if __name__ == "__main__":
    element = parse_html_from_file("index.html", True)
    with open("parsed.html", "w+", encoding="utf-8") as file:
        element.write_to_file(file)

    with open("parsed.json", "w+", encoding="utf-8") as file:
        file.write(element.json(indent=4))
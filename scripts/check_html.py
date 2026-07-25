"""Small, dependency-free markup sanity check for the static site."""

from html.parser import HTMLParser
from pathlib import Path


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.title_found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        if tag == "title":
            self.title_found = True


document = Path("index.html").read_text(encoding="utf-8")
parser = DocumentParser()
parser.feed(document)
parser.close()

assert parser.title_found, "Document must include a title"
assert not parser.duplicate_ids, f"Duplicate IDs: {sorted(parser.duplicate_ids)}"
assert 'lang="en"' in document, "Document must declare its language"
assert 'name="viewport"' in document, "Document must include a viewport meta tag"
print("HTML checks passed")

from pyparsing import (
    Empty,
    Group,
    Optional,
    Suppress,
    Word,
    alphanums,
    delimitedList,
    lineStart,
)

from .sections import GDSection, GDSectionHeader
from .values import value

key = Word(alphanums + "_/").setName("key")
var = Word(alphanums + "_").setName("variable")
attribute = Group(var + Suppress("=") + value)

section_header = (
    (
        Suppress(lineStart)
        + Suppress("[")
        + var.setResultsName("section_type")
        + Optional(delimitedList(attribute, Empty()))
        + Suppress("]")
    )
    .setName("section_header")
    .setParseAction(GDSectionHeader.from_parser)
)

section_entry = Group(Suppress(lineStart) + key + Suppress("=") + value).setName(
    "section_entry"
)
section_contents = delimitedList(section_entry, Empty()).setName("section_contents")

section = (
    (section_header + Optional(section_contents))
    .setName("section")
    .setParseAction(GDSection.from_parser)
)

scene_file = delimitedList(section, Empty())


from pathlib import Path
import json
import re

INPUT_FILE = Path(
    "data/processed/pm-kisan/revised-operational-guidelines-2020.json"
)

OUTPUT_FILE = Path(
    "data/processed/pm-kisan/revised-operational-guidelines-2020-sections.json"
)

STANDALONE_SECTION = re.compile(
    r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.?$"
)

INLINE_SECTION = re.compile(
    r"^(\d{1,2}(?:\.\d{1,2}){1,3})\.?\s+(.+)$"
)

def parse_section_marker(line):
    line = line.strip()

    standalone_match = STANDALONE_SECTION.fullmatch(line)

    if standalone_match:
        section_number = standalone_match.group(1)

        return {
            "section_number": section_number,
            "inline_title": None,
            "marker_type": "standalone"
        }

    inline_match = INLINE_SECTION.match(line)

    if inline_match:
        return {
            "section_number": inline_match.group(1),
            "inline_text": inline_match.group(2).strip(),
            "marker_type": "inline"
        }

    return None

def get_parent_section(section_number):
    parts = section_number.split(".")

    if len(parts) == 1:
        return None

    return ".".join(parts[:-1])


def is_main_section(section_number):
    return "." not in section_number


if __name__ == "__main__":
    test_sections = [
        "5",
        "5.3",
        "5.3.2",
        "5.5.1",
        "10.1"
    ]

    for section in test_sections:
        print(
            section,
            "| Parent:", get_parent_section(section),
            "| Main section:", is_main_section(section)
        )

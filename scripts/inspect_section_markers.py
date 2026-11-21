
from pathlib import Path
import json
import re

INPUT_FILE = Path(
    "data/processed/pm-kisan/revised-operational-guidelines-2020.json"
)

STANDALONE_NUMBER = re.compile(
    r"^\d{1,2}(?:\.\d{1,2}){0,3}\.?$"
)

INLINE_SECTION = re.compile(
    r"^(\d{1,2}(?:\.\d{1,2}){1,3})\.?\s+(.+)$"
)


def next_non_empty_line(lines, index):
    for line in lines[index + 1:]:
        if line.strip():
            return line.strip()

    return ""


def is_date(value):
    parts = value.rstrip(".").split(".")

    return (
        len(parts) == 3
        and len(parts[2]) == 4
    )


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        document = json.load(file)

    for page in document["pages"]:
        lines = page["cleaned_text"].splitlines()

        print(f"\n{'=' * 60}")
        print(f"PAGE {page['page_number']}")
        print(f"{'=' * 60}")

        for index, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                continue

            if index == 0 and stripped == str(page["page_number"]):
                print(f"PAGE NUMBER: {stripped}")
                continue

            if STANDALONE_NUMBER.fullmatch(stripped):
                if is_date(stripped):
                    continue

                following = next_non_empty_line(lines, index)

                print(
                    f"STANDALONE SECTION CANDIDATE: "
                    f"{stripped} -> {following}"
                )
                continue

            match = INLINE_SECTION.match(stripped)

            if match:
                section_number = match.group(1)

                if is_date(section_number):
                    continue

                print(
                    f"INLINE SECTION CANDIDATE: "
                    f"{section_number} -> {match.group(2)}"
                )


if __name__ == "__main__":
    main()

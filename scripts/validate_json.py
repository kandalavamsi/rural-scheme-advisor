
from pathlib import Path
import json

DATA_DIR = Path("data/processed/pm-kisan")

required_fields = [
    "source_file",
    "source_relative_path",
    "document_scope",
    "jurisdiction",
    "total_pages",
    "pdf_metadata",
    "pages"
]

for json_path in sorted(DATA_DIR.glob("*.json")):
    with json_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    missing_page_data = [
        page["page_number"]
        for page in data.get("pages", [])
        if not page.get("raw_text", "").strip()
        or not page.get("cleaned_text", "").strip()
    ]

    page_count_matches = (
        data.get("total_pages") == len(data.get("pages", []))
    )

    print(f"\nFILE: {json_path.name}")
    print("Missing document fields:", missing_fields)
    print("Missing page text:", missing_page_data)
    print("Page count matches:", page_count_matches)
    print("Scope:", data.get("document_scope"))
    print("Jurisdiction:", data.get("jurisdiction"))

    if (
        missing_fields
        or missing_page_data
        or not page_count_matches
    ):
        print("RESULT: FAILED")
    else:
        print("RESULT: PASSED")

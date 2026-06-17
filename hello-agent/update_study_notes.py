import os, json, datetime, sys

NOTES_FILE = r"D:\iCloudDrive\iCloud~md~obsidian\shushu\hello-agents\python_study_notes.md"
TRACKER_FILE = r"D:\iCloudDrive\iCloud~md~obsidian\shushu\hello-agents\.progress.json"

def update_notes(concepts, chapter, notes_text):
    # Load tracker
    tracker = {"concepts_covered": [], "current_chapter": "", "progress_notes": ""}
    if os.path.isfile(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            tracker = json.load(f)

    today = datetime.date.today().isoformat()
    tracker["last_updated"] = today
    tracker["current_chapter"] = chapter
    tracker["progress_notes"] = notes_text

    # Merge concepts (avoid dupes)
    existing = set(tracker["concepts_covered"])
    for c in concepts:
        existing.add(c)
    tracker["concepts_covered"] = sorted(existing)

    # Write tracker
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(tracker, f, ensure_ascii=False, indent=2)

    # Update markdown notes
    lines = []
    lines.append("# Hello Agents - Python \u5b66\u4e60\u7b14\u8bb0\n")
    lines.append(f"> \u6700\u540e\u66f4\u65b0: {today}  |  \u5f53\u524d\u7ae0\u8282: {chapter}\n")
    lines.append("---\n")
    lines.append("## \u5df2\u5b66\u6982\u5ff5\n")
    lines.append("")
    for c in sorted(existing):
        lines.append(f"- [x] {c}")
    lines.append("")
    lines.append("---\n")
    lines.append("## \u5b66\u4e60\u8fdb\u5ea6\n")
    lines.append("")
    lines.append(notes_text)
    lines.append("")

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\u2705 \u7b14\u8bb0\u5df2\u66f4\u65b0: {NOTES_FILE}")
    print(f"\u5df2\u5b66\u6982\u5ff5 ({len(existing)} \u4e2a):")
    for c in sorted(existing):
        print(f"  - {c}")

if __name__ == "__main__":
    # Example: called with args
    concepts = sys.argv[1].split(",") if len(sys.argv) > 1 else []
    chapter = sys.argv[2] if len(sys.argv) > 2 else "unknown"
    notes_text = sys.argv[3] if len(sys.argv) > 3 else ""
    update_notes(concepts, chapter, notes_text)

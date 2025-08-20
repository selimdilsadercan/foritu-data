import re
import json

def parse_elective(elective_str):
    # Example: [8th Semester Elective Course I (MT)*(BLG 413E|BLG 430E|...)]
    match = re.match(
        r"\[(.*?)\s*\((.*?)\)\*\((.*?)\)\]", elective_str
    )
    if not match:
        return None
    name_full, category, options = match.groups()
    return {
        "type": "elective",
        "name": name_full.strip(),
        "category": category.strip(),
        "options": [opt.strip() for opt in options.split("|")]
    }

def parse_line(line):
    items = line.strip().split("=")
    semester = []
    for item in items:
        item = item.strip()
        if item.startswith("[") and item.endswith("]"):
            elective = parse_elective(item)
            if elective:
                semester.append(elective)
        else:
            semester.append({
                "type": "course",
                "code": item
            })
    return semester

def main():
    with open("../data/plan.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    semesters = [parse_line(line) for line in lines if line.strip()]
    with open("../reports/plan.json", "w", encoding="utf-8") as f:
        json.dump(semesters, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
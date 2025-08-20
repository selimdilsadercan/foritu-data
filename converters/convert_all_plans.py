import json
import re
from typing import List, Dict, Any, Optional

def parse_elective_course(elective_text: str) -> Dict[str, Any]:
    """
    Parse elective course text like "[5th Semester Elective Course (TM)*(INS 313E|INS 315E|INS 317E|INS 319E)]"
    """
    # Extract name and category
    match = re.match(r'\[([^(]+)\(([^)]+)\)\*\(([^)]+)\)\]', elective_text)
    if not match:
        # Try alternative format
        match = re.match(r'\[([^(]+)\(([^)]+)\)\*\(([^)]+)\)\]', elective_text)
        if not match:
            # Try simpler format
            match = re.match(r'\[([^(]+)\(([^)]+)\)\*\(([^)]+)\)\]', elective_text)
            if not match:
                return None
    
    if match:
        name = match.group(1).strip()
        category = match.group(2).strip()
        options_text = match.group(3).strip()
        options = [opt.strip() for opt in options_text.split('|')]
        
        return {
            "name": name,
            "category": category,
            "options": options
        }
    
    return None

def parse_course_line(line: str) -> List[Dict[str, Any]]:
    """
    Parse a course line like "FIZ 101=KIM 101=BIL 101E=MAT 101E=RES 101=FIZ 101L=KIM 101L=[English Course I*(ING 101|ING 102)]"
    """
    courses = []
    parts = line.split('=')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Check if it's an elective course
        if part.startswith('[') and part.endswith(']'):
            elective = parse_elective_course(part)
            if elective:
                courses.append({
                    "type": "elective",
                    "data": elective
                })
        else:
            # Regular course code
            courses.append({
                "type": "course",
                "code": part
            })
    
    return courses

def parse_course_plans(file_path: str) -> Dict[str, Any]:
    """
    Parse the course plans file and convert to JSON structure
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    lines = content.split('\n')
    
    result = {
        "faculties": []
    }
    
    current_faculty = None
    current_program = None
    current_period = None
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        if not line:
            continue
            
        # Faculty header (starts with # but not ## or ###)
        if line.startswith('# ') and not line.startswith('##') and not line.startswith('###'):
            faculty_name = line[2:].strip()
            current_faculty = {
                "name": faculty_name,
                "programs": []
            }
            result["faculties"].append(current_faculty)
            current_program = None
            current_period = None
            print(f"Found faculty: {faculty_name}")
            
        # Program header (starts with ##)
        elif line.startswith('## '):
            program_name = line[3:].strip()
            current_program = {
                "name": program_name,
                "periods": []
            }
            if current_faculty:
                current_faculty["programs"].append(current_program)
            current_period = None
            print(f"Found program: {program_name}")
            
        # Period header (starts with ###)
        elif line.startswith('### '):
            period_name = line[4:].strip()
            current_period = {
                "name": period_name,
                "semesters": []
            }
            if current_program:
                current_program["periods"].append(current_period)
            print(f"Found period: {period_name}")
            
        # Course line (contains = and course codes, but not starting with #)
        elif '=' in line and not line.startswith('#'):
            if current_period:
                # Parse the course line
                courses = parse_course_line(line)
                
                # Create a semester entry
                semester = {
                    "courses": courses
                }
                current_period["semesters"].append(semester)
                print(f"Processing line {line_num}: {line[:50]}...")
    
    return result

def main():
    """
    Main function to convert course plans to JSON
    """
    input_file = "../data/course_plans.txt"
    output_file = "../reports/all_plans.json"
    
    print("Starting conversion...")
    
    # Parse the course plans
    plans = parse_course_plans(input_file)
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)
    
    # Print summary
    total_faculties = len(plans["faculties"])
    total_programs = sum(len(f["programs"]) for f in plans["faculties"])
    total_periods = sum(len(p["periods"]) for f in plans["faculties"] for p in f["programs"])
    total_semesters = sum(len(per["semesters"]) for f in plans["faculties"] for p in f["programs"] for per in p["periods"])
    
    print(f"\nSuccessfully converted to {output_file}")
    print(f"\nSummary:")
    print(f"- Faculties: {total_faculties}")
    print(f"- Programs: {total_programs}")
    print(f"- Periods: {total_periods}")
    print(f"- Semesters: {total_semesters}")
    
    # Print faculty names
    print(f"\nFaculties found:")
    for faculty in plans["faculties"]:
        print(f"- {faculty['name']}")
        for program in faculty["programs"]:
            print(f"  - {program['name']}")

if __name__ == "__main__":
    main() 
import json
import csv
import re

def parse_special_conditions(prereq_text, coreq_text):
    """
    Parse special conditions from both prerequisites and corequisites fields
    
    Examples:
    - "Yok" -> []
    - "4.Sınıf" -> ["4.Sınıf"]
    - "3.Sınıf ,4.Sınıf" -> ["3.Sınıf", "4.Sınıf"]
    - "4.Sınıf ,3.Sınıf" -> ["4.Sınıf", "3.Sınıf"]
    - "Yok Diğer Şartlar" -> ["Diğer Şartlar"]
    - "END 441 MIN DDveya END 441E MIN DD Diğer Şartlar" -> ["Diğer Şartlar"]
    """
    special_conditions = []
    
    # Extract year requirements (X.Sınıf) from corequisites
    if coreq_text and coreq_text.strip() != "Yok":
        year_matches = re.findall(r'\d+\.Sınıf', coreq_text)
        special_conditions.extend(year_matches)
    
    # Extract "Diğer Şartlar" (Other Conditions) from prerequisites
    if prereq_text and "Diğer Şartlar" in prereq_text:
        special_conditions.append("Diğer Şartlar")
    
    return special_conditions

def parse_prerequisites(prereq_text):
    """
    Parse prerequisite text into structured format with logical grouping
    
    Examples:
    - "Yok" -> []
    - "MAT 102 MIN DDveya MAT 102E MIN DD" -> [{"group": 1, "courses": [{"code": "MAT102", "min": "DD"}, {"code": "MAT102E", "min": "DD"}]}]
    - "(MAT 281 MIN DDveya MAT 281E MIN DD)ve (BIL 105E MIN DDveya BIL 105 MIN DD)" -> 
      [
        {"group": 1, "courses": [{"code": "MAT281", "min": "DD"}, {"code": "MAT281E", "min": "DD"}]},
        {"group": 2, "courses": [{"code": "BIL105E", "min": "DD"}, {"code": "BIL105", "min": "DD"}]}
      ]
    """
    if not prereq_text or prereq_text.strip() == "Yok":
        return []
    
    prerequisites = []
    
    # Check if there are grouped prerequisites (with parentheses and "ve")
    if "ve (" in prereq_text or prereq_text.startswith("("):
        # Handle grouped prerequisites
        group_num = 1
        
        # Split by "ve (" to separate groups
        groups = re.split(r've\s*\(', prereq_text)
        
        for i, group in enumerate(groups):
            if i == 0:
                # First group might not start with "ve ("
                if group.startswith("("):
                    group = group[1:]  # Remove opening parenthesis
            else:
                # Subsequent groups start with "ve ("
                pass
            
            # Find the closing parenthesis for this group
            if ")" in group:
                group_content = group[:group.find(")")]
            else:
                group_content = group
            
            # Parse courses within this group (OR conditions)
            group_courses = []
            or_parts = group_content.split("veya")
            
            for or_part in or_parts:
                or_part = or_part.strip()
                # Extract course code and minimum grade
                match = re.search(r'([A-Z]{2,4}\s+\d+[A-Z]?)\s+MIN\s+([A-Z]+)', or_part)
                if match:
                    course_code = match.group(1).replace(" ", "")  # Remove spaces
                    min_grade = match.group(2)
                    group_courses.append({
                        "code": course_code,
                        "min": min_grade
                    })
            
            if group_courses:
                prerequisites.append({
                    "group": group_num,
                    "courses": group_courses
                })
                group_num += 1
        
        # Handle any remaining content after the last group
        remaining = prereq_text.split(")")[-1].strip()
        if remaining and "veya" in remaining:
            remaining_courses = []
            or_parts = remaining.split("veya")
            for or_part in or_parts:
                or_part = or_part.strip()
                match = re.search(r'([A-Z]{2,4}\s+\d+[A-Z]?)\s+MIN\s+([A-Z]+)', or_part)
                if match:
                    course_code = match.group(1).replace(" ", "")
                    min_grade = match.group(2)
                    remaining_courses.append({
                        "code": course_code,
                        "min": min_grade
                    })
            
            if remaining_courses:
                prerequisites.append({
                    "group": group_num,
                    "courses": remaining_courses
                })
    
    else:
        # Simple case: only "veya" conditions (no grouping)
        group_courses = []
        or_parts = prereq_text.split("veya")
        
        for or_part in or_parts:
            or_part = or_part.strip()
            # Extract course code and minimum grade
            match = re.search(r'([A-Z]{2,4}\s+\d+[A-Z]?)\s+MIN\s+([A-Z]+)', or_part)
            if match:
                course_code = match.group(1).replace(" ", "")  # Remove spaces
                min_grade = match.group(2)
                group_courses.append({
                    "code": course_code,
                    "min": min_grade
                })
        
        if group_courses:
            prerequisites.append({
                "group": 1,
                "courses": group_courses
            })
    
    return prerequisites

def convert_psv_to_json(psv_file_path, json_file_path):
    """
    Convert PSV (Pipe-Separated Values) file to JSON format
    
    PSV Structure:
    Field 0: Course Code
    Field 1: Course Name
    Field 2: Language
    Field 3: Credits
    Field 4: ECTS Credits
    Field 5: Prerequisites
    Field 6: Corequisites
    Field 7: Description
    """
    
    courses = []
    
    try:
        # Try different encodings to handle Turkish characters properly
        encodings = ['utf-8', 'latin-1', 'cp1254', 'iso-8859-9']
        
        for encoding in encodings:
            try:
                with open(psv_file_path, 'r', encoding=encoding) as file:
                    for line_num, line in enumerate(file, 1):
                        line = line.strip()
                        if not line:  # Skip empty lines
                            continue
                        
                        # Split by pipe character
                        fields = line.split('|')
                        
                        # Check if we have the expected number of fields
                        if len(fields) != 8:
                            print(f"Warning: Line {line_num} has {len(fields)} fields instead of 8. Skipping.")
                            continue
                        
                        # Parse prerequisites
                        prerequisites = parse_prerequisites(fields[5].strip())
                        
                        # Parse special conditions from corequisites
                        special_conditions = parse_special_conditions(fields[5].strip(), fields[6].strip())
                        
                        # Create course object
                        course = {
                            "code": fields[0].strip(),
                            "name": fields[1].strip(),
                            "language": fields[2].strip(),
                            "credits": fields[3].strip(),
                            "ects_credits": fields[4].strip(),
                            "prerequisites": prerequisites,
                            "special_conditions": special_conditions,
                            "corequisites": fields[6].strip(),
                            "description": fields[7].strip()
                        }
                        
                        courses.append(course)
                
                print(f"Successfully read file with {encoding} encoding")
                break
                
            except UnicodeDecodeError:
                print(f"Failed with {encoding} encoding, trying next...")
                courses = []  # Reset courses list
                continue
        
        if not courses:
            print("Error: Could not read file with any encoding")
            return None
        
        # Print some statistics
        print(f"\nStatistics:")
        print(f"Total courses: {len(courses)}")
        
        # Count courses by language
        languages = {}
        for course in courses:
            lang = course['language']
            languages[lang] = languages.get(lang, 0) + 1
        
        print(f"Languages: {languages}")
        
        # Show first few courses as example
        print(f"\nFirst 3 courses as example:")
        for i, course in enumerate(courses[:3]):
            print(f"{i+1}. {course['code']} - {course['name']} ({course['language']})")
            print(f"   Prerequisites: {course['prerequisites']}")
            print(f"   Special Conditions: {course['special_conditions']}")
        
        return courses
        
    except FileNotFoundError:
        print(f"Error: File {psv_file_path} not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_simple_output(courses, output_file):
    """
    Create a simplified version with only essential fields (no language, no ECTS credits)
    """
    simple_courses = []
    for course in courses:
        simple_courses.append({
            "code": course["code"],
            "name": course["name"],
            "credits": course["credits"],
            "prerequisites": course["prerequisites"],
            "special_conditions": course["special_conditions"]
        })
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(simple_courses, json_file, indent=2, ensure_ascii=False)
    
    print(f"Simple version saved to {output_file}")

if __name__ == "__main__":
    # Convert PSV to JSON
    psv_file = "../data/courses.psv"
    simple_json_file = "../reports/courses_simple.json"
    
    print("Converting courses.psv to simple JSON...")
    courses = convert_psv_to_json(psv_file, None)  # No detailed version needed
    
    if courses:
        # Create simple version only
        print("\nCreating simple version...")
        create_simple_output(courses, simple_json_file)
        
        print(f"\nConversion complete!")
        print(f"- Simple version: {simple_json_file}") 